from flask import Flask, render_template, request, jsonify
from Models.deteksi_di.DiWordDetector import DiWordDetector
from Models.deteksi_terikat.kataTerikat import patterns, validateSatuKata, validateDuaKata
from Models.deteksi_terikat.preprocessing import preprocessing
from Models.deteksi_terikat.rabinKarp import rabinKarp
from Models.deteksi_terikat.bigram import generate_bigrams
from fuzzywuzzy import fuzz
from nlp_id.postag import PosTag
from nlp_id.lemmatizer import Lemmatizer
from nltk.tokenize import sent_tokenize
import nltk
import pandas as pd
nltk.download('punkt')

app = Flask(__name__, template_folder='Templates')

@app.route('/')
def index():
    result_di = None
    paragraph_di = None
    result_terikat = {} 
    paragraph_terikat = None
    result_majemuk_final = []
    paragraph_majemuk = []
    return render_template('index.html', result_di=result_di, paragraph_di=paragraph_di,
                           result_majemuk_final=result_majemuk_final, paragraph_majemuk=paragraph_majemuk)

@app.route('/detect', methods=['POST'])
def detect_diword():
    if request.method == 'POST':
        # # Ambil data paragraf
        paragraph = request.form.get('paragraph')
        
        # # Detect Majemuk #
        # Baca dataset
        katamajemuk = pd.read_csv('Models/deteksi_majemuk/daftarkatamajemuk.csv')
        list_katamajemuk = katamajemuk['kata majemuk'].values.tolist()
        dataset = pd.read_csv('Models/deteksi_majemuk/dataset_kata_benar.csv')
        dataset = dataset['word'].values.tolist()
        
        # Define lemmatizer
        lemmatizer = Lemmatizer()
        
        #preprocess
        kalimat = paragraph
        kalimat = kalimat.lower()
        kalimat = ' '.join(kalimat.split())
        kalimat_kalimat = sent_tokenize(kalimat)
        postagger = PosTag()
        postTag = []

        for a in range(len(kalimat_kalimat)):
            postTag.append(postagger.get_pos_tag(kalimat_kalimat[a])) 

        multi_word=[]
        single_word=[]

        for a in range(len(postTag)): 
            for b in range(len(postTag[a])-1):
                if postTag[a][b][1] == 'NN':
                    if postTag[a][b + 1][1] == 'VB' or postTag[a][b + 1][1] == 'JJ' or postTag[a][b + 1][1] == 'NN':
                        multi_word.append([postTag[a][b], postTag[a][b + 1]])
                if postTag[a][b][1] == 'JJ':
                    if postTag[a][b + 1][1] == 'NN' or postTag[a][b + 1][1] == 'JJ':
                        multi_word.append([postTag[a][b], postTag[a][b + 1]])
                if postTag[a][b][1] == 'VB':
                    if postTag[a][b + 1][1] == 'VB' or postTag[a][b + 1][1] == 'NN':
                        multi_word.append([postTag[a][b], postTag[a][b + 1]])



        for a in range(len(postTag)):
            for b in range(len(postTag[a])):
                if postTag[a][b][1] == 'NN' or postTag[a][b][1] == 'VB' or postTag[a][b][1] == 'JJ':
                    single_word.append(postTag[a][b][0])

        pola = [' '.join(inner[0] for inner in outer) for outer in multi_word]


        x = []
        for a in pola:
            z = a.split()
            x.append(z)

        prefixes = ['me', 'be', 'te', 'ke', 'se', 'di', 'pe']
        suffixes = ['kan', 'an', 'i', 'nya']

        has_prefix=[]
        has_suffix=[]
        for a in range(len(x)):

                # Check if the word has a prefix
                for prefix in prefixes:
                    if x[a][0].startswith(prefix):
                        if x[a][0] != lemmatizer.lemmatize(x[a][0]):
                            has_prefix.append(x[a])

        for a in range(len(x)):

                # Check if the word has a suffix
                for suffix in suffixes:
                    if x[a][0].endswith(suffix):
                        if x[a][0] != 'angkatan' and x[a][0] != 'lapangan' :
                            if x[a][0] != lemmatizer.lemmatize(x[a][0]):
                                has_suffix.append(x[a])

        res_list = [y for x in [has_prefix, has_suffix] for y in x] #combine array
        combined_values = [' '.join(pair) for pair in res_list] #combine word
        mylist = list(dict.fromkeys(combined_values)) #remove duplicate
        list_multiword = [i for i in pola if i not in mylist]


        list_singleword = list(dict.fromkeys(single_word))

        # Compare words with dataset
        data = []

        for a in range(len(list_multiword)) :
            for b in range(len(list_katamajemuk)):
                similarity = fuzz.ratio(list_multiword[a], list_katamajemuk[b])
                if (similarity>=90) :
                    data.append([list_multiword[a], list_katamajemuk[b], similarity])
                else :
                    pass
                

        for a in range(len(list_singleword)) :
            for b in range(len(list_katamajemuk)):
                similarity = fuzz.ratio(list_singleword[a], list_katamajemuk[b])
                if (similarity>=90) :
                    data.append([list_singleword[a], list_katamajemuk[b], similarity])
                else : 
                    pass
        
        #Dataframe based on array data
        df = pd.DataFrame(data, columns=['Kata Majemuk', 'Kata Majemuk Koreksi', 'Similarity'])
        # Check if the 'Kata Majemuk' column exists in the DataFrame
        if 'Kata Majemuk' in df.columns:
            # Drop duplicates based on specified subset and keep the first occurrence
            df = df.drop_duplicates(subset=['Kata Majemuk', 'Kata Majemuk Koreksi'], keep='first').reset_index(drop=True)

            # Separate data into two DataFrames based on the 'Similarity' column
            df1 = df[df['Similarity'].eq(100)].drop_duplicates()
            df2 = df[df['Similarity'].lt(100)].drop_duplicates()

            # Exclude rows in df2 that are also present in df1 based on 'Kata Majemuk'
            df2 = df2[~df2['Kata Majemuk'].isin(df1['Kata Majemuk'])]

            # Extract lists from the resulting DataFrames
            majemuk = df2['Kata Majemuk'].values.tolist()
            koreksi = df2['Kata Majemuk Koreksi'].values.tolist()
            kemiripan = df2['Similarity'].values.tolist()
        else:
            # Handle the case when 'Kata Majemuk' column is not present
            majemuk = []
            koreksi = []
            kemiripan = []


        def check_whitespace_in_words(word_list):
            words_with_whitespace = [word for word in range(len(word_list)) if ' ' not in word_list[word]]

            return words_with_whitespace

        # Example usage:
        word_list = majemuk

        result_majemuk = check_whitespace_in_words(word_list)

        data = []
        for result in result_majemuk:
            data.append([majemuk[result], koreksi[result], kemiripan[result]])

        df_singleword = pd.DataFrame(data, columns=['Kata Majemuk', 'Kata Majemuk Koreksi', 'Similarity'])

        df_multiword = df2[~df2['Kata Majemuk'].isin(df_singleword['Kata Majemuk'])]

        df_singleword_majemuk = df_singleword['Kata Majemuk'].values.tolist()

        for word in df_singleword_majemuk:
            if word in dataset:
                df_singleword = df_singleword[df_singleword['Kata Majemuk'] != word]


        df = pd.concat([df1,df_singleword, df_multiword],ignore_index=True)

        df = df.groupby(['Kata Majemuk', 'Similarity']).agg({"Kata Majemuk Koreksi": ", ".join,}).reset_index()
        df = df.sort_values(by='Similarity', ascending=False)
        df = df.drop_duplicates(subset=['Kata Majemuk'])

        num = len(df1)
        kataMajemuk = df['Kata Majemuk'].values.tolist()
        kataKoreksi = df['Kata Majemuk Koreksi'].values.tolist()

        result_majemuk_final = {}
        i = 0
        for kata in kataMajemuk:
            if i < num :
                result_majemuk_final[kata] = {
                    'is_correct' : True,
                    'suggestion' : ''
                }
            else :
                result_majemuk_final[kata] = {
                    'is_correct' : False,
                    'suggestion' : kataKoreksi[i]
                }
            i += 1
            
         # Ambil data paragraf
        paragraph = request.form.get('paragraph')

        # Deteksi Kata DI
        detector = DiWordDetector()
        result_di = detector.detect_di_usage(paragraph)

        # Detect Kata Terikat        
        with open('Models/deteksi_terikat/kata-dasar.txt', 'r') as file:
            word_list = [line.strip() for line in file.readlines()]        
        preprocess = preprocessing(paragraph)

        # RabinKarp untuk cari pattern data input
        rbnKarp = rabinKarp(preprocess, patterns)

        # Sort hasil dari index terkecil
        sort_data = sorted(rbnKarp, key=lambda x: x[-1])

        # Remove duplicates
        unique_data = {item[2]: item for item in sort_data}.values()

        # Deteksi bigram
        bigrams = generate_bigrams(preprocess)
        deteksi_bigram_terikat = []

        # Cari pattern di bigram
        for word, index in bigrams:
            result_terikat = rabinKarp(word, patterns, True, index)
            if result_terikat != []:
                deteksi_bigram_terikat.append(result_terikat)

        result_terikat_dict = {}

        result_terikat_dict.update(validateSatuKata(unique_data, word_list))
            
        if deteksi_bigram_terikat:
            result_terikat_dict.update(validateDuaKata(deteksi_bigram_terikat, word_list, paragraph))
            
        if (result_terikat_dict == {}):
            result_terikat_dict = {'errormessage': "Tidak ada kata terikat yang ditemukan"}

        return render_template('index.html', result_di=result_di, paragraph_di=paragraph, 
                               result_terikat=result_terikat_dict, paragraph_terikat=paragraph,
                               result_majemuk_final=result_majemuk_final, paragraph_majemuk=paragraph
                               )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)
