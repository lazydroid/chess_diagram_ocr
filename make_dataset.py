#!/usr/bin/env python
# encoding: utf-8
#
# create a dataset from the separate image files, resize pieces to SIZE x SIZE
#
import os, sys, cv2
import numpy as np
import json

import datetime

SIZE = 32

now = datetime.datetime.now()
suffix = now.strftime( '%Y-%m-%d_%H%M' )

result = []

if len(sys.argv) < 2 :
	sys.exit('Need an argument: ./make_dataset.py FOLDER')

for folder in sys.argv[1:] :
	r, d, files = os.walk(folder).next()
	for f in files :
		img = cv2.imread( os.path.join( r, f ), -1 )
#		img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
#		img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )	# ?
		#print img.shape

		if img.shape[0] > 32 :
			top = (img.shape[0] - 32) / 2
			img = img[top:top+32,:]
		if img.shape[1] > 32 :
			left = (img.shape[1] - 32) / 2
			img = img[left:left+32,:]
		if any(img.shape[:2] != (32,32)) :
			resized = cv2.resize( img, (SIZE,SIZE), interpolation = cv2.INTER_CUBIC)
		else :
			resized = img

		result.append( resized )

np.save( 'pieces_%d_%s.npy' % (SIZE, suffix), np.array( result, dtype='uint8'))

