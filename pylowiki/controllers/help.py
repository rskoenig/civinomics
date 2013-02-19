# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylons import config

log = logging.getLogger(__name__)

class HelpController(BaseController):

    def help( self ):
        c.subSection = 'helpCenter'
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