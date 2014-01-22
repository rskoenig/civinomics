import logging
from pylowiki.model import meta, Data
from sqlalchemy import and_, or_

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

def without_characteristic(key, value):
    return and_(Data.key == key, Data.value != value)

def with_characteristic_like(key, value, raw = 0, case_insensitive = True):
    if raw == 0:
       value = '%' + value + '%'
    if case_insensitive:
        return and_(Data.key == key, Data.value.ilike(value))
    else:
        return and_(Data.key == key, Data.value.like(value))

def with_key_characteristic_like(key, value, raw = 0, case_insensitive = True):
    if raw == 0:
       value = '%' + value + '%'
       key = '%' + key + '%'
    if case_insensitive:
        return and_(Data.key.ilike(key), Data.value.ilike(value))
    else:
        return and_(Data.key.like(key), Data.value.like(value))

def with_key_in_list(key, values):
    return and_(Data.key == key, Data.value.in_(values))

def with_key(key, case_insensitive = True):
    value = '%'
    if case_insensitive:
        return and_(Data.key == key, Data.value.ilike(value))
    else:
        return and_(Data.key == key, Data.value.like(value))

def lessThan_characteristic(key, value):
    return and_(Data.key == key, Data.value < value)

def greaterThan_characteristic(key, value):
    return and_(Data.key == key, Data.value > value)
