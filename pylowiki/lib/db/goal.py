#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
import sqlalchemy as sa
from dbHelpers import commit
from dbHelpers import with_characteristic as wc
from pylowiki.lib.utils import toBase62
import generic

log = logging.getLogger(__name__)

def getGoalsForWorkshop(workshop):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'goal').filter(Thing.data.any(wc('workshopCode', workshop['urlCode']))).all()
    except:
        return False

def Goal(title, status, workshop):
    goal = Thing('goal', workshop.id)
    goal['title'] = title
    goal['status'] = status
    goal['deleted'] = '0'
    commit(goal)
    goal['urlCode'] = toBase62(goal)
    goal = generic.linkChildToParent(goal, workshop)
    commit(goal)
    return goal
