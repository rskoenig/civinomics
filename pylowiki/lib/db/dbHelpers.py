import logging
from pylowiki.model import meta

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


