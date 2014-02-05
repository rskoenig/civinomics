import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.message      as messageLib
import pylowiki.lib.db.dbHelpers    as dbHelpers
import pylowiki.lib.db.user         as userLib

log = logging.getLogger(__name__)

class MessageController(BaseController):

    def __before__(self, action, id1 = None, id2 = None):
        if id1 is not None and id2 is not None:
            c.user = userLib.getUserByCode(id1)
            if not c.user:
                abort(404)
            if 'user' in session:
                if userLib.isAdmin(c.authuser.id):
                    c.isAdmin = True
                if c.user.id == c.authuser.id or c.isAdmin:
                    c.messages = messageLib.getMessages(c.user)
                    c.unreadMessageCount = messageLib.getMessages(c.user, read = u'0', count = True)
                    
            else:
                log.info('user not in session')
                session['afterLoginURL'] = session._environ['PATH_INFO']
                log.info('message ctrl %s' % session['afterLoginURL'])
                session.save()
                return redirect('/login')
        

    def markRead(self, urlCode):
        self.error = False
        self.message = messageLib.getMessage(c.authuser, urlCode)
        if not self.message:
            self.error = True

        if self.error:
            return "Error"
        self.message['read'] = u'1'
        dbHelpers.commit(self.message)
        return "OK"

    def showUserMessages(self, id1, id2, id3 = ''):
        return render("/derived/6_messages.bootstrap")