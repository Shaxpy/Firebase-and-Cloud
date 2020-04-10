from tensorflow import keras
from tensorflow.keras import backend
import tensorflowjs as tfjs
mobileNet = keras.applications.mobilenet.MobileNet()
tfjs.converters.save_keras_model(mobileNet, '/home/shaxpy/Desktop')
