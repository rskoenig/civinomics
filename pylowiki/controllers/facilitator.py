# -*- coding: utf-8 -*-
import logging
import pickle

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import webhelpers.paginate as paginate
import pylowiki.lib.helpers as h
from pylons import config

import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.initiative   as initiativeLib
import pylowiki.lib.db.dbHelpers    as dbhelpersLib
import pylowiki.lib.utils           as utilsLib
import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.mail            as mailLib

from hashlib import md5
import simplejson as json

log = logging.getLogger(__name__)

class FacilitatorController(BaseController):

    def __before__(self, action, code, url):
        if action in ['facilitateInviteHandler', 'facilitateResponseHandler']:
            c.user = userLib.getUserByCode(code)
        elif action in ['facilitateResignHandler', 'facilitatorNotificationHandler']:
            c.w = workshopLib.getWorkshopByCode(code)

    @h.login_required
    def facilitateInviteHandler(self, code, url):
        if c.user and 'inviteToFacilitate' in request.params:
            invite = request.params['inviteToFacilitate']
            iList = invite.split("/")
            itemCode = iList[0]
            itemURL = iList[1]
            try:
              item = workshopLib.getWorkshopByCode(itemCode)
              workshopLib.setWorkshopPrivs(item)
              objType = 'w'
              extraInfo = 'facilitationInvite'
              title = 'Facilitation invitation'
            except:
              item = initiativeLib.getInitiative(itemCode)
              objType = 'i'
              extraInfo = 'authorInvite'
              title = 'Coauthor invitation'
            facilitator = facilitatorLib.Facilitator(c.user, item, 1)
            if objType == 'w':
              fList = facilitatorLib.getFacilitatorsByUserAndWorkshop(c.user, item)
            elif objType == 'i':
              fList = facilitatorLib.getFacilitatorsByUserAndInitiative(c.user, item)
            text = '(This is an automated message)'
            m = messageLib.Message(owner = c.user, title = title, text = text, privs = c.privs, item = item, extraInfo = extraInfo, sender = c.authuser)
            m = generic.linkChildToParent(m, fList[0])
            dbhelpersLib.commit(m)
            eventLib.Event('CoFacilitator Invitation Issued', '%s issued an invitation to co facilitate %s'%(c.authuser['name'], item['title']), m, user = c.authuser, action = extraInfo)
            alert = {'type':'success'}
            alert['title'] = 'Success. ' + title + 'issued.'
            session['alert'] = alert
            session.save()
            return redirect(session['return_to'] + "#coauthors")
        else:
            alert = {'type':'error'}
            alert['title'] = 'Authorization Error. You are not authorized.'
            session['alert'] = alert
            session.save()
            return redirect(session['return_to'] + "#coauthors")

    @h.login_required
    def iFacilitateInviteHandler(self, code, url, userCode):
        inviteAuthor = userLib.getUserByCode(userCode)
        i = initiativeLib.getInitiative(code)

        iFacilitators = facilitatorLib.getAllFacilitatorsByInitiative(i)
        existing = False
        privs = False
        for fObj in iFacilitators:
          # check to see if the inviteAuthor already has a facilitator object for this initiative:
          if fObj.owner == inviteAuthor.id:
            existing = True
            f = fObj
          # check to see if active user is among the coauthors:
          if fObj.owner == c.authuser.id and fObj['disabled'] != '1':
            privs = True

        if c.authuser.id == i.owner or privs:
          if i.owner == inviteAuthor.id:
            alertMsg = '%s is already an author!' % inviteAuthor['name']
            return json.dumps({'statusCode':0, 'alertMsg':alertMsg, 'alertType':'danger'})
          elif existing:
            f['disabled'] = '0'
            dbhelpersLib.commit(f)
            if 'resendInvite' in request.params:
              alertMsg = 'A new coauthor invitation has been sent to %s.' % inviteAuthor['name']
            else:
              alertMsg = '%s has been activated as a coauthor.' % inviteAuthor['name']
          else:
            facilitator = facilitatorLib.Facilitator(inviteAuthor, i, 1)
            fList = facilitatorLib.getFacilitatorsByUserAndInitiative(inviteAuthor, i)
            f = fList[0]
            alertMsg = '%s has been added as a coauthor.' % inviteAuthor['name']

          text = '(This is an automated message)'
          title = 'Coauthor invitation'
          extraInfo = 'authorInvite'
          m = messageLib.Message(owner = inviteAuthor, title = title, text = text, privs = c.privs, item = i, extraInfo = extraInfo, sender = c.authuser)
          m = generic.linkChildToParent(m, f)
          dbhelpersLib.commit(m)
          eventLib.Event('CoFacilitator Invitation Issued', '%s issued an invitation to co facilitate %s'%(c.authuser['name'], i['title']), m, user = c.authuser, action = extraInfo)
          mailLib.sendCoauthorAddMail(inviteAuthor, c.authuser, i)

          return json.dumps({'statusCode':0, 'alertMsg':alertMsg, 'alertType': 'success'})

        else: 
          abort(404)

    @h.login_required
    def facilitateResponseHandler(self, code, url):
        if 'workshopCode' in request.params and 'workshopURL' in request.params:
            itemCode = request.params['workshopCode']
            itemURL = request.params['workshopURL']
            itemType = 'w'
            mType = "CoFacilitator"
        elif 'initiativeCode' in request.params and 'initiativeURL' in request.params:
            itemCode = request.params['initiativeCode']
            itemURL = request.params['initiativeURL']
            itemType = 'i'
            mType = "CoAuthor"

        if itemCode and itemCode != '':
            if 'messageCode' not in request.params:
                abort(404)
            messageCode = request.params['messageCode']
            message = messageLib.getMessage(c.user, messageCode)
            messageSender = userLib.getUserByCode(message['sender'])
            if not message:
                abort(404)
            if itemType == 'w':
              item = workshopLib.getWorkshop(itemCode, utilsLib.urlify(itemURL))
            elif itemType == 'i':
              item = initiativeLib.getInitiative(itemCode)
            fList = facilitatorLib.getFacilitatorsByUser(c.authuser)
            doF = False

            for f in fList:
              if 'workshopCode' in f and f['workshopCode'] == item['urlCode']:
                doF = f
              elif 'initiativeCode' in f and f['initiativeCode'] == item['urlCode']:
                  doF = f

            if doF and 'acceptInvite' in request.params:
                  doF['pending'] = '0'
                  eAction = "Accepted"
                  # this is an odd place to do this, but here we go
                  if 'workshopCode' in doF:
                    facilitatorWorkshops = pickle.loads(str(c.authuser["facilitatorWorkshops"]))
                    facilitatorWorkshops.append(doF['workshopCode'])
                    c.authuser['facilitatorWorkshops'] = str(pickle.dumps(facilitatorWorkshops))
                    session['facilitatorWorkshops'] = facilitatorWorkshops
                  elif 'initiativeCode' in doF:
                    facilitatorInitiatives = pickle.loads(str(c.authuser["facilitatorInitiatives"]))
                    facilitatorInitiatives.append(doF['initiativeCode'])
                    c.authuser['facilitatorInitiatives'] = str(pickle.dumps(facilitatorInitiatives))
                    session['facilitatorInitiatives'] = facilitatorInitiatives
                  dbhelpersLib.commit(c.authuser)
                  session.save()
                      
                  
            if doF and 'declineInvite' in request.params:
                  doF['pending'] = '0'
                  doF['disabled'] = '1'
                  eAction = "Declined"

            if doF:
                  dbhelpersLib.commit(doF)
                  eventLib.Event('%s Invitation %s'%(mType, eAction), '%s %s an invitation to %s %s'%(c.user['name'], eAction.lower(), mType.lower(), item['title']), message, user = c.user, action = eAction.lower())
                  # success message
                  
                  alert = {'type':'success'}
                  alert['title'] = 'Success. CoFacilitation Invitation %s.'%eAction
                  session['alert'] = alert
                  session.save()
                  
                  message['read'] = u'1'
                  dbhelpersLib.commit(message)

                  # send accept or decline message to inviter
                  text = '%s your invitation to coauthor' % eAction
                  title = 'Coauthor response'
                  extraInfo = 'authorResponse'
                  m = messageLib.Message(owner = messageSender, title = title, text = text, privs = c.privs, item = item, extraInfo = extraInfo, sender = c.authuser)
                  m = generic.linkChildToParent(m, doF)
                  dbhelpersLib.commit(m)
                  eventLib.Event('CoFacilitator Invitation %s' % eAction, '%s issued an invitation to co facilitate %s'% (c.authuser['name'], item['title']), m, user = c.authuser, action = extraInfo)

                  if eAction == "Accepted":
                    if itemType == 'w':
                      return redirect("/workshop/%s/%s"%(itemCode, itemURL))
                    elif itemType == 'i':
                      return redirect("/initiative/%s/%s"%(itemCode, itemURL))
                  elif eAction == "Declined":
                    return redirect("/messages/" + c.authuser['urlCode'] + "/" + c.authuser['url'] )

        alert = {'type':'error'}
        alert['title'] = 'Authorization Error. You are not authorized.'
        session['alert'] = alert
        session.save()
        return redirect("/" )

    @h.login_required
    def facilitateResignHandler(self, code, url):
        fList = facilitatorLib.getFacilitatorsByUser(c.authuser, 0)
        doF = False
        for f in fList:
           if f['workshopCode'] == c.w['urlCode'] and f['disabled'] != '1':
              doF = f

        if 'resignReason' in request.params:
           resignReason = request.params['resignReason']
           resignReason = resignReason.lstrip()
           resignReason = resignReason.rstrip()
           if resignReason == '':
              alert = {'type':'error'}
              alert['title'] = 'Error. Please include a reason.'
              session['alert'] = alert
              session.save()
              return redirect("/workshop/%s/%s/preferences"%(code, url))

           log.info('resignReason is %s'%resignReason)
        else:
           alert = {'type':'error'}
           alert['title'] = 'Error. Please include a reason.'
           session['alert'] = alert
           session.save()
           return redirect("/workshop/%s/%s"%(code, url))

        if doF and c.authuser.id == doF.owner:
           doF['disabled'] = '1'
           dbhelpersLib.commit(doF)
           eventLib.Event('CoFacilitator Resigned', '%s resigned as cofacilitator of %s: %s'%(c.authuser['name'], c.w['title'], resignReason), doF, user = c.authuser)
           alert = {'type':'success'}
           alert['title'] = 'Success. CoFacilitation resignation successful.'
           session['alert'] = alert
           session.save()
           if 'workshopCode' in doF:
                facilitatorWorkshops = pickle.loads(str(c.authuser["facilitatorWorkshops"]))
                if doF['workshopCode'] in facilitatorWorkshops:
                    facilitatorWorkshops.remove(doF['workshopCode'])
                    c.authuser['facilitatorWorkshops'] = str(pickle.dumps(facilitatorWorkshops))
                    session['facilitatorWorkshops'] = facilitatorWorkshops
           elif 'initiativeCode' in doF:
                facilitatorInitiatives = pickle.loads(str(c.authuser["facilitatorInitiatives"]))
                if doF['initiativeCode'] in facilitatorInitiatives:
                    facilitatorInitiatives.remove(doF['initiativeCode'])
                    c.authuser['facilitatorInitiatives'] = str(pickle.dumps(facilitatorInitiatives))
                    session['facilitatorInitiatives'] = facilitatorInitiatives
           dbhelpersLib.commit(c.authuser)
           session.save()
                      
           return redirect("/workshop/%s/%s"%(code, url))

        alert = {'type':'error'}
        alert['title'] = 'Authorization Error. You are not authorized.'
        session['alert'] = alert
        session.save()
        return redirect("/workshop/%s/%s"%(code, url))

    @h.login_required
    def iFacilitateResignHandler(self, code, url, userCode):
        removeAuthor = userLib.getUserByCode(userCode)
        i = initiativeLib.getInitiative(code)
        iFacilitators = facilitatorLib.getAllFacilitatorsByInitiative(i)
        rList = facilitatorLib.getFacilitatorsByUserAndInitiative(removeAuthor, i)

        privs = False
        # check to see if active user is among the coauthors:
        for fObj in iFacilitators:
          if fObj.owner == c.authuser.id and fObj['disabled'] != '1':
            privs = True
        # check to see if the user is the original author or is resigning:
        if c.authuser.id == i.owner or c.authuser == removeAuthor:
          privs = True

        if privs:
          for f in rList:
            f['disabled'] = '1'
            f['pending'] = '1'
            dbhelpersLib.commit(f)
            facilitatorInitiatives = pickle.loads(str(c.authuser["facilitatorInitiatives"]))
            if f['initiativeCode'] in facilitatorInitiatives:
                facilitatorInitiatives.remove(f['initiativeCode'])
                c.authuser['facilitatorInitiatives'] = str(pickle.dumps(facilitatorInitiatives))
                dbhelpersLib.commit(c.authuser)
                session['facilitatorInitiatives'] = facilitatorInitiatives
                session.save()

            if 'resign' in request.params:
              # the coauthor is resigning, he should be redirected away from the edit page
              return redirect('/initiative/%s/%s'%(code, url))
            else:
              alertMsg = '%s has been removed as a coauthor!' % removeAuthor['name']
              return json.dumps({'statusCode':0, 'alertMsg':alertMsg, 'alertType':'success'})
        else:
          abort(404)

        
    @h.login_required
    def facilitatorNotificationHandler(self, code, url, userCode):
        # check to see if this is a request from the iphone app
        iPhoneApp = utilsLib.iPhoneRequestTest(request)

        user = userLib.getUserByCode(userCode)
        facilitator = facilitatorLib.getFacilitatorInWorkshop(user, c.w)
        # initialize to current value if any, '0' if not set in object
        iAlerts = '0'
        fAlerts = '0'
        fDigest = '0'
        eAction = ''
        if 'itemAlerts' in facilitator:
            iAlerts = facilitator['itemAlerts']
        if 'flagAlerts' in facilitator:
            fAlerts = facilitator['flagAlerts']
        if 'digest' in facilitator:
            fDigest = facilitator['digest']
        
        if iPhoneApp:
            try:
                alert = request.params['alert']
            except:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
        else:
            payload = json.loads(request.body)
            if 'alert' not in payload:
                return "Error"
            alert = payload['alert']
        if alert == 'flags':
            if 'flagAlerts' in facilitator.keys(): # Not needed after DB reset
                if facilitator['flagAlerts'] == u'1':
                    facilitator['flagAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    facilitator['flagAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                facilitator['flagAlerts'] = u'1'
                eAction = 'Turned on'
        elif alert == 'items':
            if 'itemAlerts' in facilitator.keys(): # Not needed after DB reset
                if facilitator['itemAlerts'] == u'1':
                    facilitator['itemAlerts'] = u'0'
                    eAction = 'Turned off'
                else:
                    facilitator['itemAlerts'] = u'1'
                    eAction = 'Turned on'
            else:
                facilitator['itemAlerts'] = u'1'
                eAction = 'Turned on'
        elif alert == 'digest':
            if 'digest' in facilitator.keys(): # Not needed after DB reset
                if facilitator['digest'] == u'1':
                    facilitator['digest'] = u'0'
                    eAction = 'Turned off'
                else:
                    facilitator['digest'] = u'1'
                    eAction = 'Turned on'
            else:
                facilitator['digest'] = u'1'
                eAction = 'Turned on'
        else:
            if iPhoneApp:
                statusCode = 2
                response.headers['Content-type'] = 'application/json'
                #log.info("results workshop: %s"%json.dumps({'statusCode':statusCode, 'result':result}))
                return json.dumps({'statusCode':statusCode, 'result':'error'})
            else:
                return "Error"   
            
        dbhelpersLib.commit(facilitator)
        if eAction != '':
            eventLib.Event('Facilitator notifications set', eAction, facilitator, c.authuser)

        if iPhoneApp:
            statusCode = 0
            response.headers['Content-type'] = 'application/json'
            result = eAction
            return json.dumps({'statusCode':statusCode, 'result':result})
        else:
            return eAction

