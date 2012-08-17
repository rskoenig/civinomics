import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class CorpController(BaseController):
    
    def index(self, id):
        if id == 'None':
            id = 'about'
        return self.render_corp_page(id)

    def render_corp_page(self, page):
        render_var = {}

        if (page.lower() == 'about') :
            render_var['body_header'] = 'ABOUT'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = "about"

        elif (page.lower() == 'careers') :
            render_var['body_header'] = 'CAREERS'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'careers'

        elif (page.lower() == 'contact') :
            render_var['body_header'] = 'CONTACT US'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'contact'

        elif (page.lower() == 'features') :
            render_var['body_header'] = 'FEATURES'
            render_var['display_navigbar'] = True 
            render_var['highlight_name'] = "features"

        elif (page.lower() == 'privacy') :
            render_var['body_header'] = 'PRIVACY POLICY'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = "privacy"

        elif (page.lower() == 'outreach') :
            render_var['body_header'] = 'OUTREACH'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'outreach'

        elif (page.lower() == 'team') :
            render_var['body_header'] = 'TEAM'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'team'

        elif (page.lower() == 'terms') :
            render_var['body_header'] = 'TERMS OF USE'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'terms'

        elif (page.lower() == 'services') :
            render_var['body_header'] = 'SERVICES'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'services'

        elif (page.lower() == 'engfrontend') :
            render_var['body_header'] = 'Engineer'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'careers'

        elif (page.lower() == 'engbackend') :
            render_var['body_header'] = 'Engineer'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'careers'

        elif (page.lower() == 'communityrep') :
            render_var['body_header'] = 'Community Representative'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = 'careers'
        else:
            abort(404)
        
        c.title = render_var['body_header']
        return render("/derived/corp_"+page+".bootstrap", extra_vars=render_var)

