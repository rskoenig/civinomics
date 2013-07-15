import os
from pylons import config, request

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

def sendCommentMail(recipient, parent, workshop, text):
           
    subject = 'Civinomics Alert: A new comment has been added to one of your items'
    fromEmail = 'Civinomics Alerts <alerts@civinomics.com>'
    
    textMessage = "A new comment has been added to your " + parent.objType 
    if parent.objType != 'comment':
        textMessage += ' titled "' + parent['title'] + '"'
    else:
        textMessage += '"' + parent['data'] + '"'
    textMessage += ' in the workshop titled "' + workshop['title'] + '" \n\n"' + text + '"'

    textMessage += "\n\nThis is an automated message. Your Civinomics profile preferences are set to email \nnotifications when someone comments on one of your items.\nTo change this, login to your Civinomics account, and go to the Preferences menu\nof your Edit Profile tab." 

    send(recipient, fromEmail, subject, textMessage)
    
def sendListenerInviteMail(recipient, user, workshop, memberMessage):
           
    subject = 'You are invited to listen in on a Civinomics workshop'
    
    emailDir = config['app_conf']['emailDirectory']
    txtFile = emailDir + "/invitelistener.txt"
    browseURL = config['app_conf']['site_base_url'] + "/workshop" + "/" + workshop['urlCode'] + "/" + workshop['url']

    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    textMessage = textMessage.replace('${c.sender}', user['name'])
    textMessage = textMessage.replace('${c.workshop}', workshop['title'])
    textMessage = textMessage.replace('${c.browseLink}', browseURL)
    textMessage = textMessage.replace('${c.memberMessage}', memberMessage)

    fromEmail = 'Civinomics Invitations <invitations@civinomics.com>'

    send(recipient, fromEmail, subject, textMessage)
