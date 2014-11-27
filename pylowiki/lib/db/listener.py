#-*- coding: utf-8 -*-
import logging
import pickle

from pylons import session, tmpl_context as c
from pylowiki.model import Thing, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_key_characteristic_like as wkcl, with_characteristic_like as wcl
from pylowiki.lib.utils import toBase62
import generic
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.utils           as utils

log = logging.getLogger(__name__)

def getListenerByCode(code):
    objectList = ['listener', 'listenerUnpublished']
    try:
        return meta.Session.query(Thing)\
                .filter(Thing.objType.in_(objectList))\
                .filter(Thing.data.any(wc('urlCode', code)))\
                .one()
    except:
        return False
        
def getAllListeners():
    objectList = ['listener', 'listenerUnpublished']
    try:
        return meta.Session.query(Thing)\
                .filter(Thing.objType.in_(objectList))\
                .order_by('-date')\
                .all()
    except:
        return False

def getListener(email, workshop):
    try:
        wkey = ''
        if 'workshop_public_scope' in workshop:
            wkey = 'workshop_public_scope'
        elif 'workshop_org_scope' in workshop:
            wkey = 'workshop_org_scope'
        if wkey != '':
            wscope = workshop[wkey]
        else:
            wscope = "foo"
            
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('email', email)))\
                .filter(Thing.data.any(wc('scope', wscope)))\
                .one()
    except:
        return False
        

def getListenersForScope(limit, scope, offset = 0):
    # kludge
    if '||' in scope:
        scope = '0' + scope.replace('||', '|0|')

    postList = []
    objectList = ['listener']
    q = meta.Session.query(Thing)\
        .filter(Thing.objType.in_(objectList))\
        .filter(Thing.data.any(wkcl('scope', scope)))\
        .order_by('-date')\
        .offset(offset)
    if limit:
        postList += q.limit(limit)
    else:
        postList += q.all()
            
    return postList

def getListenersForWorkshop(workshop, disabled = 0):
    wkey = ''
    if 'workshop_public_scope' in workshop:
        wkey = 'workshop_public_scope'
        wscope = '0' + workshop[wkey].replace('||', '|0|')
    elif 'workshop_org_scope' in workshop:
        wkey = 'workshop_org_scope'
        wscope = workshop[wkey]
    else:
        wscope = "foo"
        
    tagList = []
    tags = workshop['workshop_category_tags'].split('|')
    for tag in tags:
        if tag != '':
            tagList.append(tag)
        
    all = []
        
    # get all of the elected officials for the scope 
    listeners =  meta.Session.query(Thing)\
            .filter_by(objType = 'listener')\
            .filter(Thing.data.any(wc('scope', wscope)))\
            .filter(Thing.data.any(wc('disabled', disabled)))\
            .order_by('sort')\
            .all()
    for l in listeners:
        if l['ltype'] == 'elected':
            all.append(l)
        elif l['tag1'] in tagList or l['tag2'] in tagList:
            all.append(l)
                
    return all

def getWorkshopsForListener(listener):
    scope = listener['scope'].replace('0', '')
    scopeList = scope.split('|')
    if scopeList[8] == '':
        scopeList[8] = '0'
    scopeList[9] = '0'
    scope = '|'.join(scopeList)
    
    workshops =  meta.Session.query(Thing)\
            .filter_by(objType = 'workshop')\
            .filter(Thing.data.any(wc('workshop_public_scope', scope)))\
            .filter(Thing.data.any(wc('workshop_searchable', '1')))\
            .order_by('-date')\
            .all()
    
    workshopList = []        
    if workshops:
        for w in workshops:
            if 'readOnly' in w and w['readOnly'] == '1':
                continue
            if listener['ltype'] == 'agency':
                tagList = []
                tags = w['workshop_category_tags'].split('|')
                for t in tags:
                    if t != '':
                        tagList.append(t)
                if listener['tag1'] in tagList or listener['tag2'] in tagList:
                    workshopList.append(w)
            else:
                workshopList.append(w)
    return workshopList
    
def getListenersForUser(user, disabled = 0):
    try:
        return meta.Session.query(Thing)\
                .filter_by(objType = 'listener')\
                .filter(Thing.data.any(wc('userCode', user['urlCode'])))\
                .filter(Thing.data.any(wc('disabled', disabled)))\
                .all()
    except:
        return False

def setListenersForUserInSession(lwdisabled = 0):
    if 'listenerWorkshops' not in c.authuser:
        # hack for now CCN
        listenerWorkshops = []
        c.authuser["listenerWorkshops"] = str(pickle.dumps(listenerWorkshops))
        commit(c.authuser)
    else:
        listenerWorkshops = pickle.loads(str(c.authuser["listenerWorkshops"]))

    session["listenerWorkshops"] = listenerWorkshops
    session.save()

def Listener(name, title, group, ltype, tag1, tag2, lurl, text, email, scope, term_end):
    # recycle existing disabled listener objects for this user and this workshop
    listener = getListener(email, scope)
    if listener:
        listener['disabled'] = '0'
        commit(listener)
    else:
        listener = Thing('listener')
        listener['name'] = name
        listener['title'] = title
        listener['group'] = group
        listener['ltype'] = ltype
        listener['tag1'] = tag1
        listener['tag2'] = tag2
        listener['lurl'] = lurl
        listener['text'] = text
        listener['email'] = email
        listener['scope'] = scope
        listener['term_end'] = term_end
        listener['disabled'] = u'0'
        listener['views'] = u'0'
        listener.sort = utils.urlify(group)
        commit(listener)
        listener['urlCode'] = toBase62(listener)
        user = userLib.getUserByEmail(email)
        if user:
            listener = generic.linkChildToParent(listener, user)
            listener['name'] = user['name']
        commit(listener)  
    return listener
