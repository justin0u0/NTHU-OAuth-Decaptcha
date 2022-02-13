from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard

import pandas as pd
import numpy as np
import pickle

def create_CNN():
  print("Creating CNN model...")
  input = Input((80, 150, 3))
  out = input
  out = Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu')(out)
  out = Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(out)
  out = BatchNormalization()(out)
  out = MaxPooling2D(pool_size=(2, 2))(out)
  out = Dropout(0.3)(out)
  out = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(out)
  out = Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(out)
  out = BatchNormalization()(out)
  out = MaxPooling2D(pool_size=(2, 2))(out)
  out = Dropout(0.3)(out)
  out = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu')(out)
  out = Conv2D(filters=128, kernel_size=(3, 3), activation='relu')(out)
  out = BatchNormalization()(out)
  out = MaxPooling2D(pool_size=(2, 2))(out)
  out = Dropout(0.3)(out)
  out = Conv2D(filters=256, kernel_size=(3, 3), activation='relu')(out)
  out = BatchNormalization()(out)
  out = MaxPooling2D(pool_size=(2, 2))(out)
  out = Flatten()(out)
  out = Dropout(0.3)(out)
  # out = Dense(10, name='digit', activation='softmax')(out)
  out = [Dense(10, name='digit1', activation='softmax')(out), 
         Dense(10, name='digit2', activation='softmax')(out), 
         Dense(10, name='digit3', activation='softmax')(out), 
         Dense(10, name='digit4', activation='softmax')(out)]
  print(out)
  model = keras.models.Model(inputs=input, outputs=out)
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  model.summary()
  return model

def get_label(path):
  print("Process " + path.split('/')[-1] + " label!")
  df = pd.read_csv(path + "/label.csv", names=["image", "code"], header=None)
  # get label
  read_label = []
  label = [[] for _ in range(4)]
  for i in range(df.shape[0]):
    num = df["code"][i]
    code = np.array([[int(v) for v in list(str(num).zfill(4))]]).reshape(-1)
    one_hot_code = np.eye(10)[code]
    read_label.append(one_hot_code)
  for arr in read_label:
    for i in range(4):
      label[i].append(arr[i])
  label = [arr for arr in np.asarray(label)] # 最後要把6個numpy array 放在一個list
  return label

# load date
test_data = np.load("data/test/test_2800.npy")
test_label = pickle.load(open("./data/test/test_label.pkl", "rb"))

# load model
CNN_model = create_CNN()
model_path = "model/captcha_model_new_1.h5"
CNN_model = keras.models.load_model(model_path)

predictions = CNN_model.predict(test_data)
total = predictions[0].shape[0]

print("Test label")
print("shape: ", end='')
print(len(test_label), test_label[0].shape)
print(test_label[0][0])
print(predictions[0][0])

correct_digit = [0 for _ in range(4)]
for i in range(total):
  for j in range(4):
    if np.argmax(predictions[j][i]) == test_label[i][j]:
      correct_digit[j] += 1
for j in range(4):
  print("digit{:d} acc:{:.4f}%".format(j+1, correct_digit[j]/total*100))
