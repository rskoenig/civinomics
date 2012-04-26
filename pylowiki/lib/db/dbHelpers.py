import logging
from pylowiki.model import meta, Data
from sqlalchemy import and_

log = logging.getLogger(__name__)

################
# Commit helpers
################

def commit(obj):
    try:
        meta.Session.add(obj)
        meta.Session.commit()
        return True
    except:
        log.info("Could not commit: ")
        log.info(obj)
        raise
        return False

def with_characteristic(key, value):
    return and_(Data.key == key, Data.value == value)
#with_characteristic = lambda key, value: and_(Data.key == key, Data.value == value)