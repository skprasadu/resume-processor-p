from flask import Flask
from datetime import datetime
from wordcloud import WordCloud,STOPWORDS
from PyPDF2 import PdfFileReader
from docx import Document
from flask import request, Response, render_template
from io import BytesIO
from werkzeug import secure_filename
from subprocess import Popen, PIPE
import os
import requests

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
            txt = getDocText(file)            
        elif file.filename.endswith('docx'):
            txt = getDocxText(file.stream)
        elif file.filename.endswith('pdf'):
            txt = getPdfText(file)
        else:
            raise Exception("format not supported now")
    
    if txt.strip() != '':
        wordcloud = wc.generate(txt)
        img = BytesIO()
        wordcloud.to_image().save(img, 'PNG')
        img.seek(0)
        return Response(img, mimetype='image/jpeg')
    else:
        raise Exception("Empty text not supported")

def getDocxText(stream):
    doc = Document(stream)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getPdfText(file):
    stream = file.stream
    pdfReader = PdfFileReader(stream)
    count = pdfReader.numPages
    totalStr = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        totalStr +=  page.extractText()
        totalStr += '\n'
    if totalStr.strip() != '':
        return totalStr
    else:
        return getFromOCRestful(file)
        
    return ''
    
def getFromOCRestful(file):
    print(os.environ['OCRESTFUL_BASE_URL'])
    print(os.environ['OCRESTFUL_API_SECRET'])    
    
    return ''

def getDocText(file):
    filename = secure_filename(file.filename)
    file.save(filename)
    
    cmd = ['antiword', '-f', filename]
    try:
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        os.remove(filename)
        return stdout.decode('utf-8', 'ignore')
    except:
        return ''

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

