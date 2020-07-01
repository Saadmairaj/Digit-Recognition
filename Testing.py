# Testing purposes only.

import tensorflow as tf
import numpy as np
import cv2
import PIL.Image as Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import Dataset
import Model

def prepare( filepath ):
    Img_size = 28
    img_arr = cv2.imread( filepath, cv2.IMREAD_GRAYSCALE )
    img_arr = np.invert(img_arr)
    
    try:
        plt.imshow( img_arr, cmap="gray" )
        plt.show()
    except: 
        pass
    
    img_arr = cv2.resize( img_arr, (Img_size, Img_size) )
    
    return np.array(img_arr).reshape( -1, Img_size, Img_size, 1 )


model = tf.keras.models.load_model("Digit_Reader1.h5")

pre = model.predict([prepare("Yo.png")])
print(pre)

# print("\n\n",np.argmax(pre[0]), "\n\n")

# img = cv2.imread( "Yo.png", cv2.IMREAD_GRAYSCALE )
# img = np.invert( img )
# img = cv2.resize( img, (28, 28) )
# # img = img.reshape(28, 28, 1)

# label = 4
# Dataset.add(img, label)
# Model.Train_Digit()

