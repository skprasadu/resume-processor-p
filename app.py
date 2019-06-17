from flask import Flask
from flask import request, Response, render_template
from io import BytesIO
from wordcloud import WordCloud,STOPWORDS
from process_file import getDocText, getDocxText, getPdfText

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
            #print(txt)
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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

