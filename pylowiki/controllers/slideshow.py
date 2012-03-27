import logging

from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshop
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.slide import Slide, getSlide
from pylowiki.lib.db.slideshow import Slideshow, getSlideshow
from pylowiki.lib.db.imageIdentifier import getImageIdentifier

from pylowiki.lib.images import saveImage, resizeImage, numImagesInDirectory

#from pylowiki.lib.images import saveImage, resizeImage

log = logging.getLogger(__name__)

import pylowiki.lib.helpers as h
import simplejson as json
import os

class SlideshowController(BaseController):

    @h.login_required
    def addImageDisplay(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        if not c.w:
            h.flash('Could not find workshop!', 'error')
            return redirect('/')
        return render('/derived/uploadImages.html')
        #return render('/derived/test4.html')
    
    @h.login_required
    def addImageHandler(self, id1, id2):
        code = id1
        url = id2
        
        w = getWorkshop(code, url)
        s = getSlideshow(w['mainSlideshow_id'])
        if not w:
            h.flash('Could not find workshop!', 'error')
            return redirect('/')
        elif not s:
            h.flash('Could not find slideshow!', 'error')
            return redirect('/')
        
        if 'files[]' in request.params.keys():
            file = request.params['files[]']
            imageFile = file.file
            filename = file.filename
            identifier = 'slide'
            hash = saveImage(imageFile, filename, c.authuser, identifier, s)
            resizeImage(identifier, hash, 120, 65, 'thumbnail')
            resizeImage(identifier, hash, 835, 550, 'slideshow')
            
            identifier = 'slide'
            i = getImageIdentifier(identifier)
            directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
            savename = hash + '.orig'
            newPath = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, 'orig', savename)
            log.info('hash = %s' % hash)
            log.info('newPath = %s' % newPath)
            st = os.stat(newPath)
            l = []
            d = {}
            d['name'] = savename
            d['size'] = st.st_size
            d['url'] = 'http://www.civinomics.org:6626/images/%s/%s/orig/%s.orig' % (identifier, directoryNumber, hash)
            d['thumbnail_url'] = 'http://www.civinomics.org:6626/images/%s/%s/thumbnail/%s.thumbnail' % (identifier, directoryNumber, hash)
            d['delete_url'] = 'http://www.civinomics.org:6626/workshop/%s/%s/slideshow/delete/%s' %(w['urlCode'], w['url'], hash)
            d['delete_type'] = "DELETE"
            d['-'] = hash
            d['type'] = 'image/png'
            l.append(d)
            return json.dumps(l)
        """
        Return a JSON-encoded string of the following format:
        
        [
          {
            "name":"picture1.jpg",
            "size":902604,
            "url":"\/\/example.org\/files\/picture1.jpg",
            "thumbnail_url":"\/\/example.org\/thumbnails\/picture1.jpg",
            "delete_url":"\/\/example.org\/upload-handler?file=picture1.jpg",
            "delete_type":"DELETE"
          },
          {
            "name":"picture2.jpg",
            "size":841946,
            "url":"\/\/example.org\/files\/picture2.jpg",
            "thumbnail_url":"\/\/example.org\/thumbnails\/picture2.jpg",
            "delete_url":"\/\/example.org\/upload-handler?file=picture2.jpg",
            "delete_type":"DELETE"
          }
        ]

        """

    # Create a slide object.  That slide object will save the image and create the hash.  Then append the slide object to the slideshow container.
    def addSlideshow(self):
        numEntries = int(session['numEntries'])
        workshop_id = request.params['workshop_id']
        w = getWorkshopByID(workshop_id)
        slideshow = Slideshow(c.authuser, w)
        slideshow = getSlideshow(slideshow.s.id)
        w['mainSlideshow_id'] = slideshow.id
        slides = [] # Used for storing slide IDs
        identifier = 'slide'
        
        for i in range(1, numEntries):
            thisImage = request.POST['image%d'%i]
            thisCaption = request.params['caption%d'%i]
            thisTitle = request.params['title%s'%i]
            
            s = Slide(c.authuser, slideshow, thisTitle, thisCaption, thisImage.filename, thisImage.file)
            slides.append(s.s.id)
            
            if i == 1:
                w['mainImage_caption'] = thisCaption
                w['mainImage_title'] = thisTitle
                w['mainImage_hash'] = s.s['pictureHash']
                w['mainImage_postFix'] = 'orig'
                w['mainImage_identifier'] = identifier
                w['mainImage_id'] = s.s.id
        slideshow['slideshow_order'] = ','.join([str(item) for item in slides])
        commit(slideshow)
        commit(w)
        return redirect('/')
        """
            s = saveImage(c.authuser, thisImage.file, thisImage.filename, s.s, identifier)
            resizeImage(c.authuser, s, identifier, '.slideshow', 835, 550)
            resizeImage(c.authuser, s, identifier, '.thumbnail', 120, 65)
            
            thisSlide = Slide(c.authuser, s, )
            
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
        """
        
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
