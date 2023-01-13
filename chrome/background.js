
const decaptcha = async() => {
	const model = await tf.loadLayersModel('https://raw.githubusercontent.com/justin0u0/NTHU-OAuth-Decaptcha/master/cnn-decaptcha/model/tensorflowjs/model.json');

	const imageElement = document.getElementById('captcha_image');

	let captchaCode = '';

	try {
		const imageTensor = tf.browser.fromPixels(imageElement);
		const imageArray = imageTensor.arraySync();
		for (const row of imageArray) {
			for (const pixel of row) {
				pixel[0] /= 255.0;
				pixel[1] /= 255.0;
				pixel[2] /= 255.0;
			}
		}

		const expandedImageTensor = tf.expandDims(tf.tensor(imageArray), 0);

		const tensors = model.predict(expandedImageTensor);
		for (const tensor of tensors) {
			const [predictions] = tensor.arraySync();
			if (predictions.length !== 10) {
				return;
			}

			let maxIndex = 0;
			let maxValue = 0;

			for (let i = 0; i < 10; ++i) {
				if (predictions[i] > maxValue) {
					maxIndex = i;
					maxValue = predictions[i];
				}
			}

			captchaCode += `${maxIndex}`;
		}
	} catch (err) {
		console.log('err', err);
	}

	document.getElementById('captcha_code').value = captchaCode;
};

const requestFilter = {
	urls: [
		'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php*'
	]
};

// on every captcha request send, insert the captcha code automatically
// https://developer.chrome.com/docs/extensions/reference/webRequest/#event-onBeforeSendHeaders
chrome.webRequest.onBeforeSendHeaders.addListener(async(details) => {
	await chrome.scripting.executeScript({
		target: {
			tabId: details.tabId
		},
		files: ['./js/tfjs-core.min.js', './js/tfjs-backend-webgl.min.js', './js/tfjs-layers.min.js'],
	});

	const injection = {
		func: decaptcha,
		args: [],
		target: {
			tabId: details.tabId
		}
	};

	await chrome.scripting.executeScript(injection);
}, requestFilter, ['requestHeaders', 'extraHeaders']);

const urlFilter = {
	urls: [
		{ urlPrefix: 'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php' }
	]
};

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
	console.log('webNavigation.onBeforeNavigate', details);
	// workaround to activate service worker
}, urlFilter);
