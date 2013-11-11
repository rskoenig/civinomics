import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.dbHelpers    as dbHelpers

log = logging.getLogger(__name__)

class MessageController(BaseController):

    def __before__(self, action, urlCode):
        self.error = False
        self.message = messageLib.getMessage(c.authuser, urlCode)
        if not self.message:
            self.error = True

    def markRead(self, urlCode):
        if self.error:
            return "Error"
        self.message['read'] = u'1'
        dbHelpers.commit(self.message)
        return "OK"