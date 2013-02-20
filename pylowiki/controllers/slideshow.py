import logging

from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.workshop     as workshopLib
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshop
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.slide import Slide, getSlide, forceGetSlide
from pylowiki.lib.db.slideshow import Slideshow, getSlideshow, getAllSlides
import pylowiki.lib.db.slideshow        as slideshowLib
from pylowiki.lib.db.imageIdentifier import getImageIdentifier

from pylowiki.lib.images import saveImage, resizeImage, numImagesInDirectory, isImage

log = logging.getLogger(__name__)

import pylowiki.lib.helpers as h
import simplejson as json
import os

class SlideshowController(BaseController):

    def __before__(self, action, workshopCode = None):
        if action in ['addImageHandler']:
            if workshopCode is None:
                abort(404)
            c.w = workshopLib.getWorkshopByCode(workshopCode)
            if not c.w:
                abort(404)
            c.slideshow = getSlideshow(c.w)
            if not c.slideshow:
                abort(404)

    @h.login_required
    def addImageHandler(self, workshopCode, workshopURL):
        allSlides = getAllSlides(c.slideshow.id)
        
        if 'files[]' in request.params.keys():
            file = request.params['files[]']
            imageFile = file.file
            filename = file.filename
            identifier = 'slide'
            
            if not isImage(imageFile):
                abort(404)
            imageFile.seek(0)

            slide = Slide(c.authuser, c.slideshow, 'Sample caption', filename, imageFile, '1')
            
            i = getImageIdentifier(identifier)
            directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
            hash = slide['pictureHash']
            savename = hash + '.jpg'
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
            d['delete_url'] = '%s/workshop/%s/%s/slideshow/delete/%s' %(siteURL, c.w['urlCode'], c.w['url'], hash)
            d['delete_type'] = "DELETE"
            d['-'] = hash
            d['type'] = 'image/png'
            l.append(d)
            
            if len(allSlides) == 1:
                if allSlides[0]['filename'] == 'supDawg.png':
                    s = allSlides[0]
                    s['deleted'] = "1"
                    commit(s)
                    w['mainImage_hash'] = slide.s['pictureHash']
                    w['mainImage_directoryNum'] = directoryNumber
                    w['mainImage_postFix'] = 'orig'
                    w['mainImage_identifier'] = identifier
                    w['mainImage_id'] = slide.id
                    s['slideshow_order'] = slide.id
                    commit(s)       
            session['confTab'] = "tab4"
            alert = {'type':'success'}
            alert['title'] = 'Upload complete. Please add a title and caption to new slideshow images below.'
            session['alert'] = alert
            session.save()
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
            return json.dumps(l)
        
    @h.login_required
    def edit(self):
        """
            Gets called whenever an edit to the title or caption of a slide is made
            
            content        ->    The modified value that a user types in
            slideparams    ->    A string separated with an underscore of the form slideID_slideField.  
                slideID    ->    The Thing id of a slide
                slideField ->    Either 'title' or 'caption'
        """
        content = request.params['value']
        slideparams = request.params['id']
        slideparams = slideparams.split('_')
        slide_id = slideparams[0]
        slideField = slideparams[1] # either title or caption
        
        slide = forceGetSlide(slide_id)
        slideshow = slideshowLib.getSlideshowByCode(slide['slideshowCode'])
        
        if slide_id == int(slideshow['slideshow_order'].split(',')[0]):
            w = getWorkshopByID(int(slideshow['workshop_id']))
            key = 'mainImage_' + slideField
            w[key] = content
            commit(w)
        
        slide[slideField] = content
        commit(slide)
        
        return request.params['value']
        return json.dumps({'content':content})
        
    @h.login_required
    def editPosition(self):
        """
            Gets called whenever the slideshow order is changed.
            Gets called once per column.
            Publishes and unpublishes slides (sets the 'deleted' attribute)
        """
        value = request.params['slides']
        if value == '_published' or value == '_unpublished':
            return
        
        value = value.split('_')
        order = '&' + value[0]
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
            slideshow = slideshowLib.getSlideshowByCode(firstSlide['slideshowCode'])
            w = workshopLib.getWorkshopByCode(slideshow['workshopCode'])
            
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
            
