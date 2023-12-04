from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from Models.DiWordDetector import DiWordDetector

app = Flask(__name__, template_folder='Pages')

@app.route('/')
def index():
    # Redirect to the home page
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_diword():
    if request.method == 'POST':
        paragraph = request.form.get('paragraph')
        detector = DiWordDetector()
        result = detector.detect_di_usage(paragraph)
        return render_template('index.html', result=result, paragraph=paragraph)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)