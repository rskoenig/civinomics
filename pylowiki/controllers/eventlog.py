# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.model import get_all_events

import pylowiki.lib.helpers as h
import webhelpers.paginate as paginate

log = logging.getLogger(__name__)

class EventlogController(BaseController):

    @h.login_required 
    def index(self):
        """Paginate all events"""
        c.events = get_all_events()
        c.count = len(c.events)
        c.paginator = paginate.Page(
            c.events, page=int(request.params.get('page', 1)),
            items_per_page = 20, item_count = c.count
        )
        c.title = c.heading = "Event Log"  
        return render("/derived/eventlog.mako")
