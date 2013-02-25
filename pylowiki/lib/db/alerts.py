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
            if ('flagAlerts' in facilitator and facilitator['flagAlerts'] == '1' and thing.objType == 'flag') or ('itemAlerts' in facilitator and facilitator['itemAlerts'] == '1'):
                facilitatorUser = userLib.getUserByID(facilitator.owner)
                thingUser = userLib.getUserByID(thing.owner)
                fromEmail = 'Civinomics Alerts <alerts@civinomics.com>'
                toEmail = facilitatorUser['email']
                thingOwner = thingUser['name']
                workshopName = workshop['title']
                newThing = thing.objType
    
                emailDir = config['app_conf']['emailDirectory']
                myURL = config['app_conf']['site_base_url']
                workshopURL = '%s/workshop/%s/%s'%(myURL, workshop['urlCode'], workshop['url'])
                if thing.objType == 'flag':
                    thingURL = workshopURL + '/preferences'
                    newThing = 'flagged item'
                else:
                    thingURL = '%s/%s/%s/%s'%(workshopURL, thing.objType, thing['urlCode'], thing['url'])

                txtFile = emailDir + "/facilitatorAlert.txt"
    
                # open and read the text file
                fp = open(txtFile, 'r')
                textMessage = fp.read()
                fp.close()
                
                # do the substitutions
                subject = 'Alert: New %s added to your Civinomics workshop'%newThing
                textMessage = textMessage.replace('${c.thingType}', newThing)
                textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
                textMessage = textMessage.replace('${c.workshopURL}', workshopURL)
                textMessage = textMessage.replace('${c.workshopName}', workshopName)
                textMessage = textMessage.replace('${c.thingURL}', thingURL)
                textMessage = textMessage.replace('${c.thingOwner}', thingOwner)
  
                mailLib.send(toEmail, fromEmail, subject, textMessage)


                
                