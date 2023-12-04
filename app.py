from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from Models.deteksi_di.DiWordDetector import DiWordDetector
from Models.deteksi_terikat.kataTerikat import patterns, validateSatuKata, validateDuaKata
from Models.deteksi_terikat.preprocessing import preprocessing
from Models.deteksi_terikat.rabinKarp import rabinKarp
from Models.deteksi_terikat.bigram import generate_bigrams

app = Flask(__name__, template_folder='Templates')

@app.route('/')
def index():
    result = None
    paragraph = None
    return render_template('index.html', result=result, paragraph=paragraph)

@app.route('/detect', methods=['POST'])
def detect_diword():
    if request.method == 'POST':
        # Ambil data paragraf
        paragraph = request.form.get('paragraph')

        # Detect di
        detector = DiWordDetector()
        result_di = detector.detect_di_usage(paragraph)

        # Detect terikat
        # Baca file txt sebagai kata dasar
        with open('Models/deteksi_terikat/kata-dasar.txt', 'r') as file:
            word_list = [line.strip() for line in file.readlines()]
        
        # Preprocessing
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

        if (deteksi_bigram_terikat != []):
            result_terikat_dict.update(validateDuaKata(deteksi_bigram_terikat, word_list, paragraph))

        # Jika tidak ada kata terikat
        if result_terikat_dict == {}:
            result_terikat_dict = {'errormessage' : "Tidak ada kata terikat yang ditemukan"}

        return render_template('index.html', result=[result_di, result_terikat_dict], paragraph=paragraph)
    

    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)