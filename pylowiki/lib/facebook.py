import os, logging, re

import urllib

from pylons import session, config, request, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.images      as imageLib

log = logging.getLogger(__name__)


"""
    General workflow for facebook library:

"""

def saveFacebookImage(imageLink, **kwargs):
    """ When a user registers or logs in with their facebook identity, their profile picture
    is available as a link. In order to standardize resolution and size of this picture, this 
    function will save cropped versions of it to disk for use as the user's current avatar. """
    # there are various ways to verify this is an image. can we trust the link provided by
    # facebook to be a valid image? 
    
    #if c.authuser.id != c.user.id:
    #    abort(404)
    log.info("testconf: %s"%config['app_conf']['imageDirectory'])
    # /glyphicons_pro/glyphicons/png/
    # glyphicons_003_user.png

    #savename = imageHash = imageLib.generateHash(fileHolderName, c.authuser)
    #sampleDir = config['app_conf'] .. '/images/glyphicons_pro/glyphicons/png/'
    #pathname = os.path.join(config['app_conf']['avatarDirectory'])
    #    fullpath = os.path.join(config['app_conf']['imageDirectory'], savename)
    #    file = open(fullpath, 'wb')
    #    shutil.copyfileobj(picture.file, file)
    #    picture.file.close()
    #    file.close()
    
    log.info("make a place for the image")
    log.info("current dir %s"%os.path)
    glyphName = '/glyphicons_pro/glyphicons/png/glyphicons_003_user.png'
    fullpath = "%s%s"%(config['app_conf']['imageDirectory'], glyphName)
    log.info("fullPath %s" % fullpath)
    fileHolder = open(fullpath,"r")
    image = imageLib.openImage(fileHolder)
    fileHolderName = "glyphicons_003_user"
    fileHolderFile = fileHolder.file
    image = imageLib.openImage(fileHolderFile)
    if not image:
        abort(404) # Maybe make this a json response instead
    imageHash = imageLib.generateHash(fileHolderName, c.authuser)
    image = imageLib.saveImage(image, imageHash, 'avatar', 'orig', thing = c.authuser)
    log.info("by saving a copy of our default avatar")
    log.info("now c.authuser has the directoryNum_avatar key we can work with")
    # this will be called from login or register in the controller folder
    log.info("in saveFacebookImage %s" % imageLink)
    # retrieve image
    filename = 'facebookAvatar'
    log.info("c authu: %s" % str(c.authuser) )
    imageHash = imageLib.generateHash(filename, c.authuser)

    # need to have a directory for this guy
    #fileLocation =('/images/%s.png' % imageHash )
    fileLocation =('/images/avatar/%s/avatar/%s.png' % (c.authuser['directoryNum_avatar'], imageHash) )
    #os.chdir('/images/avatar/%s/avatar/%s.png' % (c.authuser['directoryNum_avatar'], imageHash) )
    
    os.chdir(fileLocation)
    testImg = "http://thehomie.com/images/Napali.png"

    imageFile=urllib.URLopener()
    imageFile.retrieve(testImg,filename)  



    image = imageLib.openImage(imageFile)

    if not image:
        abort(404) # Maybe make this a json response instead

    log.info("in saveFacebookImage its a pic")
    # do i use this file's name or just make a default name?
        # with default name it's easier to delete, though file type may vary
        # with image name it's just that, a name for this image. the image should replace whatever 
        # may already be on this server for the user's profile pic

    
    image = imageLib.saveImage(image, imageHash, 'avatar', 'orig', thing = c.authuser)
    
    width = min(image.size)
    x = 0
    y = 0
    if 'width' in kwargs:
        width = int(kwargs['width'])
    if 'x' in kwargs:
        x = int(kwargs['x'])
    if 'y' in kwargs:
        y = int(kwargs['y'])
    dims = {'x': x, 
            'y': y, 
            'width':width,
            'height':width}
    clientWidth = -1
    clientHeight = -1
    if 'clientWidth' in kwargs:
        clientWidth = kwargs['clientWidth']
    if 'clientHeight' in kwargs:
        clientHeight = kwargs['clientHeight']
    image = imageLib.cropImage(image, imageHash, dims, clientWidth = clientWidth, clientHeight = clientHeight)
    image = imageLib.resizeImage(image, imageHash, 200, 200)
    image = imageLib.saveImage(image, imageHash, 'avatar', 'avatar')
    image = imageLib.resizeImage(image, imageHash, 100, 100)
    image = imageLib.saveImage(image, imageHash, 'avatar', 'thumbnail')
    
    #jsonResponse =  {'files': [
    #    {
    #        'name':filename,
    #        'thumbnail_url':'/images/avatar/%s/avatar/%s.png' %(c.authuser['directoryNum_avatar'], imageHash)
    #    }
    #]}
    #return json.dumps(jsonResponse)
    thumbnail_url = '/images/avatar/%s/avatar/%s.png' %(c.authuser['directoryNum_avatar'], imageHash)
    return fileLocation
