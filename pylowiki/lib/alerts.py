# -*- coding: utf-8 -*-
import logging, smtplib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylowiki.model import Thing

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.pmember      as pmemberLib
import pylowiki.lib.mail            as mailLib

log = logging.getLogger(__name__)

# we will continue to compactify this function over time...
def emailAlerts(thing):
    # a kludge for comments
    if hasattr(thing, 'c'):
        newThing = thisComment = Thing('comment', thing.c.owner)
        for key in thing.c.keys():
            newThing[key] = thing.c[key]
        thing = newThing
        
    if 'workshopCode' in thing:
        codes = ['resourceCode', 'ideaCode', 'discussionCode']
        fromEmail = 'Civinomics Alerts <alerts@civinomics.com>'
        emailDir = config['app_conf']['emailDirectory']
        myURL = config['app_conf']['site_base_url']
        
        workshop = workshopLib.getWorkshopByCode(thing['workshopCode'])
        workshopURL = '%s/workshop/%s/%s'%(myURL, workshop['urlCode'], workshop['url'])
        workshopName = workshop['title']
        newThing = thing.objType
        thingUser = userLib.getUserByID(thing.owner)
        thingOwner = thingUser['name']
        
        facilitators = facilitatorLib.getFacilitatorsByWorkshop(workshop)
        followers = followLib.getWorkshopFollowers(workshop)
        listeners = listenerLib.getListenersForWorkshop(workshop)
        pmembers = pmemberLib.getPrivateMembers(workshop['urlCode'])
        
        if thing.objType == 'comment':
            parentCodeList = [i for i in codes if i in thing.keys()]
            parentCodeField = parentCodeList[0]
            parentCode = thing[parentCodeField]
            parent = generic.getThing(parentCode)
            thingURL = '%s/%s/%s/%s?comment=%s'%(workshopURL, parent.objType, parent['urlCode'], parent['url'], thing['urlCode'])
            log.info(thingURL)
        elif thing.objType == 'flag':
            if 'commentCode' in thing:
                comment = generic.getThing(thing['commentCode'])
                parentCodeList = [i for i in codes if i in comment.keys()]
                parentCodeField = parentCodeList[0]
                parentCode = comment[parentCodeField]
                parent = generic.getThing(parentCode)
                thingURL = '%s/%s/%s/%s?comment=%s'%(workshopURL, parent.objType, parent['urlCode'], parent['url'], comment['urlCode'])
            else:
                parentCodeList = [i for i in codes if i in thing.keys()]
                parentCodeField = parentCodeList[0]
                parentCode = thing[parentCodeField]
                parent = generic.getThing(parentCode)
                thingURL = '%s/%s/%s/%s'%(workshopURL, parent.objType, parent['urlCode'], parent['url'])
        else:
            thingURL = '%s/%s/%s/%s'%(workshopURL, thing.objType, thing['urlCode'], thing['url'])
                
                
        # do facilitators first
        if thing.objType == 'flag':
            subject = 'Civinomics Alert: New Flag in workshop "%s"'%workshopName
            thingURL = workshopURL + '/preferences'
            newThing = 'flagged item'
            txtFile = emailDir + "/facilitatorFlagAlert.txt"
        else:
            subject = 'Civinomics Alert: New Item in workshop "%s"'%workshopName
            txtFile = emailDir + "/facilitatorItemAlert.txt"
    
        # open and read the text file
        fp = open(txtFile, 'r')
        textMessage = fp.read()
        fp.close()
         
        viewMessage = "To view the new " +  newThing
        if workshop['public_private'] == 'public':
            viewMessage += ", use your browser to view it here:\n"
        else:
            viewMessage += ", use your browser to login to Civinomics and view it here:\n"
            
        viewMessage += thingURL
            
        # do the substitutions
        textMessage = textMessage.replace('${c.viewMessage}', viewMessage)
        textMessage = textMessage.replace('${c.thingType}', newThing)
        textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
        textMessage = textMessage.replace('${c.workshopURL}', workshopURL)
        textMessage = textMessage.replace('${c.workshopName}', workshopName)
        textMessage = textMessage.replace('${c.thingURL}', thingURL)
        for facilitator in facilitators:
            if ('flagAlerts' in facilitator and facilitator['flagAlerts'] == '1' and thing.objType == 'flag') or ('itemAlerts' in facilitator and facilitator['itemAlerts'] == '1'):
                facilitatorUser = userLib.getUserByID(facilitator.owner)
                # don't send emails if the facilitator created the object
                if thingUser != facilitatorUser:
                    toEmail = facilitatorUser['email']
      
                    mailLib.send(toEmail, fromEmail, subject, textMessage)

        # Flag alerts only go to facilitators
        if thing.objType != 'flag':
            txtFile = emailDir + "/memberItemAlert.txt"   
               
            # open and read the text file
            fp = open(txtFile, 'r')
            textMessage = fp.read()
            fp.close()
                
            # do the substitutions
            textMessage = textMessage.replace('${c.viewMessage}', viewMessage)
            textMessage = textMessage.replace('${c.thingType}', newThing)
            textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
            textMessage = textMessage.replace('${c.workshopURL}', workshopURL)
            textMessage = textMessage.replace('${c.workshopName}', workshopName)
            textMessage = textMessage.replace('${c.thingURL}', thingURL)
            
            subject = 'Civinomics Alert: New Item in bookmarked workshop "%s"'%workshopName
            for follower in followers:
                if 'itemAlerts' in follower and follower['itemAlerts'] == '1':
                    followerUser = userLib.getUserByID(follower.owner)
                    toEmail = followerUser['email']
                    
                    mailLib.send(toEmail, fromEmail, subject, textMessage)

            subject = 'Civinomics Listener Alert: New Item in workshop "%s"'%workshopName                
            for listener in listeners:
                if 'itemAlerts' in listener and listener['itemAlerts'] == '1':
                    listenerUser = userLib.getUserByCode(listener['userCode'])
                    toEmail = listenerUser['email']
  
                    mailLib.send(toEmail, fromEmail, subject, textMessage)
                    
            subject = 'Civinomics Alert: New Item in private workshop "%s"'%workshopName                
            for pmember in pmembers:
                if 'itemAlerts' in pmember and pmember['itemAlerts'] == '1':
                    pmemberUser = userLib.getUserByCode(pmember['userCode'])
                    toEmail = pmemberUser['email']
  
                    mailLib.send(toEmail, fromEmail, subject, textMessage)

            
                
                

                