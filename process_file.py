from PyPDF2 import PdfFileReader
from docx import Document
from io import BytesIO
from werkzeug import secure_filename
from subprocess import Popen, PIPE
import os
import requests

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


def getDocxText(stream):
    doc = Document(stream)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
