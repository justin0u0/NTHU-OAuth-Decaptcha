import tensorflowjs as tfjs
from tensorflow.keras.models import load_model, save_model

model = load_model("model/pruned_model.h5")
model.compile()
tfjs.converters.save_keras_model(model, "model/tensorflowjs")
