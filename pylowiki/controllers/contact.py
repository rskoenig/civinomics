# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

# pylowiki imports

from pylowiki.lib.mail import send
import pylowiki.lib.helpers as h

class ContactController(BaseController):
    def __before__(self):
        c.title = c.heading =  'Contact us'
    
    def index(self):
        return render('/derived/contact.mako')

    def handler(self):
        try:
            to_email = c.conf['contact.email']
            from_email = request.params['from_email']
            subject = request.params['subject']
            # convert message field to ascii, ignore unknown chars 
            # message = unicode( request.params['message'], encoding='ascii', errors='ignore' )
            message = request.params['message']
            
            if len( from_email.split('@') ) == 2: # email needs one @
                
                # Attempt to send submitted for to config contact.email
                # If successful, send success email and show success page.
	         
                if send( to_email, from_email, subject, message ):
                    message = "We have received your email.  We will get back to you as soon as possible!"
                    send( from_email, c.conf['contact.email'], subject, message )
                    h.flash( 'Email was sent successfully.', 'success')
                else:
                    h.flash( 'Email was NOT sent successfully.', 'error' )
                    
            else:
                h.flash( 'Invalid email address.  Press back to correct.', 'error' )

        except KeyError:
                h.flash( 'Please fill out all fields', 'error' )
        
        return redirect( url( controller='contact', action='index') )
