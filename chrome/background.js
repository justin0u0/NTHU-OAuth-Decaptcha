const decaptcha = async(maxRetries = 10) => {
	for (let i = 0; i < maxRetries; ++i) {
		if (typeof tf === 'undefined') {
			await new Promise(resolve => setTimeout(resolve, 100));
		}
	}

	const model = await tf.loadLayersModel(chrome.runtime.getURL('/model/model.json'));
	const imageElement = document.getElementById('captcha_image');

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

	const captchaCode = tensors.map(tensor => {
		const [predictions] = tensor.arraySync();
		let maxIndex = 0;
		let maxValue = 0;

		for (let i = 0; i < 10; ++i) {
			if (predictions[i] > maxValue) {
				maxIndex = i;
				maxValue = predictions[i];
			}
		}

		return `${maxIndex}`;
	}).join('');

	document.getElementById('captcha_code').value = captchaCode;
};

const requestFilter = {
	urls: [
		'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php*'
	]
};

// on every captcha request send, insert the captcha code automatically
// https://developer.chrome.com/docs/extensions/reference/webRequest/#event-onCompleted
chrome.webRequest.onCompleted.addListener(async(details) => {
	const injection = {
		func: decaptcha,
		target: {
			tabId: details.tabId
		}
	};

	await chrome.scripting.executeScript(injection);
}, requestFilter);
