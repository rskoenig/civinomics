from pylons import tmpl_context as c, config, session
from pylowiki.model import Thing, meta, Data

import time, datetime
import logging
from pylowiki.lib.mail import send
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def sendAbuseReport(problemType, alreadyFlagged, offendingUser, startTime, problem, reporterName, reporterEmail):
    subject = reporterName + ' is reporting a violation of Civinomics policy'
    recipient = 'help@civinomics.com'

    if 'user' in session:
      userName = c.authuser['name']
      userEmail = c.authuser['email']
      loggedIn = ''
    else:
      userName = "Not Logged In"
      userEmail = "Not Logged In"
      loggedIn = 'NOT'


    emailDir = config['app_conf']['emailDirectory']
   # imageDir = config['app_conf']['imageDirectory']
   # myURL = config['app_conf']['site_base_url']
    
    htmlFile = emailDir + "/abuseReport.html"
    txtFile = emailDir + "/abuseReport.txt"
    # headerImage = imageDir + "/email_logo.png"
    
    # open and read in HTML file
    fp = open(htmlFile, 'r')
    htmlMessage = fp.read()
    fp.close()
    
    # do the substitutions
    htmlMessage = htmlMessage.replace('${c.reporterName}', reporterName)
    htmlMessage = htmlMessage.replace('${c.reporterEmail}', reporterEmail)
    htmlMessage = htmlMessage.replace('${c.problemType}', problemType)
    htmlMessage = htmlMessage.replace('${c.alreadyFlagged}', alreadyFlagged)
    htmlMessage = htmlMessage.replace('${c.offendingUser}', offendingUser)
    htmlMessage = htmlMessage.replace('${c.startTime}', startTime)
    htmlMessage = htmlMessage.replace('${c.problem}', problem)
    htmlMessage = htmlMessage.replace('${c.userName}', userName)
    htmlMessage = htmlMessage.replace('${c.userEmail}', userEmail)
    htmlMessage = htmlMessage.replace('${c.loggedIn}', loggedIn)

    htmlMessage = htmlMessage.replace('${c.imageSrc}', 'cid:civinomicslogo')
    
    # open and read the text file
    fp = open(txtFile, 'r')
    textMessage = fp.read()
    fp.close()
    
    # do the substitutions
    textMessage = textMessage.replace('${c.reporterName}', reporterName)
    textMessage = textMessage.replace('${c.reporterEmail}', reporterEmail)
    textMessage = textMessage.replace('${c.problemType}', problemType)
    textMessage = textMessage.replace('${c.alreadyFlagged}', alreadyFlagged)
    textMessage = textMessage.replace('${c.offendingUser}', offendingUser)
    textMessage = textMessage.replace('${c.startTime}', startTime)
    textMessage = textMessage.replace('${c.problem}', problem)
    textMessage = textMessage.replace('${c.userName}', userName)
    textMessage = textMessage.replace('${c.userEmail}', userEmail)
    textMessage = textMessage.replace('${c.loggedIn}', loggedIn)

  
    # open and read in the image
    #fp = open(headerImage, 'rb')
    #logo = fp.read()
    #fp.close()
       
    # create a MIME email object, initialize the header info
    email = MIMEMultipart(_subtype='related')
    email['Subject'] = 'html test subject'
    email['From'] = 'help@civinomics.com'
    email['To'] = 'help@civinomics.com'
    
    # now attatch the text and html and picture parts
    part1 = MIMEText(textMessage, 'plain')
    #part2 = MIMEText(htmlMessage, 'html')
    #part3 = MIMEImage(logo, 'png')
    #part3.add_header('Content-Id', '<civinomicslogo>')
    email.attach(part1)
    #email.attach(part2)
    #email.attach(part3)
    
    # send that suckah
    send( 'help@civinomics.com', 'help@civinomics.com', subject, textMessage)