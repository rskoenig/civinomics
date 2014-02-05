import logging

from pylons import request, response, session, tmpl_context as c
from pylons import config
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

import pylowiki.lib.db.workshop     as workshopLib
from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshop, isPublished
from pylowiki.lib.db.dbHelpers import commit
import pylowiki.lib.db.slide        as slideLib
import pylowiki.lib.db.slideshow        as slideshowLib
import pylowiki.lib.db.mainImage        as mainImageLib
from pylowiki.lib.db.imageIdentifier import getImageIdentifier
import pylowiki.lib.db.generic        as genericLib

from pylowiki.lib.images import saveImage, resizeImage, numImagesInDirectory

log = logging.getLogger(__name__)

import pylowiki.lib.helpers as h
import simplejson as json
import os

class SlideshowController(BaseController):

    def __before__(self, action, parentCode = None):
        if action in ['addImageHandler', 'edit', 'editPosition']:
            if parentCode is None:
                abort(404)
            parent = genericLib.getThing(parentCode)
            if parent.objType == 'workshop':
                c.w = workshopLib.getWorkshopByCode(parentCode)
                workshopLib.setWorkshopPrivs(c.w)
                if not c.w:
                    abort(404)
                if not (c.privs['admin'] or c.privs['facilitator']):
                    abort(404)
                
                c.slideshow = slideshowLib.getSlideshow(c.w)
                if not c.slideshow:
                    abort(404)
            elif parent.objType == 'resource':
                if 'workshopCode' in resource:
                    c.w = workshopLib.getWorkshopByCode(resource['workshopCode'])
                    workshopLib.setWorkshopPrivs(c.w)
                    if not (c.privs['admin'] or c.privs['facilitator']) and (resource.owner != c.authuser.id):
                        abort(404)
                    c.slideshow = resource

    @h.login_required
    def addImageHandler(self, parentCode, parentURL):
        allSlides = slideshowLib.getAllSlides(c.slideshow)
        
        if 'files[]' in request.params.keys():
            file = request.params['files[]']
            imageFile = file.file
            filename = file.filename
            identifier = 'slide'
            
            slide = slideLib.Slide(c.authuser, c.slideshow, 'Sample caption', filename, imageFile, '1')
            
            i = getImageIdentifier(identifier)
            directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
            hash = slide['pictureHash']
            savename = hash + '.png'
            # This bit is a bit wonky to avoid a security-based race condition wherein we check if the file exists (it does),
            # it gets modified, and then we use the file, still assuming it's the same.
            size = 0
            try:
                newPath = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, 'orig', savename)
                with open(newPath):
                    st = os.stat(newPath)
                    size = st.st_size
            except IOError:
                abort(500)
            l = []
            d = {}
            d['name'] = savename
            d['size'] = size
            if 'site_base_url' in config:
                siteURL = config['site_base_url']
            else:
                siteURL = 'http://civinomics.com'
            
            d['url'] = '%s/images/%s/%s/orig/%s.png' % (siteURL, identifier, directoryNumber, hash)
            d['thumbnail_url'] = '%s/images/%s/%s/thumbnail/%s.png' % (siteURL, identifier, directoryNumber, hash)
            d['delete_url'] = '%s/workshop/%s/%s/slideshow/delete/%s' %(siteURL, c.w['urlCode'], c.w['url'], hash)
            d['delete_type'] = "DELETE"
            d['-'] = hash
            d['type'] = 'image/png'
            l.append(d)
            
            if len(allSlides) == 1:
                if allSlides[0]['filename'] == 'supDawg.png':
                    s = allSlides[0]
                    s['deleted'] = "1"
                    s['slideshow_order'] = slide.id
                    commit(s)
                mainImageLib.setMainImage(c.authuser, c.w, slide)
            aTitle = 'Upload complete. Please add a caption to new images.'
            if not isPublished(c.w):
                aTitle += ' See your changes by clicking on the preview button above.'
            session['confTab'] = "slideshow"
            alert = {'type':'success'}
            alert['title'] = aTitle
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
            result = {'files': l}
            return json.dumps(result)
        
    @h.login_required
    def edit(self, parentCode, parentURL):
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
        
        slide = slideLib.forceGetSlide(slide_id)
        slideshow = slideshowLib.getSlideshowByCode(slide['slideshowCode'])
        
        slide[slideField] = content
        commit(slide)
        
        return request.params['value']
        return json.dumps({'content':content})
        
    @h.login_required
    def editPosition(self, parentCode, parentURL):
        """
            Gets called whenever the slideshow order is changed.
            Gets called once per column.
            Publishes and unpublishes slides (sets the 'deleted' attribute)
        """
        allSlides = slideshowLib.getAllSlides(c.slideshow)
        published = 0
        for s in allSlides:
            if s['deleted'] == 0:
                published += 1
        value = request.params['slides']
        log.info(value)
        if value == '_published' or value == '_unpublished':
            return
        
        value = value.split('_')
        order = '&' + value[0]
        state = value[1] # published or unpublished
        order = [item for item in order.split('&portlet[]=')][1:]
        
        if state == 'unpublished':
            for item in order:
                slide = slideLib.forceGetSlide(int(item))
                if int(slide['deleted']) == 0 and published > 1:
                    slide['deleted'] = '1'
                    commit(slide)
        elif state == 'published':
            firstSlide = slideLib.forceGetSlide(int(order[0]))
            slideshow = slideshowLib.getSlideshowByCode(firstSlide['slideshowCode'])
            
            # If we change the initial image
            if firstSlide.id != int(slideshow['slideshow_order'].split(',')[0]):
                mainImageLib.setMainImage(c.authuser, c.w, firstSlide)
            else:
                pass
            
            for item in order:
                slide = slideLib.forceGetSlide(item)
                if int(slide['deleted']) == 1:
                    slide['deleted'] = '0'
                    commit(slide)
            
            slideshow['slideshow_order'] = ','.join(map(str, order))
            commit(slideshow)
            
