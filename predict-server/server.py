from flask import Flask, request
from flask_cors import CORS
from tensorflow import keras
from io import BytesIO
from PIL import Image

import numpy as np
import requests

app = Flask(__name__)
CORS(app)

config = {
	'samples': 3
}

model = keras.models.load_model('./model/saved_model.h5')

base_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php'

def fetch_predict(captcha_id, session_id):
	url = f'{base_url}?id={captcha_id}'
	cookies = {'PHPSESSID': session_id}

	image_bytes = []
	for _ in range(config['samples']):
		resp = requests.get(url, cookies=cookies)
		image_bytes.append(resp.content)

	return predict(image_bytes)

def predict(images_bytes):
	images_array = []
	for image_bytes in images_bytes:
		image = Image.open(BytesIO(image_bytes))
		images_array.append(np.array(image) / 255.0)

	data = np.stack(images_array)
	predictions = model.predict(data)
	
	codes = [[np.argmax(predictions[i][j]) for j in range(config['samples'])] for i in range(4)]

	return codes

@app.route('/')
def healthz():
	return {'status': 'ok'}

@app.route('/decaptcha')
def decaptcha():
	captcha_id = request.args.get('captchaId')
	session_id = request.args.get('sessionId')

	codes = fetch_predict(captcha_id, session_id)

	code = ''
	for i in range(4):
		code += str(np.bincount(codes[i]).argmax())

	return {'code': code}

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
