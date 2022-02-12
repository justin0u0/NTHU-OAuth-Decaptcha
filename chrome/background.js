
const baseURL = 'https://nthu-oauth-decaptcha.herokuapp.com/decaptcha';

const parseCookie = (cookie) => cookie
	.split(';')
	.map((v) => v.split('='))
	.reduce((acc, v) => {
		acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
		return acc;
	}, {});

const predict = async(captchaId, sessionId) => {
	const resp = await fetch(`${baseURL}?captchaId=${captchaId}&sessionId=${sessionId}`)
		.then((res) => res.json());

	return resp.code;
};

const insertCode = (code) => {
	const captchaInput = document.getElementsByName('captcha')[0];
	captchaInput.value = code;
};

const requestFilter = {
	urls: [
		'https://oauth.ccxp.nthu.edu.tw/v1.1/captchaimg.php*'
	]
};

// on every captcha request send, insert the captcha code automatically
// https://developer.chrome.com/docs/extensions/reference/webRequest/#event-onBeforeSendHeaders
chrome.webRequest.onBeforeSendHeaders.addListener(async(details) => {
	if (!Array.isArray(details.requestHeaders)) {
		return;
	}

	const cookieFromHeader = details.requestHeaders.find((h) => h.name === 'Cookie');
	if (!cookieFromHeader) {
		return;
	}

	// get session id from cookie
	const cookie = parseCookie(cookieFromHeader.value);
	const sessionId = cookie['PHPSESSID'];

	// get captcha id from url
	const url = new URL(details.url);
	const params = new Proxy(new URLSearchParams(url.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
	const captchaId = params.id;

	// predict the captcha from server
	const code = await predict(captchaId, sessionId);

	// insert the captcha code into the form
	const injection = {
		func: insertCode,
		args: [code],
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
	// workaround to activate service worker
}, urlFilter);
