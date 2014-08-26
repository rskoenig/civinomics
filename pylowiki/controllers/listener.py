# -*- coding: utf-8 -*-
import logging
import pickle

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render

import pylowiki.lib.helpers         as h
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.utils           as utils
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.generic      as generic

log = logging.getLogger(__name__)

class ListenerController(BaseController):
    
    @h.login_required
    def __before__(self, action, urlCode):
        if not urlCode or urlCode == '':
            abort(404)

    def listenerShow(self, urlCode):
        c.listener = listenerLib.getListenerByCode(urlCode)
        
        return render( "/derived/6_listener.bootstrap" )
            
    @h.login_required
    def listenerEditHandler(self, urlCode):
        payload = request.params
        if 'lName' not in payload or 'lTitle' not in payload or 'lEmail' not in payload or 'urlCode' not in payload:
            return "Error"
        lName = payload['lName']
        lTitle = payload['lTitle']
        lEmail = payload['lEmail']
        urlCode = payload['urlCode']
        if not lName or not lTitle or not lEmail:
            return "Please enter complete information"
        if urlCode == 'new':
            listener = listenerLib.Listen()
        else:
            listener = listenerLib.getListenerByCode(urlCode)
            if not listener:
                return 'No such listener!'
            else:
                listener['name'] = lName;
                listener['title'] = lTitle;
                listener['email'] = lEmail;

        dbHelpers.commit(listener)
        eventLib.Event('Listener edited', '%s edited listener info'%c.authuser['name'], listener, user = c.authuser)
        return "Updated Listener."
            
    @h.login_required
    def listenerToggleHandler(self):
        payload = json.loads(request.body)
        if 'lReason' not in payload:
            return '{"state":"Error", "errorMessage":"Error no lReason"}'
        if 'urlCode' not in payload:
            return '{"state":"Error", "errorMessage":"Error no urlCode"}'
        if 'toggleState' not in payload:
            return '{"state":"Error", "errorMessage":"Error no toggle state"}'
            
        lReason = payload['lReason']
        urlCode = payload['urlCode']
        toggleState = payload['toggleState']
        
        if not lReason or not urlCode or not toggleState:
            return '{"state":"Error", "errorMessage":"Please enter complete information"}'
            
        # get the listener object
        listener = listenerLib.getListenerByCode(urlCode)

        if not listener:
            return '{"state":"Error", "errorMessage":"No such Listener!"}'
            
        # toggle the listener
        if listener['disabled'] == '1':
            listener['disabled'] = '0';
            dbHelpers.commit(listener)
            returnMsg = "Listener Enabled!"
        elif listener['disabled'] == '0':
            listener['disabled'] = '1';
            dbHelpers.commit(listener)
            returnMsg = "Listener Disabled!"
        
        if 'userCode' in listener:
            user = userLib.getUserByCode(listener['userCode'])
            if 'listenerWorkshops' in user:
                listenerWorkshops = pickle.loads(str(user["listenerWorkshops"]))
            else:
                listenerWorkshops = []
                
            lKey = 'listener_counter'
            if lKey in user:
                lValue = int(user[lKey])
                if listener['disabled'] == '0':
                    lValue += 1
                else:
                    lValue -= 1
            else:
                if listener['disabled'] == '0':
                    lValue = 1
                else:
                    lValue = 0
            
            if toggleState == 'Enable':
                if listener['workshopCode'] not in listenerWorkshops:
                    listenerWorkshops.append(listener['workshopCode'])
            else:
                if listener['workshopCode'] in listenerWorkshops:
                    listenerWorkshops.remove(listener['workshopCode'])
                    
            user[lKey] = str(lValue)
            user['listenerWorkshops'] = str(pickle.dumps(listenerWorkshops))
            session['listenerWorkshops'] = listenerWorkshops
            session.save()
            dbHelpers.commit(user)
            
        eventLib.Event(returnMsg, '%s by %s'%(returnMsg, c.authuser['name']), listener, user = c.authuser)
        return returnMsg
        
    @h.login_required
    def listenerListHandler(self):
        activeEnabled = []
        pendingEnabled = []
        activeDisabled = []
        pendingDisabled = []
        
        #log.info('listenerListHandler')
        enabled = listenerLib.getListenersForWorkshop(c.w)
        for l in enabled:
            if 'userCode' in l:
                activeEnabled.append(l)
            else:
                pendingEnabled.append(l)
                
        disabled = listenerLib.getListenersForWorkshop(c.w, '1')
        for l in disabled:
            if 'userCode' in l:
                activeDisabled.append(l)
            else:
                pendingDisabled.append(l)
                    
        jsonReturn = '{ "listeners": ['
        comma = ''
        for l in activeEnabled:
            user = userLib.getUserByCode(l['userCode'])
            userImage = generic.userImageSource(user)
            profileLink = "/profile/" + user['urlCode'] + "/" + user['url']
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Disable","state":"Active"}'
            comma = ','
 
        if not activeEnabled:
            comma = ''
        userImage = "/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png"
        profileLink = ""
        for l in pendingEnabled:
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Disable","state":"Pending"}'
            comma = ','

        if not activeEnabled and not pendingEnabled:
            comma = ''
        for l in activeDisabled:
            user = userLib.getUserByCode(l['userCode'])
            userImage = generic.userImageSource(user)
            profileLink = "/profile/" + user['urlCode'] + "/" + user['url']
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Enable","state":"Active Disabled"}'
            comma = ','

        if not activeEnabled and not pendingEnabled and not activeDisabled:
            comma = ''
        userImage = "/images/glyphicons_pro/glyphicons/png/glyphicons_003_user.png"
        profileLink = ''
        for l in pendingDisabled:
            jsonReturn += comma + '{"urlCode":"' + l['urlCode'] + '","lName":"' + l['name'].replace("'", "&#39;") + '", "lTitle":"' + l['title'].replace("'", "&#39;") + '", "lEmail":"' + l['email'] + '", "profileLink":"' + profileLink + '","userImage":"' + userImage + '", "button":"Enable","state":"Pending Disabled"}'
            comma = ','
        jsonReturn += "]}"
        
        return jsonReturn
