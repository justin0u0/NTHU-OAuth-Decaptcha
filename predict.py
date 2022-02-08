from tensorflow import keras
from PIL import Image

import numpy as np
import argparse

model_path = "model/captcha_model_new_1.h5"

def test(image_path, model):
    img = Image.open(image_path)
    data = [np.array(img) / 255.0]
    data = np.stack(data)
    predictions = model.predict(data)
    ans = ""
    for i in range(4):
        ans += str(np.argmax(predictions[i][0]))
    print(ans)
    return img, ans

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="image path")
args = parser.parse_args()

CNN_model = keras.models.load_model(model_path)
test(args.data, CNN_model)
