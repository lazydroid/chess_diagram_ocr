#!/usr/bin/env python
# encoding: utf-8
#

# Python 2/3 compatibility
from __future__ import print_function

import os, sys, cv2
import numpy as np
import json

import datetime

now = datetime.datetime.now()
suffix = now.strftime( '%Y-%m-%d_%H%M' )

def save_square( base, num, square ) :
	'''
	create a file name from base name and save the square
	'''
	folder = 'squares_%s' % suffix
	if not os.path.isdir(folder) :
		os.mkdir( folder )
	name = os.path.join( folder, '%s_board_%d.png' % (base, num))
	print( 'saving square', name )
	cv2.imwrite( name, square )

if __name__ == '__main__':
	if len(sys.argv) < 2 :
		sys.exit('Need an argument: ./board_splitter.py FOLDER')

	pages = sys.argv[1]
	if not os.path.isdir(pages) :
		sys.exit('Not a folder or does not exist: ' + folder)

	r, d, files = os.walk(pages).next()
	for f in files :
		#f = 'dee3ed3205b763ac0ad29cf218b93810-120.png'
		#f = '4e53bead1775de509de92091ab72a583-57.png'
		print( f )
		name = os.path.join( r, f )

		base = f.split('/')[-1].split('.')[0]

		img = cv2.imread( name )
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		offset = 5
		size_x = img.shape[0] - offset*2
		size_y = img.shape[1] - offset*2

		for i in range(9) :
			start_point = (0, offset + i*size_x / 8)
			end_point = (img.shape[1], offset + i*size_x / 8)
			cv2.line( img, start_point, end_point, (0, 255, 0), 1 )

			start_point = (offset + i*size_y / 8, 0)
			end_point = (offset + i*size_y / 8, img.shape[0])
			cv2.line( img, start_point, end_point, (0, 0, 255), 1 )


		for i in range(8) :
			for j in range(8) :
				left = offset + i*size_y/8
				right = offset + (i+1)*size_y/8
				top = offset + j*size_x/8
				bottom = offset + (j+1)*size_x/8
				square = gray[top:bottom, left:right]
				save_square( base, i*8+j, square )

		cv2.imshow('squares', cv2.pyrUp(img))
		ch = cv2.waitKey() & 0xFF
		if ch == 27:
			break

		#break

	cv2.destroyAllWindows()

