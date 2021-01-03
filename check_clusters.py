#!/usr/bin/env python
# encoding: utf-8
#

import numpy as np
import pylab as Plot
import scipy.cluster	# kmean

import os, sys, json, time, datetime

import cv2

data = np.load( 'pieces_2021-01-02_1625.npy' )
validation_split = int(len(data)*0.8)
x_train = data[:validation_split]
x_test = data[validation_split:]

Y = np.loadtxt( 'tsne_Y_1000_2021-01-03_0454.txt' )
_, labels = scipy.cluster.vq.kmeans2( Y, 50 )

#Plot.scatter(Y[:,0], Y[:,1], 20, labels)
#Plot.show()

PATH = 'clusters'

if not os.path.isdir( PATH ) :
	os.mkdir( PATH )

clusters = sorted( list( set( list( labels ))))

for c in clusters :
	for i in range(len(Y)) :
		if labels[i] == c :
			name = os.path.join( PATH, 'cluster_%d_img_%d.png' % (int(c), i) )
			cv2.imwrite( name, x_test[i] )

