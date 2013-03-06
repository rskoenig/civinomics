# -*- coding: utf-8 -*-
import logging, smtplib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.follow       as followLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.pmember      as pmemberLib
import pylowiki.lib.mail            as mailLib

log = logging.getLogger(__name__)

# we will continue to compactify this function over time...
def emailAlerts(thing):
    if 'workshopCode' in thing:
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
                
        # do facilitators first
        if thing.objType == 'flag':
            subject = 'Alert: an item was flagged in your Civinomics workshop'
            thingURL = workshopURL + '/preferences'
            newThing = 'flagged item'
            txtFile = emailDir + "/facilitatorFlagAlert.txt"
        else:
            subject = 'Alert: New %s added to your Civinomics workshop'%newThing
            thingURL = '%s/%s/%s/%s'%(workshopURL, thing.objType, thing['urlCode'], thing['url'])
            txtFile = emailDir + "/facilitatorItemAlert.txt"
    
        # open and read the text file
        fp = open(txtFile, 'r')
        textMessage = fp.read()
        fp.close()
                
        # do the substitutions
        textMessage = textMessage.replace('${c.thingType}', newThing)
        textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
        textMessage = textMessage.replace('${c.workshopURL}', workshopURL)
        textMessage = textMessage.replace('${c.workshopName}', workshopName)
        textMessage = textMessage.replace('${c.thingURL}', thingURL)
        textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
        for facilitator in facilitators:
            if ('flagAlerts' in facilitator and facilitator['flagAlerts'] == '1' and thing.objType == 'flag') or ('itemAlerts' in facilitator and facilitator['itemAlerts'] == '1'):
                facilitatorUser = userLib.getUserByID(facilitator.owner)
                toEmail = facilitatorUser['email']
  
                mailLib.send(toEmail, fromEmail, subject, textMessage)

        # Flag alerts only go to facilitators
        if thing.objType != 'flag':
            thingURL = '%s/%s/%s/%s'%(workshopURL, thing.objType, thing['urlCode'], thing['url'])
            txtFile = emailDir + "/memberItemAlert.txt"
    
            # open and read the text file
            fp = open(txtFile, 'r')
            textMessage = fp.read()
            fp.close()
                
            # do the substitutions
            textMessage = textMessage.replace('${c.thingType}', newThing)
            textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
            textMessage = textMessage.replace('${c.workshopURL}', workshopURL)
            textMessage = textMessage.replace('${c.workshopName}', workshopName)
            textMessage = textMessage.replace('${c.thingURL}', thingURL)
            textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
            
            subject = 'Alert: New %s added to a bookmarked Civinomics workshop'%newThing
            for follower in followers:
                if 'itemAlerts' in follower and follower['itemAlerts'] == '1':
                    followerUser = userLib.getUserByID(follower.id)
                    toEmail = followerUser['email']
  
                    mailLib.send(toEmail, fromEmail, subject, textMessage)

            subject = 'Listener Alert: New %s added to your Civinomics workshop'%newThing                
            for listener in listeners:
                if 'itemAlerts' in listener and listener['itemAlerts'] == '1':
                    listenerUser = userLib.getUserByCode(listener['userCode'])
                    toEmail = listenerUser['email']
  
                    mailLib.send(toEmail, fromEmail, subject, textMessage)
                    
            subject = 'Private Workshop Alert: New %s added to your Civinomics workshop'%newThing                
            for pmember in pmembers:
                if 'itemAlerts' in pmember and pmember['itemAlerts'] == '1':
                    pmemberUser = userLib.getUserByCode(pmember['userCode'])
                    toEmail = pmemberUser['email']
  
                    mailLib.send(toEmail, fromEmail, subject, textMessage)
                
                

                