import os
from pylons import config

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
