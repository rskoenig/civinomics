import logging

from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshop
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.slide import Slide, getSlide, forceGetSlide
from pylowiki.lib.db.slideshow import Slideshow, getSlideshow, getAllSlides
from pylowiki.lib.db.imageIdentifier import getImageIdentifier

from pylowiki.lib.images import saveImage, resizeImage, numImagesInDirectory, isImage

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
    
    @h.login_required
    def addImageHandler(self, id1, id2):
        code = id1
        url = id2
        
        w = getWorkshop(code, url)
        s = getSlideshow(w['mainSlideshow_id'])
        allSlides = getAllSlides(s.id)
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
            
            isAnImage = isImage(imageFile)
            if isAnImage == False:
                return
            else:
                imageFile.seek(0)

            slide = Slide(c.authuser, s, 'Sample title', 'Sample caption', filename, imageFile, '1')
                      
            i = getImageIdentifier(identifier)
            directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
            hash = slide.s['pictureHash']
            savename = hash + '.orig'
            newPath = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, 'orig', savename)
            st = os.stat(newPath)
            l = []
            d = {}
            d['name'] = savename
            d['size'] = st.st_size
            if 'site_base_url' in config:
                siteURL = config['site_base_url']
            else:
                siteURL = 'http://www.civinomics.com'
            
            d['url'] = '%s/images/%s/%s/orig/%s.orig' % (siteURL, identifier, directoryNumber, hash)
            d['thumbnail_url'] = '%s/images/%s/%s/thumbnail/%s.thumbnail' % (siteURL, identifier, directoryNumber, hash)
            d['delete_url'] = '%s/workshop/%s/%s/slideshow/delete/%s' %(siteURL, w['urlCode'], w['url'], hash)
            d['delete_type'] = "DELETE"
            d['-'] = hash
            d['type'] = 'image/png'
            l.append(d)
            
            if len(allSlides) == 1:
                if allSlides[0]['filename'] == 'supDawg.png':
                    s = allSlides[0]
                    s['deleted'] = "1"
                    commit(s)
            session['confTab'] = "tab2"
            alert = {'type':'success'}
            alert['title'] = 'Upload complete. Please add a title and caption to new slideshow images below.'
            session['alert'] = alert
            session.save()
            session.save() 
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
    @h.login_required
    def editSlideshowDisplay(self, id1, id2):
        code = id1
        url = id2
        
        c.w = getWorkshop(code, url)
        slideshow = getSlideshow(c.w['mainSlideshow_id'])
        l = []
        """
        for slide_id in [int(item) for item in slideshow['slideshow_order'].split(',')]:
            l.append(getSlide(slide_id))
        
        c.slideshow = l
        """
        c.slideshow = getAllSlides(slideshow.id)
        c.title = 'Edit slideshow'
        #c.colors = ['yellow', 'red', 'blue', 'white', 'orange', 'green']
        return render('/derived/editSlideshow.html')

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
        Gets called whenever an edit to the title or caption of a slide is made
        
        content        ->    The modified value that a user types in
        slideparams    ->    A string separated with an underscore of the form slideID_slideField.  
            slideID    ->    The Thing id of a slide
            slideField ->    Either 'title' or 'caption'
    """
    @h.login_required
    def edit(self):
        content = request.params['value']
        slideparams = request.params['id']
        slideparams = slideparams.split('_')
        slide_id = slideparams[0]
        slideField = slideparams[1] # either title or caption
        
        slide = forceGetSlide(slide_id)
        slideshow = getSlideshow(int(slide['slideshow_id']))
        
        if slide_id == int(slideshow['slideshow_order'].split(',')[0]):
            w = getWorkshopByID(int(slideshow['workshop_id']))
            key = 'mainImage_' + slideField
            w[key] = content
            commit(w)
        
        slide[slideField] = content
        commit(slide)
        
        return request.params['value']
        return json.dumps({'content':content})
        
    """
        Gets called whenever the slideshow order is changed.
        Gets called once per column.
        Publishes and unpublishes slides (sets the 'deleted' attribute)
    """
    def editPosition(self):
        
        value = request.params['slides']
        if value == '_published' or value == '_unpublished':
            return
        
        value = value.split('_')
        order = '&' + value[0]
        log.info('order = %s' % order)
        state = value[1] # published or unpublished
        
        order = [item for item in order.split('&portlet[]=')][1:]
        log.info('order: %s'%order)
        
        if state == 'unpublished':
            for item in order:
                slide = forceGetSlide(int(item))
                if int(slide['deleted']) == 0:
                    slide['deleted'] = '1'
                    commit(slide)
        elif state == 'published':
            firstSlide = forceGetSlide(int(order[0]))
            slideshow = getSlideshow(firstSlide['slideshow_id'])
            w = getWorkshopByID(int(slideshow['workshop_id']))
            
            # If we change the initial image
            if firstSlide.id != int(slideshow['slideshow_order'].split(',')[0]):
                w['mainImage_directoryNum'] = firstSlide['directoryNumber']
                w['mainImage_hash'] = firstSlide['pictureHash']
                w['mainImage_id'] = firstSlide.id
                commit(w)
            else:
                pass
            
            for item in order:
                slide = forceGetSlide(item)
                if int(slide['deleted']) == 1:
                    slide['deleted'] = '0'
                    commit(slide)
            
            slideshow['slideshow_order'] = ','.join(map(str, order))
            commit(slideshow)
            
        
        
        """ Used for the inettuts implementation of the iGoogle interface
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
            
        log.info(ids)
        for i in range(len(ids)):
            s = getSlide(ids[i])
            s['title'] = titles[i]
            s['caption'] = captions[i]
            if not commit(s):
                log.error('Error commiting slide change for slideID = %s, caption = %s, title = %s, userID = %s' %(ids[i], captions[i], titles[i], c.authuser.id))
                return json.dumps({'error' : 'Error commiting slide change'})
            #log.info('User %s successfully updated: slideID = %s, title = %s, caption = %s' %(c.authuser.id, ids[i], titles[i], captions[i]))

        mainSlide = getSlide(ids[0])
        slideshow = getSlideshow(mainSlide['slideshow_id'])
        #log.info('s.keys() = %s'%s.keys())
        order = ','.join(map(str, ids)) # Save the new order as a comma-separated list of slide IDs
        slideshow['slideshow_order'] = order
        
        
        w = getWorkshopByID(int(slideshow['workshop_id']))
        w['mainImage_id'] = ids[0]
        w['mainImage_caption'] = captions[0]
        w['mainImage_title'] = titles[0]
        w['mainImage_hash'] = mainSlide['pictureHash'] 
        w['mainImage_postFix'] = 'slideshow'
        w['mainImage_directoryNum'] = mainSlide['directoryNumber']
        commit(w)
        
        if not commit(slideshow):
            log.error('Error changing slideshow order for slideshow = %s, user = %s' %(s.id, c.authuser.id))
            return json.dumps({'error' : 'Error saving slideshow order'})

        return json.dumps({'success' : 'Success commiting slide change'})
        """

