#!/usr/bin/env python
#
# Generate a board based on FEN to check the fonts
#

import sys, os, StringIO, urllib, hashlib, base64, re
import logging, random, traceback, urllib2, gzip

from PIL import Image, ImageDraw, ImageFont	#, ImageOps

font_names = { 'alpha2' : 'ChessAlpha2.ttf' }

def fen2board( fen ) :	# returns 64-char long array with chess pieces
	fen = ''.join( [f for f in fen if f.lower() in '12345678qkbnrp/'] )
	for num in range(9) :
		fen = fen.replace(str(num),' ' * num)
	#if len(fen) != 71 :
	#	print 'invalid fen length', len(fen)
	chunks = fen.split('/')
	#print chunks

	return ''.join([(c + '        ')[:8] for c in chunks[-8:]]) + ' '*64

def make_board_image( board, options ) :
	font_size = 24
	font_name = 'ChessAlpha2.ttf'
	white, black = 0xC0, 0xE0	# character code base
	pieces = { 'r' : 4, 'n' : 2, 'b' : 0, 'q' : 6, 'k' : 8, 'p' : 10 }

	single = double = coordinates = False
	for o in options :
		try :
			font_size = int(o)
		except :
			pass
		if o.lower() in font_names :
			font_name = font_names[o.lower()]
		if o.lower() == 'single' :
			single = True
		if o.lower() == 'double' :
			double = True
		if o.lower().startswith( 'coord' ) :
			coordinates = True

	border = False
	if single :
		border = True
		if coordinates :
			border_set = [
				'\xF9','\xFA', '\xFB', '\xD8\xD7\xD6\xD5\xD4\xD3\xD2\xD1',
				'\xCC', '\xD9', '\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8', '\xDB'
			]
		else :
			border_set = [
				'\xF9','\xFA', '\xFB', '\xCD',
				'\xCC', '\xD9', '\xDA', '\xDB'
			]

	if double :
		border = True
		if coordinates :
			border_set = ['[','z',']','*&^%$\xA3"\xAC', '\\', '{', 'ABCDEFGH', '}' ]
		else :
			border_set = ['[','z',']','|', '\\', '{', 'y', '}' ]

	font_size = min( 128, max( 16, font_size ))

	SIZE = (font_size * (8 + border*2), font_size * (8 + border*2))
	im = Image.new( "L", SIZE, 255)
	draw = ImageDraw.ImageDraw( im )

	color = 0	#64
	font = ImageFont.truetype( font_name, font_size)

	if border :
		draw.text( (0,0), border_set[0], fill = color, font = font )
		draw.text( (font_size*9,0), border_set[2], fill = color, font = font )
		draw.text( (0,font_size*9), border_set[5], fill = color, font = font )
		draw.text( (font_size*9,font_size*9), border_set[7], fill = color, font = font )
		for i in range(8) :
			# upper
			draw.text( ((i+border)*font_size,0), border_set[1][i%len(border_set[1])], fill = color, font = font )
			draw.text( (0,(i+border)*font_size), border_set[3][i%len(border_set[3])], fill = color, font = font )
			draw.text( (font_size*9,(i+border)*font_size), border_set[4][i%len(border_set[4])], fill = color, font = font )
			draw.text( ((i+border)*font_size,font_size*9), border_set[6][i%len(border_set[6])], fill = color, font = font )

		#draw.text( (0,0), border_set[0], fill = color, font = font )
		#for j in range(8) :
		#	draw.text( (0,(j+border)*font_size), border_set[10+j], fill = color, font = font )

	for i in range(8) :
		for j in range(8) :
			filled = (i+j)&1
			piece = board[i*8+j]
			pos = ((j+border)*font_size, (i+border)*font_size-1)
			if piece == ' ' :
				if filled :
					draw.text( pos, '#', fill = color, font = font )
			else :
				code = pieces[piece.lower()] | (white if piece.isupper() else black) | filled
				draw.text( pos, chr(code), fill = color, font = font )
	return im

if __name__ == '__main__' :

	fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

	options = ''
	board = fen2board( fen )
	make_board_image( board, options ).save( 'board.png', format="png")

