import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect

import pylowiki.lib.helpers as h
from pylowiki.model import get_user, getPoints, getUserSuggestions, getArticlesRead, getVotes
from pylowiki.model import getSolutions, getUserContributions, getUserConnections, getUserWork

from pylowiki.lib.base import BaseController, render


log = logging.getLogger(__name__)

class CorpController(BaseController):
    
    def index(self):
        if 'page' in request.params :
            page = request.params['page']
            if (len(page) > 20) :
                abort(404)
            return self.render_corp_page(page)
        else :
            abort(404)

    def render_corp_page(self, page):
        render_var = {}

        if (page.lower() == 'about') :
            render_var['body_header'] = 'ABOUT'
            render_var['display_navigbar'] = True
            render_var['highlight_name'] = "about"
        elif (page.lower() == 'features') :
            render_var['body_header'] = 'FEATURES'
            render_var['display_navigbar'] = True 
            render_var['highlight_name'] = "features"
        elif (page.lower() == 'privacy') :
            render_var['body_header'] = 'PRIVACY POLICY'
            render_var['display_navigbar'] = False
        elif (page.lower() == 'careers') :
            render_var['body_header'] = 'CAREERS'
            render_var['display_navigbar'] = True
        elif (page.lower() == 'services') :
            render_var['body_header'] = 'SERVICES'
            render_var['display_navigbar'] = True
        else:
            abort(404)
        
        c.title = render_var['body_header']
        if session.get('user') :
            c.user = get_user(session['user'])
        else :
            c.user = None
        return render("/derived/corp_"+page+".mako", extra_vars=render_var)

