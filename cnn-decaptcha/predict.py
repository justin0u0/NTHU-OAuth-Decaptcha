from tensorflow.keras.models import load_model, save_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image

import time
import numpy as np
import tensorflow_model_optimization as tfmot

model_path = "model/captcha_model_new_1.h5"
export_path = "model/pruned_model.h5"

def test(image_paths, model):
    data = []
    for pth in image_paths:
        data.append(img_to_array(load_img(pth)) / 255.0)
    data = np.stack(data)
    print(data.shape)
    start = time.time()
    predictions = model(data)
    ans = ""
    for j in range(3):
        for i in range(4):
            ans += str(np.argmax(predictions[i][j]))
        ans += ", "
    print(ans)
    end = time.time()
    print('time: ', end - start)
    return ans

CNN_model = load_model(model_path)
model_for_export = tfmot.sparsity.keras.strip_pruning(CNN_model)
save_model(model_for_export, export_path, include_optimizer=False)

pruned_model = load_model(export_path)

test_data = ["./data/demo/captcha-0.png", "./data/demo/captcha-1.png", "./data/demo/captcha-2.png"]

test(test_data, pruned_model)
