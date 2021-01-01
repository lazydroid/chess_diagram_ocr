#!/usr/bin/env python
#
# collect and output MNIST training images as one large image (64x64 of small images)
#

import numpy as np
import cv2

from tensorflow import keras

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print( 'x_train.shape', x_train.shape )

for num in range(10) :
	pics = x_train[y_train == num]
	print( 'digit', num, 'length', len(pics))

	img = np.hstack( [np.vstack( pics[i*64:(i+1)*64] ) for i in range(64)] )

	cv2.imwrite( '%d.png' % num, img )

'''
x_train.shape (60000, 28, 28)
digit 0 length 5923
digit 1 length 6742
digit 2 length 5958
digit 3 length 6131
digit 4 length 5842
digit 5 length 5421
digit 6 length 5918
digit 7 length 6265
digit 8 length 5851
digit 9 length 5949
'''
