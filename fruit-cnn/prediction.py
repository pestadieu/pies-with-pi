from keras.models import load_model, Sequential
from PIL import Image
import numpy as np

img = Image.open("banana-7.jpg")
img = img.resize((100,100), Image.ANTIALIAS)
img = np.array(img).astype(np.uint8)
img = np.expand_dims(img, axis=0)

model = load_model("fruit_model.h5")
print(model.predict_classes(img))