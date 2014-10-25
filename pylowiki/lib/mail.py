import os
import logging
import pylowiki.lib.utils           as utils
from pylons import config, request

log = logging.getLogger(__name__)

def send( send_too, send_from, subject, message ):

    #SENDMAIL = "sendmail" #path to sendmail
    SENDMAIL = "/usr/sbin/sendmail" #path to sendmail
    BR = "\n" # BR types/reads easier

    sub_process = os.popen( "%s -t" % SENDMAIL, "w" )
    sub_process.write( "To: " + send_too + BR )
    sub_process.write( "From: " + send_from + BR )
    sub_process.write( "Subject: " + subject + BR )
    sub_process.write( BR ) #blank line seperates headers from body
    sub_process.write( message + BR )
    status = sub_process.close()
    return True

def sendWelcomeMail(u): 
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/welcome.txt"

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()

    subject = "Civinomics: let's get started!"
    fromEmail = config['activation.email']
    toEmail = u['email']
    
    send(toEmail, fromEmail, subject, textMessage)
    
       
def sendActivationMail(recipient, activationLink):
    subject = 'Civinomics Account Activation'
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/activate.txt"

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    # do the substitutions
    textMessage = textMessage.replace('${c.activationLink}', activationLink)

    fromEmail = config['activation.email']
    toEmail = recipient

    send(toEmail, fromEmail, subject, textMessage)
    
def sendActivationMailWithPassword(recipient, activationLink, password):
    subject = 'Civinomics Account Activation'
    

    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/activateWithPassword.txt"

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    textMessage = textMessage.replace('${c.activationLink}', activationLink)
    textMessage = textMessage.replace('${password}', password)
    
    fromEmail = config['activation.email']
    toEmail = recipient

    send(toEmail, fromEmail, subject, textMessage)

       
def sendPMemberInvite(workshopName, senderName, recipient, message, browseURL):
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/private_invite.txt"
    
    if 'paste.testing_variables' in request.environ:
            request.environ['paste.testing_variables']['browseUrl'] = browseURL
   
    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    # do the substitutions
    textMessage = textMessage.replace('${c.sender}', senderName)
    textMessage = textMessage.replace('${c.workshopName}', workshopName)
    textMessage = textMessage.replace('${c.inviteMessage}', message)
    textMessage = textMessage.replace('${c.browseLink}', browseURL)
    textMessage = textMessage.replace('${c.browseLink}', browseURL)
    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'
    toEmail = recipient
    subject = 'An invitation from ' + senderName

    send(toEmail, fromEmail, subject, textMessage)
    
def sendWorkshopMail(recipient):    
    emailDir = config['app_conf']['emailDirectory']
    myURL = config['app_conf']['site_base_url']

    txtFile = emailDir + "/workshop.txt"
    
    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()

    subject = 'About your new Civinomics workshop'
    fromEmail = 'Civinomics Helpdesk <helpdesk@civinomics.com>'
    toEmail = recipient

    send(toEmail, fromEmail, subject, textMessage)
    
def sendAccountMail(recipient):
           
    subject = 'Information about your new Civinomics Professional Workshop account'
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/account.txt"

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()

    fromEmail = 'Civinomics Billing <billing@civinomics.com>'

    send(recipient, fromEmail, subject, textMessage)

def sendCommentMail(recipient, sender, parent, dparent, text):
           
    subject = 'Civinomics Alert: A new comment has been added to one of your items'
    fromEmail = 'Civinomics Alerts <alerts@civinomics.com>'
    
    textMessage = sender['name'] + " has commented on your " + parent.objType.replace("Unpublished", "") 
    if parent.objType != 'comment':
        textMessage += ' "' + parent['title'] + '"'
    else:
        textMessage += '"' + parent['data'] + '"'
        
    if 'workshopCode' in parent:
        parentBase = "workshop"
        textMessage += ' in the ' + parentBase + ' titled "' + dparent['title'] + '"'

    textMessage += ': civ.io/' + parent.objType.replace("Unpublished", "") + '/' + parent['urlCode'] + '/' + parent['url']
    textMessage += '\n\n"' + text + '"\n\n'
    textMessage += "\n\nThis is an automated message. Your Civinomics profile preferences are set to email \nnotifications when someone comments on one of your items.\nTo change this, login to your Civinomics account, and go to the Preferences menu\nof your Edit Profile tab." 

    send(recipient, fromEmail, subject, textMessage)
    
def sendListenerInviteMail(recipient, user, workshop, memberMessage, numInvites):
           
    subject = 'You are invited to listen in on a Civinomics workshop'
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/invitelistener.txt"
    browseURL = config['app_conf']['site_base_url'] + "/workshop" + "/" + workshop['urlCode'] + "/" + workshop['url']
    if numInvites == '0':
        numInvitesMessage = ''
    else:
        numInvitesMessage = "\nThere are now %s members who've asked you to join in!\n"%numInvites

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    textMessage = textMessage.replace('${c.sender}', user['name'])
    textMessage = textMessage.replace('${c.workshop}', workshop['title'])
    textMessage = textMessage.replace('${c.browseLink}', browseURL)
    textMessage = textMessage.replace('${c.memberMessage}', memberMessage)
    textMessage = textMessage.replace('${c.numInvitesMessage}', numInvitesMessage)

    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'

    send(recipient, fromEmail, subject, textMessage)
    
def sendListenerAddMail(recipient, user, workshop):
           
    subject = 'You are invited to listen in on a Civinomics workshop'
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/addlistener.txt"
    browseURL = config['app_conf']['site_base_url'] + "/workshop" + "/" + workshop['urlCode'] + "/" + workshop['url']

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    textMessage = textMessage.replace('${c.sender}', user['name'])
    textMessage = textMessage.replace('${c.workshop}', workshop['title'])
    textMessage = textMessage.replace('${c.browseLink}', browseURL)

    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'

    send(recipient, fromEmail, subject, textMessage)
    
def sendNewListenerMail(listener):
           
    subject = 'You have been added as a Civinomics Listener'
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/newlistener.txt"
    scopeInfo = utils.getPublicScope(listener)
    listenerScope = scopeInfo['level'] + " of " + scopeInfo['name']
    
    # 0|0|united-states|0|0|0|0|0|0|0
    scopeList = listener['scope'].split('|')
    state = scopeList[4]
    county = scopeList[6]
    city = scopeList[8]
    
    browseURL = config['app_conf']['site_base_url'] + "/workshops/geo/earth/united-states"
    
    if state != '0' and state != '':
        browseURL += '/' + state
    if county != '0' and county != '':
        browseURL += '/' + county
    if city != '0' and city != '':
        browseURL += '/' + city


    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    textMessage = textMessage.replace('${c.listenerScope}', listenerScope)
    textMessage = textMessage.replace('${c.listenerName}', listener['name'])
    textMessage = textMessage.replace('${c.browseLink}', browseURL)

    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'

    send(listener['email'], fromEmail, subject, textMessage)
    
def sendShareMail(recipientEmail, memberMessage, user, item, itemURL):
           
    subject = '%s shared "%s" with you' % (user['name'], item['title'])
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/shareemail.txt"
    
    introduction = ""
    #itemDet = 'a'
    #if item.objType == 'idea':
    #    itemDet = 'an'
        
    introduction = "This %s is hosted on Civinomics:\n%s\n\n"%(item.objType, itemURL)

    #if item.objType == 'workshop':
    #   introduction += 'The workshop is titled "%s".'%item['title']
    #else:
    #    introduction += 'The %s is titled "%s" and is in a workshop titled "%s".'%(item.objType, item['title'], workshop['title'])

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    #textMessage = textMessage.replace('${c.sender}', user['name'])
    textMessage = textMessage.replace('${c.intro}', introduction)
    textMessage = textMessage.replace('${c.memberMessage}', memberMessage)

    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'

    send(recipientEmail, fromEmail, subject, textMessage)


def sendCoauthorAddMail(recipient, user, initiative):
    log.info('mail controller called')
           
    subject = '%s invited you to coauthor %s' % (user['name'], initiative['title'])
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/addCoauthor.txt"
    messagesURL = utils.getBaseUrl() + "/messages/" + recipient['urlCode'] + "/" + recipient['url']

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    textMessage = textMessage.replace('${c.sender}', user['name'])
    textMessage = textMessage.replace('${c.initiative}', initiative['title'])
    textMessage = textMessage.replace('${c.messagesLink}', messagesURL)

    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'

    send(recipient['email'], fromEmail, subject, textMessage)
