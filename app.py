from datetime import datetime
from wordcloud import WordCloud,STOPWORDS
from flask import Flask, request, Response, render_template
import textract

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
        text = textract.process(file.read())
        wordcloud = wc.generate(text)
        img = BytesIO()
        wordcloud.to_image().save(img, 'PNG')
        img.seek(0)
        return Response(img, mimetype='image/jpeg')
    return "error"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
