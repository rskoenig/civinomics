import logging
log = logging.getLogger(__name__)

from pylowiki.model import Thing, Data, meta
from dbHelpers import with_characteristic as wc

def linkChildToParent(child, parent):
    # Defines a standard for object linking.
    # All objects that get accessed through a URL need the following two fields:
    # 
    # urlCode: obtained from toBase62() in pylowiki/lib/utils.py
    # url: obtained from urlify() in pylowiki/lib/utils.py
    # 
    # Because the urlCode field is unique, this is what we use to link objects.
    try:
        code = parent['urlCode']
    except Exception as e:
        log.error("linkChildToParent(): parent object missing 'urlCode' field.")
        return False
    
    key = '%s%s' %(parent.objType, 'Code')
    if key not in child:
        child[key] = code
    else:
        log.warning("linkChildToParent(): parent object link already exists in child.")
    return child
   
def getThing(code):
    try:
        return meta.Session.query(Thing)\
            .filter(Thing.data.any(wc('urlCode', code))).one()
    except Exception as e:
        log.info(e)
        return False
        
def getThingByID(thingID):
    try:
        return meta.Session.query(Thing)\
            .filter_by(id = thingID)\
            .one()
    except:
        return False

def addedItemAs(thing, privs, role = None):
    """
        thing       ->  A Thing object
        privs       ->  The c.privs dict that sets permissions within a workshop
        role        ->  (Optional) The preferred role to use, in string format.
        
        This sets the addedAs attribute for a given Thing.  For example, if someone is
        posting a comment as a facilitator, then that comment gets the 'addedAs' attribute
        set to 'facilitator'.
        
        If the attribute already exists, it overwrites.  If the attribute does not exist, it creates.
    """
    if role is not None:
        thing['addedAs'] = role
    else:
        if privs['admin']:
            thing['addedAs'] = 'admin'
        elif privs['facilitator']:
            thing['addedAs'] = 'facilitator'
        else:
            thing['addedAs'] = 'user'
    return thing
