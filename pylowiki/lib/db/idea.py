#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, meta
import sqlalchemy as sa
from sqlalchemy import or_
from dbHelpers import commit
from dbHelpers import with_characteristic as wc, with_characteristic_like as wcl, greaterThan_characteristic as gtc
from pylowiki.lib.utils import urlify, toBase62
from discussion import Discussion

log = logging.getLogger(__name__)

def Idea(user, title, workshop):
    """
        user    ->  The user Thing creating the idea
        title   ->  The idea itself, in string format.
    """
    idea = Thing('idea', user.id)
    idea['title'] = title
    idea['disabled'] = '0'
    idea['deleted'] = '0'
    idea['allowComments'] = '1'
    idea['ups'] = '0'
    idea['downs'] = '0'
    idea['url'] = urlify(title[:20])
    commit(idea)
    idea['urlCode'] = toBase62(idea)
    d = Discussion(owner = user, discType = 'idea', attachedThing = idea, workshop = workshop, title = title)
    idea['discussionCode'] = d.d['urlCode']
    commit(idea)
    return idea