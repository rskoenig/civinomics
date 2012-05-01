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
        return meta.Session.query(Thing).filter_by(objType = 'discussion').filter_by(id = id).one()
    except:
        return False

class Discussion(object):
    # If the owner is None, the discussion is a system generated discussion, like the comments in the background wiki.
    # If the owner is not None, then the discussion was actively created by some user.
    def __init__(self, **kwargs):
        """
            Discussions can only be attached to a workshop's feedback, a workshop's background, and a suggestion
            kwargs: dict of arguments, keyed as follows:
                    owner                ->    The owner Thing that created the discussion
                    title                ->    The title of the discussion, in string format
                    attachedThing        ->    The Thing to which we are attaching this discussion
                    discType             ->    Used to determine special properties, like a background discussion or a feedback discussion in a workshop
                    workshop             ->    Used for creating the 'workshopCode' and 'workshopURL' linkbacks if the discussion isn't tied directly to a workshop
        """
        if 'owner' not in kwargs.keys():
            d = Thing('discussion')
        else:
            d = Thing('discussion', kwargs['owner'].id)
        title = kwargs['title']
        attachedThing = kwargs['attachedThing']
        discType = kwargs['discType']
        d['discType'] = discType # Used in determining the linkbacks
        if attachedThing.objType == 'workshop':
            d['workshopCode'] = attachedThing['urlCode']
            d['workshopURL'] = attachedThing['url']
        elif attachedThing.objType == 'suggestion':
            d['workshopCode'] = kwargs['workshop']['urlCode']
            d['workshopURL'] = kwargs['workshop']['url']
            d['suggestionCode'] = attachedThing['urlCode']
            d['suggestionURL'] = attachedThing['url']
        elif attachedThing.objType == 'article':
            d['workshopCode'] = kwargs['workshop']['urlCode']
            d['workshopURL'] = kwargs['workshop']['url']
            d['articleCode'] = attachedThing['urlCode']
            d['articleURL'] = attachedThing['url']
        d['title'] = title
        d['url'] = urlify(title)
        d['urlCode'] = toBase62('%s_%s'%(title, int(time())))
        d['numComments'] = 0
        d['attachedThing_id'] = attachedThing.id
        commit(d)
        
        self.d = d
