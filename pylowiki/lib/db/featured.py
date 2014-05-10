import urllib2

from pylons import tmpl_context as c, config, session
from pylons import request
from pylowiki.model import Thing, meta, Data
from sqlalchemy import and_, not_, or_

import pylowiki.lib.utils           as utils
import pylowiki.lib.db.facilitator  as facilitatorLib
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.pmember      as privateMemberLib
import pylowiki.lib.db.activity     as activityLib
import pylowiki.lib.db.discussion   as discussionLib
import pylowiki.lib.db.listener     as listenerLib
import pylowiki.lib.db.generic      as generic
import pylowiki.lib.db.page         as pageLib
import pylowiki.lib.db.event        as eventLib
import pylowiki.lib.db.slideshow    as slideshowLib
import pylowiki.lib.db.slide        as slideLib
import pylowiki.lib.db.mainImage    as mainImageLib
import pylowiki.lib.mail            as mailLib

from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl
import time, datetime, logging

log = logging.getLogger(__name__)

def getFeatured():
    log.info('in database featured function!!')
    try:
        return meta.Session.query(Thing).filter_by(objType = 'workshop').filter(Thing.data.any(wc('featured', '1'))).all()
        
    except:
        return False
