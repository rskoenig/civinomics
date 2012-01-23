import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pylowiki.lib.base import BaseController, render
from pylowiki.model import getSlide, commit

log = logging.getLogger(__name__)

import simplejson as json

class SlideshowController(BaseController):

    """ Huge optimization: send request per widget after close button is hit or after order is changed.
        Currently everything is being sent after any edit """
    def edit(self):
        s = request.params['string']
        slides = s.split(';|;')
        ids = []
        titles = []
        captions = []
        for slide in slides:
            s2 = slide.split('||')
            ids.append(s2[0])
            titles.append(s2[1])
            captions.append(s2[2])
            
        for i in range(len(ids)):
            s = getSlide(ids[i])
            s.title = titles[i]
            s.caption = captions[i]
            if not commit(s):
                log.error('Error commiting slide change for slideID = %s, caption = %s, title = %s, userID = %s' %(ids[i], captions[i], titles[i], c.authuser.id))
                return json.dumps({'error' : 'Error commiting slide change'})
            log.info('User %s successfully updated: slideID = %s, title = %s, caption = %s' %(c.authuser.id, ids[i], titles[i], captions[i]))

        i = s.issue
        i.slideshowOrder = ','.join(map(str, ids)) # Save the new order as a comma-separated list of slide IDs
        if not commit(i):
            log.error('Error changing slideshow order for issue = %s, user = %s' %(i.id, c.authuser.id))
            return json.dumps({'error' : 'Error saving slideshow order'})

        return json.dumps({'success' : 'Success commiting slide change'})




        """
        s = getSlide(slideID)
        s.caption = caption
        s.title = title
        if not commit(s):
            log.error('Error commiting slide change for slideID = %s, caption = %s, title = %s, userID = %s' %(slideID, caption, title, c.authuser.id))
            return json.dumps({'error' : 'Error commiting slide change'})
        
        log.info('slideID = %s, title = %s, caption = %s' %(slideID, title, caption))
        return json.dumps({'success' : 'Success commiting slide change'})
        """
