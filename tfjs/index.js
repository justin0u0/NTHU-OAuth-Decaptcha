import * as tfjs from '@tensorflow/tfjs-node';
import * as fs from 'fs/promises';

(async() => {
	const model = await tfjs.loadLayersModel('https://raw.githubusercontent.com/justin0u0/NTHU-OAuth-Decaptcha/master/cnn-decaptcha/model/tensorflowjs/model.json');
	console.log('model:', model);

	const image = await fs.readFile('./assets/captcha.png');
	const imageTensor = tfjs.node.decodeImage(image);
	console.log('imageTensor', imageTensor);

	const expandedImageTensor = tfjs.expandDims(imageTensor, 0);
	console.log('expandedImageTensor', expandedImageTensor);

	const tensors = model.predict(expandedImageTensor);
	for (const tensor of tensors) {
		console.log(tensor.dataSync());
	}
})();
