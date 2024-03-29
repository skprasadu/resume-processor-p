import os
from wordcloud import WordCloud,STOPWORDS
from flask import Flask, request, Response, render_template
import textract
from werkzeug import secure_filename
from io import BytesIO

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
    
    wc = WordCloud(stopwords=new_stopwords, width=700, height=350)

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(filename)
        text = textract.process(filename)
        os.remove(filename)
        wordcloud = wc.generate(str(text))
        img = BytesIO()
        wordcloud.to_image().save(img, 'PNG')
        img.seek(0)
        return Response(img, mimetype='image/jpeg')
    return "error"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
