from pylowiki.model import Thing, meta

from dbHelpers import commit

import logging
log = logging.getLogger(__name__)

def getFeaturedSurvey():
    try:
        return meta.Session.query(Thing).filter_by(objType = 'featuredSurvey').one()
    except:
        return False
    
def setFeaturedSurvey(survey):
    try:
        fs = getFeaturedSurvey()
        if not fs:
            fs = FeaturedSurvey()
        fs['survey'] = survey.id
        commit(fs)
        return True
    except:
        return False

def FeaturedSurvey():
    fs = Thing('featuredSurvey')
    return fs