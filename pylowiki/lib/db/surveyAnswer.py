from pylons import tmpl_context as c

from pylowiki.model import Thing, meta
from dbHelpers import commit, with_characteristic as wc, without_characteristic as wo, with_characteristic_like as wcl

import logging
log = logging.getLogger(__name__)

def getSurveyAnswer(survey, slide, owner):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'surveyAnswer').filter_by(owner = owner.id).filter(Thing.data.any(wc('survey_id', survey.id))).filter(Thing.data.any(wc('slide_id', slide.id))).one()
    except:
        return False
    
def getAllAnswersForSurvey(survey):
    try:
        return meta.Session.query(Thing).filter_by(objType = 'surveyAnswer').filter(Thing.data.any(wc('survey_id', survey.id))).all()
    except:
        return False
    
def SurveyAnswer(survey, slide, answer, label = ''):
    s = Thing('surveyAnswer', c.authuser.id)
    s['survey_id'] = survey.id
    s['slide_id'] = slide.id
    s['slideNum'] = slide['slideNum']
    if label != '':
        s['answer_%s'%label] = answer
    else:
        s['answer'] = answer
    commit(s)
    return s

def editSurveyAnswer(survey, slide, answer, label = ''):
    surveyAnswer = getSurveyAnswer(survey, slide, c.authuser)
    if label == '':
        surveyAnswer['answer'] = answer
    else:
        surveyAnswer['answer_%s'%label] = answer
    commit(surveyAnswer)
    return surveyAnswer