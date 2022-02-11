from flask import Flask, request
from flask_cors import CORS
from tensorflow import keras
from PIL import Image

import numpy as np
import threading
import requests
import os

app = Flask(__name__)
CORS(app)

config = {
	'samples': 3
}

model = keras.models.load_model('./model/saved_model.h5')

base_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php'

def fetch_predict(captcha_id, session_id, i, result):
	fileurl = f'./temp/{captcha_id}-{session_id}-{i}.png'
	url = f'{base_url}?id={captcha_id}'

	with open(fileurl, 'wb') as f:
		cookies = {'PHPSESSID': session_id}

		f.write(requests.get(url, cookies=cookies).content)

	code = predict(fileurl)

	os.remove(fileurl)

	result[fileurl] = code

def predict(url):
	img = Image.open(url)
	data = np.stack([np.array(img) / 255.0])
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
