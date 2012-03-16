#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic
from pylowiki.lib.utils import urlify, toBase62
from time import time

log = logging.getLogger(__name__)

def getDiscussionByID(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

class Discussion(object):
    def __init__(self, title):
        d = Thing('discussion')
        d['title'] =  title
        d['url'] = urlify(url)
        d['urlCode'] = toBase62('%s_%s'%(title, int(time())))