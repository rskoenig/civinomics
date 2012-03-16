import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.workshop import getWorkshopByID
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.slide import Slide, getSlide
from pylowiki.lib.db.slideshow import Slideshow

from pylowiki.lib.images import saveImage, resizeImage

log = logging.getLogger(__name__)

import simplejson as json

class SlideshowController(BaseController):

    def addSlideshow(self):
        numEntries = int(session['numEntries'])
        workshop_id = request.params['workshop_id']
        w = getWorkshopByID(workshop_id)
        s = Slideshow(c.authuser, w)
        l = [] # Used for storing slide IDs
        identifier = 'slide'
        
        for i in range(1, numEntries):
            thisImage = request.POST['image%d'%i]
            thisCaption = request.params['caption%d'%i]
            thisTitle = request.params['title%s'%i]
            
            s = saveImage(c.authuser, thisImage.file, thisImage.filename, s.s, identifier)
            resizeImage(c.authuser, s, identifier, '.slideshow', 835, 550)
            resizeImage(c.authuser, s, identifier, '.thumbnail', 120, 65)
            
            if i == 1:
                w['mainImage_caption'] = thisCaption
                w['mainImage_title'] = thisTitle
                w['mainImage_hash'] = s['image_hash_%s' % identifier] 
                w['mainImage_postFix'] = s['image_postfix_%s' % identifier]
                w['mainImage_identifier'] = identifier
                w['mainImage_id'] = s.id
                
            l.append(s.id)
        
        slideshow_order = ','.join([str(id) for id in l])
        w['slideshow_order'] = slideshow_order
        s['slideshow_order'] = slideshow_order
        commit(w)
        commit(s)
        return redirect('/')
        
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
