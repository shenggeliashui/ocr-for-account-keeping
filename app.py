import os
from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    try:
        image = Image.open(io.BytesIO(image_bytes))
    except IOError:
        return jsonify({'error': 'Invalid image file'}), 400

    # 直接对图片进行OCR识别
    try:
        recognized_text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        # 将多行文本分割成列表
        recognized_lines = [line.strip() for line in recognized_text.split('\n') if line.strip()]
    except Exception as e:
        return jsonify({'error': 'OCR failed', 'details': str(e)}), 500

    return jsonify({'text': recognized_lines})

@app.route('/')
def health_check():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))