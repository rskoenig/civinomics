import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.model import getSurvey, Survey, SurveyAns, commit

import pylowiki.lib.helpers as h
import simplejson as json

log = logging.getLogger(__name__)

class IpadlistenerController(BaseController):

    @h.login_required
    def index(self):
        if c.authuser.accessLevel <= 150:
            log.info('User %s with id %s tried to access (unauthorized) index page of ipadListener' %(c.authuser.name, c.authuser.id))
            h.flash('Unauthorized access.', 'error')
            return redirect('/')
        log.info('User %s with id = %s successfully accessed ipadListener index page' %(c.authuser.name, c.authuser.id))

    @h.login_required
    def sendSurveyData(self):
        if c.authuser.accessLevel < 150:
            h.flash('Unauthorized access', 'error')
            log.info('User %s with id = %s tried to access (unauthorized) sendSurveyData page of ipadListener' %(c.authuser.name, c.authuser.id))
            return redirect('/')
        log.info('User %s with id = %s successfully accessed ipadListener sendSurveyData page' %(c.authuser.name, c.authuser.id))

        for key in request.params:
            dict = key

        dict = json.loads(dict)
        for key in dict:
            log.info('key: %s =========== value: %s' %(key, dict[key]))

        surveyName = dict['survey']
        survey = getSurvey(surveyName)
        if not survey:
            survey = Survey(surveyName, 'Completely devoid of any description whatsoever')
            survey.creator = c.authuser
            if not commit(survey):
                return "Failed to create new survey"

        for key in dict:
            if key == 'survey':
                continue
            questionNum = key
            questionAns = request.params[key]
            sAns = SurveyAns(questionNum, questionAns)
            survey.answers.append(sAns)
            if not commit(sAns):
                return "Failed to commit this survey"
            log.info('questionNum: %s, questionAns: %s' %(questionNum, questionAns))
        return "Sucessfully accessed this page"

    
