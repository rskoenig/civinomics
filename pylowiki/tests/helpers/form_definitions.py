# -*- coding: utf-8 -*-
from pylowiki.tests import *

def addComment():
    return 'commentAddHandler_root'

def addComment_text():
    return 'comment-textarea'

def addComment_submit():
    return 'reply'

def addConversation():
    return 'addDiscussion'

def addConversation_text():
    return 'text'

def addConversation_title():
    return 'title'

def addIdea():
    return 'addIdea'

def addIdea_submit():
    return ''

def editIdea_submit():
    return 'reply'

def addIdea_text():
    return 'title'

def createWorkshop_1_form():
    return 'CreateWorkshop'

def create_workshop_1_personal_professional(kwargs=None):
    #: value of button for creating a personal or professional workshop
    #: can return value for choosing personal or professional workshops
    if kwargs != None:
        if 'personal' in kwargs:
            if 'personal' == True:
                return 'createPersonal'
            else:
                #: if we get selenium to drive this test,
                #: we will be able to use the javascript for actually processing the payment form.
                #: For now, we'll need to create a personal workshop but manually set it as professional
                #: return 'createProfessional'
                return 'createPersonal'
        else:
            return 'createPersonal'
    else:
        return 'createPersonal'

def createWorkshop_paymentForm():
    return 'paymentForm'

def create_workshop_paymentToken():
    return 'stripeToken'

def create_workshop_paymentToken_val():
    return 'tok_19tVR0n1Mz7qua'

def createWorkshop_button():
    return 'CreateWorkshop'

def createWorkshop_FileUploadForm():
    return 'fileupload'

def createWorkshop_2_Basics():
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

def createWorkshopForm2(private=True):
    if private:
        return 'private'
    else:
        return 'scope'

def createWorkshopForm2_submit():
    return 'continueToNext'

def createWorkshopForm3():
    return 'workshop_tags'

def createWorkshopForm4_continueToNext():
    return 'continueToNext'

def createWorkshopForm5_wikiBackground():
    return 'workshop_background'

def createWorkshopForm5_wikiBackground_text():
    return 'data'

def createWorkshopForm5_wikiBackground_submit():
    return ''

def editComment_submit():
    return 'reply'

def login_email():
    return 'email'

def login_homePage():
    return 'sign_in'

def login_password():
    return 'password'

def parameter_submit():
    return 'submit'

def paymentForm():
    return 'paymentForm'

def paymentFormAdminUpgrade():
    return 'adminUpgradeForm'

def paymentFormAdminUpgradeSubmitName():
    return 'admin-submit-button'

def submitNone():
    return None

def upgradeWorkshop():
    return 'workshopUpgrade'

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

def workshopSettings_privateForm():
    return u'private'

def workshopSettings_privateForm_addMemberField():
    return u'addMember'

def workshopSettings_privateForm_invite():
    return u'newMember'

# looks like this input field is no longer used
#def workshopSettings_privateForm_sendInviteMsg():
#    return u'sendInvite'


