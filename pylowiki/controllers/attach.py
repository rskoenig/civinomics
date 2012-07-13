# -*- coding: utf-8 -*-
import logging

import os, shutil

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render
import pylowiki.lib.helpers as h
from pylowiki.model import commit_attach

log = logging.getLogger(__name__)

class AttachController(BaseController):
    def __before__(self):
        c.title = c.heading = "Attachment Upload"

    @h.login_required
    def index(self):
        return render( "/derived/attach.mako" )

    @h.login_required
    def upload(self):

        store = c.conf['upload.path']

        userfile = request.POST['userfile']
        filename = userfile.filename.lower().replace (" ", "-")
        
        
        try:

            request.params['upload']        

            permfile = open( os.path.join( store, filename.lstrip( os.sep ) ), 'w' )
            shutil.copyfileobj( userfile.file, permfile )
        
            userfile.file.close()
            permfile.close()

            commit_attach( session['user'], "attach", filename + " " + request.params.get('remark') );

            h.flash( "The attach was successful!", "success" )

            c.content = h.literal( '<br> <img src="/attachment/%s"><br> <a href="/attachment/%s">/attachment/%s</a>' % (filename, filename, filename) )

        except:
            h.flash( "The attach was not successful!", "warning" )
            c.content = "The attach was not successful!"

        c.title = c.heading = "Attachment Upload"
        return render( "/derived/body.mako" )


    @h.login_required
    def list_attachments(self):
        c.content = 'This logic has not been written'

        return render( "/derived/body.mako" )
