from keybert import KeyBERT
from flask import Flask
"""
USING FLASK TO CREATE AN API FOR SIMPLE KEYWORD EXTRACTION
"""

app = Flask(__name__)

@app.route("/keybert/<string:text>")
def process(text=str):
    kw_model = KeyBERT('paraphrase-MiniLM-L6-v2')
    extracted_kw = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), top_n=2)

    return extracted_kw


if __name__ == "__main__":
    app.run(debug=True)