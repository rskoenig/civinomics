# -*- coding: utf-8 -*-
from pylowiki.tests import *

def addIdea():
	return 'addIdea'

def addIdea_submit():
	return ''

def addComment():
	return 'commentAddHandler_root'

def addComment_text():
	return 'comment-textarea'

def addComment_submit():
	return 'reply'

def addIdea_text():
	return 'title'

def createWorkshop():
	return 'CreateWorkshop'

def createWorkshop_button():
	return 'CreateWorkshop'

def createWorkshop_FileUploadForm():
	return 'fileupload'

def createWorkshopForm1():
	return 'edit_issue'

def createWorkshopForm1_description():
	return 'description'

def createWorkshopForm1_goals():
	return 'goals'

def createWorkshopForm1_resources():
	return 'allowResources'

def createWorkshopForm1_suggestions():
	return 'allowSuggestions'

def createWorkshopForm1_title():
	return 'title'

def createWorkshopForm2():
	return 'private'

def createWorkshopForm2_submit():
	return 'continueToNext'

def createWorkshopForm3():
	return 'workshop_tags'

def createWorkshopForm4_continueToNext():
	return 'continueToNext'

def createWorkshopForm5_wikiBackground():
	return 'wikiBackground'

def createWorkshopForm5_wikiBackground_text():
	return 'textarea0'

def parameter_submit():
	return 'submit'

def personal_workshop_button_search():
	return 'Pers'

def professional_workshop_button_search():
	return 'Prof'

def submitNone():
	return None

def workshopSettings_allowIdeas(choice=True):
	"""Takes bool input and returns form-specific input value replacting the parameter's value."""
	if choice:
		return u'1'
	else:
		return u'0'

def workshopSettings_allowResourceLinks(choice=True):
	"""Takes bool input and returns form-specific input value replacting the parameter's value."""
	if choice:
		return u'1'
	else:
		return u'0'
