import os
from flask import Flask, render_template, request
import csv
from docx import Document

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    acronym_file = request.files['acronym_file']
    csv_file = request.files['csv_file']

    #create temp directory if it does not exist
    if not os.path.exists("temp"):
        os.makedirs("temp")
    # Save the uploaded files to a temporary location
    acronym_file.save(os.path.join("temp", acronym_file.filename))
    csv_file.save(os.path.join("temp", csv_file.filename))

    # read the CSV file into a dictionary
    translations = {}
    with open(os.path.join("temp", csv_file.filename)) as f:
        reader = csv.DictReader(f)
        for row in reader:
            translations[row['acronym']] = row['abbreviation']

    # open the Word document
    document = Document(os.path.join("temp", acronym_file.filename))

    # replace acronyms in the document with their translations
    for para in document.paragraphs:
        for run in para.runs:
            for acronym, abbreviation in translations.items():
                run.text = run.text.replace(acronym, abbreviation)
    #save the modified document
    document.save(os.path.join("temp", acronym_file.filename))
    return "Translated Document saved as :"+ acronym_file.filename

if __name__ == '__main__':
    app.run(debug=True)
