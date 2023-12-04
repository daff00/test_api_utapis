from flask import Flask, render_template, request, jsonify, send_from_directory
from Models.DiWordDetector import DiWordDetector

app = Flask(__name__, template_folder='Pages')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_diword():
    if request.method == 'POST':
        paragraph = request.form.get('paragraph')
        detector = DiWordDetector()
        result = detector.detect_di_usage(paragraph)
        return render_template('index.html', result=result, paragraph=paragraph)

if __name__ == '__main__':
    app.run(debug=True)