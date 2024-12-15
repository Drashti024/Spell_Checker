from flask import Flask, request, render_template
from textblob import TextBlob
import language_tool_python

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')


def spell_checker(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)


def grammar_checker(text):
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text


def improve_fluency(text):
    blob = TextBlob(text)
    sentences = blob.sentences
    improved_sentences = []
    for sentence in sentences:
        improved_sentence = sentence.correct()  # Correct spelling in each sentence
        improved_sentences.append(str(improved_sentence))
    improved_text = ' '.join(improved_sentences)  # Join corrected sentences
    return improved_text


def process_text(text):
    corrected_spelling = spell_checker(text)
    corrected_grammar = grammar_checker(corrected_spelling)
    improved_fluency = improve_fluency(corrected_grammar)
    return improved_fluency


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_text():
    text = request.form['text']
    if not text:
        return render_template('index.html', error="Please enter some text.")

    corrected_text = process_text(text)
    return render_template('result.html', original_text=text, corrected_text=corrected_text)


if __name__ == '__main__':
    app.run(debug=True)
