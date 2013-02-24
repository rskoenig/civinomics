# -*- coding: utf-8 -*-
import logging, smtplib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.dbHelpers    as dbhelpersLib
import pylowiki.lib.utils           as utilsLib
import pylowiki.lib.mail            as mailLib

log = logging.getLogger(__name__)

def facilitatorAlerts(thing):
    if 'workshopCode' in thing:
        workshop = workshopLib.getWorkshopByCode(thing['workshopCode'])
        facilitators = facilitatorLib.getFacilitatorsByWorkshop(workshop.id)
        for facilitator in facilitators:
            if 'alerts' in facilitator and facilitator['alerts'] == '1':
                facilitatorUser = userLib.getUserByID(facilitator.owner)
                thingUser = userLib.getUserByID(thing.owner)
                fromEmail = 'Civinomics Alerts <alerts@civinomics.com>'
                toEmail = facilitatorUser['email']
                thingOwner = thingUser['name']
                subject = 'Alert: New %s added to your Civinomics workshop'%thing.objType
                workshopName = workshop['title']
    
                emailDir = config['app_conf']['emailDirectory']
                myURL = config['app_conf']['site_base_url']
                thingURL = '%s/workshop/%s/%s/%s/%s/%s'%(myURL, workshop['urlCode'], workshop['url'], thing.objType, thing['urlCode'], thing['url'])
                workshopURL = '%s/workshop/%s/%s'%(myURL, workshop['urlCode'], workshop['url'])
                txtFile = emailDir + "/facilitatorAlert.txt"
    
                # open and read the text file
                fp = open(txtFile, 'r')
                textMessage = fp.read()
                fp.close()
                
                # do the substitutions
                textMessage = textMessage.replace('${c.thingType}', thing.objType)
                textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
                textMessage = textMessage.replace('${c.workshopURL}', workshopURL)
                textMessage = textMessage.replace('${c.workshopName}', workshopName)
                textMessage = textMessage.replace('${c.thingURL}', thingURL)
                textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
  
                mailLib.send(toEmail, fromEmail, subject, textMessage)


                
                