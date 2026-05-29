from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap 
from textblob import TextBlob, Word 
import random 
import time

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    start = time.time()

    if request.method == 'POST':
        rawtext = request.form['rawtext']

        blob = TextBlob(rawtext)

        blob_sentiment = blob.sentiment.polarity
        blob_subjectivity = blob.sentiment.subjectivity

        number_of_tokens = len(list(blob.words))

        # Extract nouns
        nouns = [word for word, tag in blob.tags if tag == 'NN']

        len_of_words = len(nouns)

        rand_words = random.sample(nouns, len(nouns)) if nouns else []

        final_word = [Word(item).pluralize() for item in rand_words]

        summary = final_word

        final_time = time.time() - start

        return render_template(
            'index.html',
            received_text=rawtext,
            number_of_tokens=number_of_tokens,
            blob_sentiment=blob_sentiment,
            blob_subjectivity=blob_subjectivity,
            summary=summary,
            final_time=final_time,
            len_of_words=len_of_words
        )

if __name__ == '__main__':
    app.run(debug=True)