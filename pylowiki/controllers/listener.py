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
import pylowiki.lib.db.geoInfo      as geoInfoLib
import pylowiki.lib.db.tag          as tagLib

log = logging.getLogger(__name__)

class ListenerController(BaseController):
    
    def __before__(self, action = "foo", urlCode = "foo"):
        if not urlCode or urlCode == '':
            abort(404)

    def listenerShow(self, urlCode):
        c.listener = listenerLib.getListenerByCode(urlCode)
        if c.listener:
            views = int(c.listener['views'])
            views += 1
            c.listener['views'] = str(views)
            dbHelpers.commit(c.listener)
            
        if c.listener and 'userCode' in c.listener:
            userCode = c.listener['userCode']
            c.member = userLib.getUserByCode(userCode)
            
        c.tags = []
        if 'tag1' in c.listener and c.listener['tag1'] != "":
            c.tags.append(c.listener['tag1'])
        if 'tag2' in c.listener and c.listener['tag2'] != "":
            c.tags.append(c.listener['tag2'])
            
        
        return render( "/derived/6_listener.bootstrap" )
     
    @h.login_required   
    def listenerEdit(self, urlCode):
        # initialize the scope dropdown selector in the edit template
        c.states = geoInfoLib.getStateList('United-States')
        c.country = "United States"
        c.state = "0"
        c.county = "0"
        c.city = "0"
        c.postal = "0"
        
        c.tagList = tagLib.getTagCategories()

        if urlCode != 'new':
            c.listener = listenerLib.getListenerByCode(urlCode)
            
            # ||country||state||county||city|zip
            if c.listener['scope'] != '':
                geoTags = c.listener['scope'].split('|')
                c.country = utils.geoDeurlify(geoTags[2])
                c.state = utils.geoDeurlify(geoTags[4])
                c.county = utils.geoDeurlify(geoTags[6])
                c.city = utils.geoDeurlify(geoTags[8])
                c.postal = utils.geoDeurlify(geoTags[9])
            else:
                if userLib.isAdmin(c.authuser.id):
                    c.country = "United States"
                    c.state = "0"
                    c.county = "0"
                    c.city = "0"
                    c.postal = "0"
                elif 'curateLevel' in c.authuser and c.authuser['curateLevel'] != '':
                    scope = '0' + c.authuser['curateScope']
                    clevel = c.authuser['curateLevel']
                    if clevel == '2':
                        scope += '|0|0|0|0|0|0|0'
                    elif clevel == '4':
                        scope += '|0|0|0|0|0'
                    elif clevel == '6':
                        scope += '|0|0|0'
                    elif clevel == '8':
                        scope += '|0'
            
                    geoTags = scope.split('|')
                    c.country = utils.geoDeurlify(geoTags[2])
                    c.state = utils.geoDeurlify(geoTags[4])
                    c.county = utils.geoDeurlify(geoTags[6])
                    c.city = utils.geoDeurlify(geoTags[8])
                    c.postal = utils.geoDeurlify(geoTags[9])

        return render( "/derived/6_listener_edit.bootstrap" )
            
    @h.login_required
    # name, title, group, ltype, tag1, tag2, lurl, text, email, scope, term_end
    def listenerEditHandler(self, urlCode):
        if 'listenerName' not in request.params or 'listenerTitle' not in request.params or 'listenerEmail' not in request.params:
            abort(404)
            
        name = request.params['listenerName']
        title = request.params['listenerTitle']
        email = request.params['listenerEmail']
        ltype = request.params['listenerType']
        
        if 'listenerGroup' in request.params and request.params['listenerGroup'] != '':
            group = request.params['listenerGroup']
        else:
            group = ""
            
        if 'listenerTag1' in request.params and request.params['listenerTag1'] != '':
            tag1 = request.params['listenerTag1']
        else:
            tag1 = ""
            
        if 'listenerTag2' in request.params and request.params['listenerTag2'] != '':
            tag2 = request.params['listenerTag2']
        else:
            tag2 = ""
        
        if 'listenerText' in request.params and request.params['listenerText'] != '':
            text = request.params['listenerText']
        else:
            text = "" 
            
        if 'listenerURL' in request.params and request.params['listenerURL'] != '':
            lurl = request.params['listenerURL']
        else:
            lurl = ""

        if 'termEnd' in request.params and request.params['termEnd'] != '':
            term_end = request.params['termEnd']
        else:
            term_end = ""            

        
        if 'geoTagCountry' in request.params:
            if 'geoTagCountry' in request.params and request.params['geoTagCountry'] != '0':
                geoTagCountry = request.params['geoTagCountry']
            else:
                geoTagCountry = "0"
                
            if 'geoTagState' in request.params and request.params['geoTagState'] != '0':
                geoTagState = request.params['geoTagState']
            else:
                geoTagState = "0"
                
            if 'geoTagCounty' in request.params and request.params['geoTagCounty'] != '0':
                geoTagCounty = request.params['geoTagCounty']
            else:
                geoTagCounty = "0"
                
            if 'geoTagCity' in request.params and request.params['geoTagCity'] != '0':
                geoTagCity = request.params['geoTagCity']
            else:
                geoTagCity = "0"
                
            if 'geoTagPostal' in request.params and request.params['geoTagPostal'] != '0':
                geoTagPostal = request.params['geoTagPostal']
            else:
                geoTagPostal = "0"

            # assemble the scope string 
            # ||country||state||county||city|zip
            scope = "0|0|" + utils.urlify(geoTagCountry) + "|0|" + utils.urlify(geoTagState) + "|0|" + utils.urlify(geoTagCounty) + "|0|" + utils.urlify(geoTagCity) + "|" + utils.urlify(geoTagPostal)
        else:
            scope = '0|0|united-states|0|0|0|0|0|0|0'
        
        if ltype == 'elected':    
            if not name or not title or not email or not ltype:
                return "Please enter complete information"
            tag1 = ""
            tag2 = ""
        else:
            if not name or not title or not email or not ltype or not tag1 or not tag2:
                return "Please enter complete information"
                
        if urlCode == 'new':
            listener = listenerLib.Listener(name, title, group, ltype, tag1, tag2, lurl, text, email, scope, term_end)
        else:
            listener = listenerLib.getListenerByCode(urlCode)
            if not listener:
                return 'No such listener!'
            else:
                listener['name'] = name;
                listener['title'] = title;
                listener['email'] = email;
                listener['group'] = group;
                listener['ltype'] = ltype;
                listener['tag1'] = tag1;
                listener['tag2'] = tag2;
                listener['text'] = text;
                listener['scope'] = scope;
                listener['term_end'] = term_end;
                listener.sort = utils.urlify(group)

        dbHelpers.commit(listener)
        eventLib.Event('Listener edited', '%s edited listener info'%c.authuser['name'], listener, user = c.authuser)
        
        returnURL = "/listener/%s/listenerShow"%listener['urlCode']
        
        return redirect(returnURL)
            
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
