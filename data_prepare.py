from PIL import Image

import pandas as pd
import numpy as np
import pickle

def get_data(path):
  print("Process " + path.split('/')[-1] + " data!")
  data = []
  for id, row in enumerate(df["image"]):
    if (id % 100 == 0):
      print(id)
    data.append(np.array(Image.open(path + "/" + row)) / 255.0)
  data = np.stack(data)
  return data

def get_test_label(path):
  df = pd.read_csv(path + "/label.csv", names=["image", "code"], header=None)
  # get label
  label = []
  for i in range(df.shape[0]):
    num = df["code"][i]
    code = np.array([int(v) for v in list(str(num).zfill(4))])
    label.append(code)
  return label
  
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

def main():
    PATH = "/content/drive/MyDrive/Colab Notebooks/ML CAPTCHA/data/" # change to your data path
    
    train_data, train_label = get_data(PATH + "train")
    valid_data, valid_label = get_data(PATH + "validate")
    test_data, test_label = get_data(PATH + "test")
    train_label = get_label(PATH + "train")
    valid_label = get_label(PATH + "validate")
    test_label = get_label(PATH + "test")

    print(train_data.shape)
    print(valid_data.shape)
    print(test_data.shape)
    print(len(train_label), train_label[0].shape)
    print(len(valid_label), valid_label[0].shape)
    print(len(test_label), test_label[0].shape)

    np.save(PATH + "train_19600.npy", train_data)
    np.save(PATH + "validate_5600.npy", valid_data)
    np.save(PATH + "test_2800.npy", test_data)

    with open(PATH + "train_label.pkl", "wb") as fp:   #Pickling
        pickle.dump(train_label, fp)
    with open(PATH + "valid_label.pkl", "wb") as fp:   #Pickling
        pickle.dump(valid_label, fp)
    with open(PATH + "test_label.pkl", "wb") as fp:   #Pickling
        pickle.dump(test_label, fp)

if __name__ == '__main__':
    main()
