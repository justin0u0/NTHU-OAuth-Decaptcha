from tensorflow import keras
from PIL import Image
import numpy as np
from flask import Flask
import requests
import threading

app = Flask(__name__)

config = {
	'samples': 9
}

model = keras.models.load_model('./model/saved_model.h5')

base_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php'

def fetch_predict(captchaId, sessionId, i, result):
	url = f'{base_url}?id={captchaId}'

	with open(f'./temp/{captchaId}-{sessionId}-{i}.png', 'wb') as f:
		cookies = {'PHPSESSID': sessionId}

		f.write(requests.get(url, cookies=cookies).content)

	code = predict(url)

	result[url] = code

def predict(url):
	img = Image.open(url)
	data = np.stack(list(np.array(img) / 255.0))
	predictions = model.predict(data)

	code = [np.argmax(predictions[i][0]) for i in range(4)]

	return code

@app.route('/')
def healthz():
	return {'status': 'ok'}

@app.route('/decaptcha')
def decaptcha():
	captchaId = requests.args.get('captchaId')
	sessionId = requests.args.get('sessionId')

	result = {}
	threads = []
	for i in range(config['samples']):
		threads.append(threading.Thread(target = fetch_predict, args = (captchaId, sessionId, i, result)))
		threads[i].start()
	
	for i in range(config['samples']):
		threads[i].join()

	answer = []
	for i in range(4):
		answer.append(str(np.bitcount([result[k][0] for k in result]).argmax()))

	code = ''.join(answer)

	return {'code': code}
