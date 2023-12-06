
from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
from fuzzywuzzy import fuzz
from nlp_id.postag import PosTag
from nlp_id.lemmatizer import Lemmatizer
from nltk.tokenize import sent_tokenize


app = Flask(__name__, template_folder='index')


@app.route('/', methods=['GET', 'POST'])


def index():

    if request.method == 'POST':
        artikel = request.form['text']
        kalimat = artikel

        #read dataset
        katamajemuk = pd.read_csv('daftarkatamajemuk.csv')
        list_katamajemuk = katamajemuk['kata majemuk'].values.tolist()
        dataset = pd.read_csv('dataset_kata_benar.csv')
        dataset = dataset['word'].values.tolist()

        # create lemmatizer
        lemmatizer = Lemmatizer()

        #preprocess
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
        df = df.drop_duplicates( 
            subset = ['Kata Majemuk', 'Kata Majemuk Koreksi'], 
            keep = 'first').reset_index(drop = True)
        
        df1 = df[df['Similarity'].apply(lambda x : x == 100)]
        df2 = df[df['Similarity'].apply(lambda x : x < 100)]

        df1 = df1.drop_duplicates()
        df2 = df2[~df2['Kata Majemuk'].isin(df1['Kata Majemuk'])]

        majemuk = df2['Kata Majemuk'].values.tolist()
        koreksi = df2['Kata Majemuk Koreksi'].values.tolist()
        kemiripan = df2['Similarity'].values.tolist()


        def check_whitespace_in_words(word_list):
            words_with_whitespace = [word for word in range(len(word_list)) if ' ' not in word_list[word]]

            return words_with_whitespace

        # Example usage:
        word_list = majemuk

        result = check_whitespace_in_words(word_list)

        data = []
        for result in result:
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

        result = {}
        i = 0
        for kata in kataMajemuk:
            if i < num :
                result[kata] = {
                    'is_correct' : True,
                    'suggestion' : ''
                }
            else :
                result[kata] = {
                    'is_correct' : False,
                    'suggestion' : kataKoreksi[i]
                }
            i += 1
        return jsonify(result)
        #return render_template('result.html',  artikel=artikel, result=result)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
   
