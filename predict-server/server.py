from flask import Flask, request
from flask_cors import CORS
from tensorflow import keras
from io import BytesIO
from PIL import Image

import numpy as np
import requests
import threading
# import time

app = Flask(__name__)
CORS(app)

config = {
	'samples': 3
}

model = keras.models.load_model('./model/saved_model.h5')

base_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php'

def fetch(captcha_id, session_id, images_array):
	url = f'{base_url}?id={captcha_id}'
	cookies = {'PHPSESSID': session_id}

	for _ in range(config['samples']):
		resp = requests.get(url, cookies=cookies)
		image = Image.open(BytesIO(resp.content))
		images_array.append(np.array(image) / 255.0)

def predict(images_array):
	data = np.stack(images_array)
	predictions = model(data)

	codes = [[np.argmax(predictions[i][j]) for j in range(config['samples'])] for i in range(4)]

	return codes

@app.route('/')
def healthz():
	return {'status': 'ok'}

@app.route('/decaptcha')
def decaptcha():
	# start = time.time()
	captcha_id = request.args.get('captchaId')
	session_id = request.args.get('sessionId')

	images_array = []
	threads = []
	for i in range(config['samples']):
		threads.append(threading.Thread(target = fetch, args = (captcha_id, session_id, images_array)))
		threads[i].start()

	for i in range(config['samples']):
		threads[i].join()
	
	# fetch_time_end = time.time()

	codes = predict(images_array)

	# predict_time = time.time()

	code = ''
	for i in range(4):
		code += str(np.bincount(codes[i]).argmax())

	# print('fetch time: {}'.format(fetch_time_end - start))
	# print('predict time: {}'.format(predict_time - fetch_time_end))
	# print('total time: {}'.format(time.time() - start))

	return {'code': code}

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
