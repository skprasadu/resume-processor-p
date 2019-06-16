from flask import Flask
from datetime import datetime
from wordcloud import WordCloud,STOPWORDS
from PyPDF2 import PdfFileReader
from docx import Document
from flask import request, Response, render_template
from io import BytesIO
import subprocess
from subprocess import run, PIPE
from werkzeug import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadResume', methods=['POST'])
def upload():
    stopwords= set(STOPWORDS)

    #append new words to the stopwords list
    new_words =open(r'./stop-words.txt').read().split()
    new_stopwords=stopwords.union(new_words)
    
    wc = WordCloud(stopwords=new_stopwords)

    file = request.files['file']
    if file:
        if file.filename.endswith('doc'):
            wordcloud = wc.generate(getDocText(file))
        else:
            if file.filename.endswith('docx'):
                wordcloud = wc.generate(getDocxText(file.stream))
            elif file.filename.endswith('pdf'):
                wordcloud = wc.generate(getPdfText(file.stream))
            else:
                return "format not supported now"

            img = BytesIO()
            wordcloud.to_image().save(img, 'PNG')
            img.seek(0)
            return Response(img, mimetype='image/jpeg')
    return "error"

def getDocxText(stream):
    doc = Document(stream)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getPdfText(stream):
    pdfReader = PdfFileReader(stream)
    count = pdfReader.numPages
    totalStr = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        totalStr +=  page.extractText()
        totalStr += ' '
    return totalStr

def getDocText(file):
    filename = secure_filename(file.filename)
    file.save(filename)
    
    p = run(['catdoc'], stdout=PIPE,
        input=filename)
    print(p.returncode)
    print(p.stdout)
    return p.stdout


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

