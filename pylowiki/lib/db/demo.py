#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic as wc
import pylowiki.lib.db.event    as eventLib
import pylowiki.lib.db.generic  as generic

log = logging.getLogger(__name__)

def getDemo():
    try:
        return meta.Session.query(Thing)\
            .filter_by(objType = 'demo')\
            .one()
    except:
        return False

def setDemo(workshop, user, **kwargs):
    data = '%s set workshop %s as the demo workshop' %(user['email'], workshop['urlCode'])
    demo = getDemo()
    if not demo:
        demo = Demo(workshop, user, **kwargs)
        title = 'Initial demo workshop'
        eventLib.Event(title, data, workshop, user)
        return demo
    title = 'Updated demo workshop'
    eventLib.Event(title, data, workshop, user)
    generic.linkChildToParent(demo, workshop)
    commit(demo)
    return demo

def Demo(workshop, user, **kwargs):
    """
        Only points to one workshop at a time; that workshop is the demo workshop used for a product tour.
        Should not be called on directly - use setDemo() instead.
    """
    demo = Thing('demo', user.id)
    generic.linkChildToParent(demo, workshop)
    commit(demo)
    return demo
    