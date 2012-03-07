#-*- coding: utf-8 -*-
import logging

from pylowiki.model import Thing, Data, meta
import sqlalchemy as sa
from dbHelpers import commit, with_characteristic

log = logging.getLogger(__name__)

# Every time a revision is made, we make a new revision Thing, and add another revision key-value pair to the page
class Revision(Thing):
    def __init__(owner, data):
        r = Thing('revision', owner)
        r['data'] = data
        