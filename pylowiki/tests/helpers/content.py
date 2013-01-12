# -*- coding: utf-8 -*-
from pylowiki.tests import *
"""contents.py is a file meant to act as a souce for simple and reliable content examples"""

def noChars():
	return ''

def oneWord(index=0):
	"""Simple function for returning a number of unique words."""
	if index < 0 or index > 5:
		index = 1
	samples = ['alpha',
		'beta', 
		'theta', 
		'dorita', 
		'quarto', 
		'cinque'
	]
	return samples[index]

def twoWords(index=0):
	"""Simple function for returning a number of unique word combos."""
	if index < 0 or index > 5:
		index = 1
	samples = ['alpha ab',
		'beta bet', 
		'theta tet', 
		'dorita dori', 
		'quarto qua', 
		'cinque chin'
	]

def oneLine(index=0):
	"""Simple function for returning a number of unique lines of standard characters."""
	if index < 0 or index > 5:
		index = 1
	samples = ['a group of characters',
		'another group of characters', 
		'something else', 
		'more unique text', 
		'a new piece of non-info', 
		'fifth indexed line of words'
	]
	return samples[index]

def twoLines():
	return """one line of words
	and another line of words"""

