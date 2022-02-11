from flask import Flask, request
from tensorflow import keras
from PIL import Image

import numpy as np
import threading
import requests
import os

app = Flask(__name__)

config = {
	'samples': 9
}

model = keras.models.load_model('./model/saved_model.h5')

base_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php'

def fetch_predict(captchaId, sessionId, i, result):
	fileurl = f'./temp/{captchaId}-{sessionId}-{i}.png'
	url = f'{base_url}?id={captchaId}'

	with open(fileurl, 'wb') as f:
		cookies = {'PHPSESSID': sessionId}

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
	captchaId = request.args.get('captchaId')
	sessionId = request.args.get('sessionId')

	result = {}
	threads = []
	for i in range(config['samples']):
		threads.append(threading.Thread(target = fetch_predict, args = (captchaId, sessionId, i, result)))
		threads[i].start()
	
	for i in range(config['samples']):
		threads[i].join()

	code = ''
	for i in range(4):
		code += str(np.bincount([result[k][i] for k in result]).argmax())

	return {'code': code}
