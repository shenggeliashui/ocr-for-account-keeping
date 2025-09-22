import os
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import io
from PIL import Image
import numpy as np

app = Flask(__name__)

# 初始化 PaddleOCR 引擎
# 第一次运行时会自动下载模型，可能需要一些时间
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

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

    # 将图片转换为 NumPy 数组，PaddleOCR 需要这种格式
    img_np = np.array(image)

    result = ocr.ocr(img_np, cls=True)

    if not result or not result[0]:
        return jsonify({'text': []})

    recognized_text = [item[1][0] for item in result[0]]

    # 返回提取的文字内容
    return jsonify({'text': recognized_text})


# 定义一个健康检查路由，Render 部署时需要
@app.route('/')
def health_check():
    return "OK"


if __name__ == '__main__':
    # 在本地运行时，使用 Flask 自带的服务器
    # Render 部署时会使用 Gunicorn 服务器
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))