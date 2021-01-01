#!/usr/bin/env python
# encoding: utf-8
#
# Assuming you have a book you want to check for the chess diagrams. Here are 3 steps:
#	1. convert the book into pages, every page is a .png file
#	2. use THIS script to extract the diagrams from the pages
#	3. use the recognizer to recognize the diagrams
#	4. profit!!! =)
#
# This script assumes you provide the path to the folder with .png pages of the book.
# Another assumption is that chess diagrams are printed with the black borders and
# there are no abundant vertical black lines besides the diagrams.
#
# Copyright (c) 2020, lenik terenin
#

# Python 2/3 compatibility
from __future__ import print_function
import sys

PY3 = sys.version_info[0] == 3

if PY3:
	xrange = range

import os, sys, cv2
import numpy as np
import json

import datetime

now = datetime.datetime.now()
suffix = now.strftime( '%Y-%m-%d_%H%M' )

def angle_cos(p0, p1, p2):
	'''
	calculate the angle between sides of the square to make sure it's close to 90 degrees
	'''
	d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
	return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
	'''
	looking for the squares in the image, filtering out everything that does not have 4 corners,
	then check for the angle between the sides (should be approximately 90 deg) and not rotated
	'''
	img = cv2.GaussianBlur(img, (5, 5), 0)
	squares = []
	for gray in cv2.split(img):
		for thrs in xrange(0, 255, 26):
			if thrs == 0:
				bin = cv2.Canny(gray, 0, 50, apertureSize=5)
				bin = cv2.dilate(bin, None)
			else:
				_retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
			contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			for cnt in contours:
				cnt_len = cv2.arcLength(cnt, True)
				cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
				# we need squares with 4 corners and bigger than 100x100 pixels large
				if len(cnt) == 4 and cv2.contourArea(cnt) > 10000 and cv2.isContourConvex(cnt):
					cnt = cnt.reshape(-1, 2)
					max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
					if max_cos < 0.1 :		# should be more or less upright (not rotated)
						if cnt[0][0] > 5 and cnt[0][1] > 5 :	# ignore the whole page outline
							squares.append(cnt)
	return squares

def make_tuples( arr ) :
	center_x = np.mean( [a[0] for a in arr] )
	center_y = np.mean( [a[1] for a in arr] )

	return tuple(tuple(a) for a in arr) + ( (center_x, center_y), )

def get_tlbr( arr ) :
	'''
	take a bunch of the square corners, find the top/left/bottom/right coords
	'''
	x = [a[0] for a in arr]
	y = [a[1] for a in arr]
	return ( (min(x), min(y)), (max(x), max(y)) )

def within10pix( a, b ) :
	'''
	make sure these points are within 10pixels: likely the same diagram
	'''
	return max( abs(a[0] - b[0]), abs(a[1] - b[1]) ) < 10

def sort_and_join_squares( squares ) :
	'''
	findCountours() produces hundreds of possible squares, so here we have to
	make it into a fewer, probably maximum 6 on the page.
	'''
	print( len(squares) )
	squares = [make_tuples(sq) for sq in squares]

	# remove the exact duplicates
	squares = list(set(squares))
	print( len(squares) )

	# sort by the middle point of the square, favouring Y direction over X
	squares = sorted(squares, key=lambda x : x[4][0]/3 + x[4][1])
	for sq in squares :
		print( sq )

	out = []
	while len(squares) :
		marked = []
		for sq in squares :
			# bundle together the contours that are within 10pixels area
			if within10pix( sq[4], squares[0][4] ) :
				marked.append( sq )

		for m in marked :
			squares.remove( m )

		# now calculate the TLBR for all bundled squares
		out.append( get_tlbr( [p for sq in marked for p in sq] ))

	print( len(out) )
	for sq in out :
		print( sq )

	return out

def save_board( page_num, num, board ) :
	'''
	create a file name from page number, diagram number and saves the board
	'''
	folder = 'boards_%s' % suffix
	if not os.path.isdir(folder) :
		os.mkdir( folder )
	name = os.path.join( folder, 'page_%03d_board_%d.png' % (page_num, num))
	print( 'saving board', name )
	cv2.imwrite( name, board )

def main() :
	if len(sys.argv) < 2 :
		sys.exit('Need an argument: ./diagram_extractor.py FOLDER')

	pages = sys.argv[1]
	if not os.path.isdir(pages) :
		sys.exit('Not a folder or does not exist: ' + folder)

	r, d, files = os.walk(pages).next()
	for f in files :
		#f = 'dee3ed3205b763ac0ad29cf218b93810-120.png'
		#f = '4e53bead1775de509de92091ab72a583-57.png'
		print( f )
		name = os.path.join( r, f )

		page_num = int(f.split('-')[1].split('.')[0])

		img = cv2.imread( name )
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		squares = find_squares(img)
		cv2.drawContours( img, squares, -1, (0, 255, 0), 1 )

		squares = sort_and_join_squares( squares )

		for num,sq in enumerate(squares) :
			(left, top), (right, bottom) = sq

			b = gray[top:bottom, left:right]

			save_board( page_num, num, b )

			#cv2.imshow( 'contours', b )
			#cv2.waitKey(0)

		cv2.imshow('squares', img)
		ch = cv2.waitKey() & 0xFF
		if ch == 27:
			break

		#break

if __name__ == '__main__':
	main()
	cv2.destroyAllWindows()

