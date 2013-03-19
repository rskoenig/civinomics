# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylowiki.lib.base import BaseController, render
from pylons import config

import pylowiki.lib.db.demo         as demoLib
import pylowiki.lib.db.workshop     as workshopLib
import pylowiki.lib.db.help         as helpLib

log = logging.getLogger(__name__)

class HelpController(BaseController):

    def help( self ):
        c.subSection = 'helpCenter'
        
        demo = demoLib.getDemo()
        if not demo:
            tutorialURL = '/'
        else:
            tutorial = workshopLib.getWorkshopByCode(demo['workshopCode'])
            c.tutorialURL = '/workshops/%s/%s' %(tutorial['urlCode'], tutorial['url'])

        return render('/derived/6_help.bootstrap')

    def facilitatorGuide( self ):
      c.subSection = 'facilitatorGuide'
      return render('/derived/6_help.bootstrap')

    def faq( self ):
        c.subSection = 'faq'
        return render('/derived/6_help.bootstrap')

    def reportIssue( self ):
        c.subSection = 'reportIssue'
        return render('/derived/6_help.bootstrap')

    def reportAbuse( self ):
        c.subSection = 'reportAbuse'
        return render('/derived/6_help.bootstrap')

    def abuseHandler( self ):
        c.subSection = 'reportAbuse'
        #c.userEmail = c.authuser['email']

        error = 0
        errMsg = 'Missing fields: '

        if 'problemType' in request.params:
          problemType = request.params['problemType']
        else:
          errMsg += 'problem type,'
          error = 1

        if 'alreadyFlagged' in request.params:
          alreadyFlagged = request.params['alreadyFlagged']
        else:
          errMsg += ' already flagged (Y/N),'
          error = 1  

        if 'offendingUser' in request.params:
          offendingUser = request.params['offendingUser']
        else:
          errMsg += ' name of offending user,'
          error = 1 

        if 'startTime' in request.params:
          startTime = request.params['startTime']
        else:
          errMsg += ' start time,'
          error = 1 

        if 'problem' in request.params and 'problem' != '':
          problem = request.params['problem']
        else:
          errMsg += ' problem description,'
          error = 1 

        if 'reporterName' in request.params and 'reporterName' != '':
          reporterName = request.params['reporterName']
        else:
          errMsg += ' name,'
          error = 1 

        if 'reporterEmail' in request.params and 'reporterEmail' != '':
          reporterEmail = request.params['reporterEmail']
        else:
          errMsg += ' email '
          error = 1 

        if error == 1:
          alert = {'type':'error'}
          alert['title'] = 'Error'
          alert['body'] = errMsg
          session['alert'] = alert
          session.save()

          return render('/derived/6_help.bootstrap')

        else:
          alert = {'type':'success'}
          alert['title'] = 'Success!'
          alert['body'] = 'Your report has been received. We will get back to you as soon as possible.'
          session['alert'] = alert
          session.save()
          helpLib.sendAbuseReport(problemType, alreadyFlagged, offendingUser, startTime, problem, reporterName, reporterEmail)

        return render('/derived/6_help.bootstrap')