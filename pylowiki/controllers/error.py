# -*- coding: utf-8 -*-
import cgi

from paste.urlparser import PkgResourcesParser
from pylons import request, response, session, tmpl_context as c, error
from pylons.controllers.util import forward
from pylons.middleware import error_document_template
import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

class ErrorController(BaseController):

    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    def document(self):
        """Render the error document"""
        """Fox Created this code... """
        c.title = c.heading = "This page does not exist yet..."

        return render('/derived/404.html')

        """
        resp = request.environ.get('pylons.original_response')
        c.content = h.literal( resp.body + "<br /><br /><a href='javascript:history.go(-1)'><- Back</a>") or cgi.escape(request.GET.get('message', ''))
        
        return render('/derived/body.mako')
        """

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file('/'.join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file('/'.join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request.environ['PATH_INFO'] = '/%s' % path
        return forward(PkgResourcesParser('pylons', 'pylons'))
