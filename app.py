# app.py
import os
from flask import Flask, request, jsonify
import wikipediaapi
import pytesseract
from PIL import Image

app = Flask(__name__)

# Wikipedia API for retrieving text answers
wiki_wiki = wikipediaapi.Wikipedia('en')

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    question = data.get("question")
    
    # Simple Wikipedia lookup based on question
    if question:
        page = wiki_wiki.page(question)
        if page.exists():
            return jsonify({"answer": page.summary[:500] + '...'})
        else:
            return jsonify({"answer": "Sorry, I couldn't find an answer on Wikipedia."})
    return jsonify({"answer": "Please provide a question."})

# OCR feature for image-to-text (e.g., for scanned textbook questions)
@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    image = Image.open(file.stream)
    text = pytesseract.image_to_string(image)
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
