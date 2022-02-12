from flask import Flask, request
from flask_cors import CORS
from tensorflow import keras
from PIL import Image
from io import BytesIO

import numpy as np
import threading
import requests

app = Flask(__name__)
CORS(app)

config = {
	'samples': 3
}

model = keras.models.load_model('./model/saved_model.h5')

base_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php'

def fetch_predict(captcha_id, session_id, i, result):
	url = f'{base_url}?id={captcha_id}'
	cookies = {'PHPSESSID': session_id}

	resp = requests.get(url, cookies=cookies)

	code = predict(resp.content)

	result[str(i)] = code

def predict(image_bytes):
	image = Image.open(BytesIO(image_bytes))
	data = np.stack([np.array(image) / 255.0])
	predictions = model.predict(data)

	code = [np.argmax(predictions[i][0]) for i in range(4)]

	return code

@app.route('/')
def healthz():
	return {'status': 'ok'}

@app.route('/decaptcha')
def decaptcha():
	captcha_id = request.args.get('captchaId')
	session_id = request.args.get('sessionId')

	result = {}
	threads = []
	for i in range(config['samples']):
		threads.append(threading.Thread(target = fetch_predict, args = (captcha_id, session_id, i, result)))
		threads[i].start()
	
	for i in range(config['samples']):
		threads[i].join()

	code = ''
	for i in range(4):
		code += str(np.bincount([result[k][i] for k in result]).argmax())

	return {'code': code}

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
