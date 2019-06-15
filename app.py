from flask import Flask
from wordcloud import WordCloud,STOPWORDS
from flask import request, Response, render_template
import textract

@app.route('/')
def index():
    return 'hello'
