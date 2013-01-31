# -*- coding: utf-8 -*-
from pylowiki.tests import *
"""contents.py is a file meant to act as a souce for simple and reliable content examples"""

def activation_success():
    return 'Workshops'

def deleteObjectForm_findByCode(soup, ideaCode):
	"""expects a beautifulsoup page object, and the code of the idea to be deleted"""
	# find the form with regex for how these actions are formatted
	# <form action = 'delete/objectType/!' (object code == !)
	# action="/delete/idea/4ICv"
	# soup.find_all("form", action="/delete/idea/4ICv", limit=1)
	import re
	# return soup.find_all("form", re.compile("^delete\/*.?\/"+ideaCode), limit=1)
	# return soup.find_all("form", action=re.compile("/delete/"), limit=1)
	return soup.find("form", action=re.compile("/delete/.*?/"+ideaCode))
	# return soup.find_all("form", limit=1)

def getFormParts_soup(deleteForm):
    """expects a beautifulsoup form object, returns action, parameters"""
    formParts = {}
    #params = {}
    if deleteForm.name != 'form':
        return False
    # get the action of the form
    formParts['action'] = deleteForm.attrs['action']
    # normally, we'd need to get the input and submit values out somehow, 
    # but this form submits without any parameters
    #for child in deleteForm.children:
    #    if child.name == 'input':
    #        params[child.attrs['name']] = child.attrs['value']

    return formParts


def ideaTitleLink_getCode(ideaLink):
    # we want the object's code
    #/workshop/wsCode/wsName/objectType/OBJECTCODE/objectName
    urlParts = ideaLink.split('/')
    codeIndex = len(urlParts)-2
    thisCode = urlParts[codeIndex]
    return thisCode

def noChars():
	return ''

def oneLine(index=0):
	"""Simple function for returning a number of unique lines of standard characters."""
	if index < 0 or index > 5:
		index = 1
	samples = ['a group of characters',
		'1 new char set 1', 
		'2 new char set 2', 
		'3 new char set 3', 
		'4 new char set 4', 
		'5 new char set 5'
	]
	return samples[index]

def oneWord(index=0):
	"""Simple function for returning a number of unique words."""
	if index < 0 or index > 5:
		index = 1
	samples = ['alpha',
		'ONE', 
		'TWO', 
		'THREE', 
		'FOUR', 
		'FIVE'
	]
	return samples[index]

def twoLines():
	return """one line of words
	and another line of words"""

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

