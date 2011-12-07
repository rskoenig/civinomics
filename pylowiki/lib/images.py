import os, shutil, logging
from PIL import Image
from pylons import config

log = logging.getLogger(__name__)

def saveImage(name, hash, file, type):

    """ Save original to disk """
    savename = hash + '.png'
    if type == 'avatar':
        pathname = os.path.join(config['app_conf']['avatarDirectory'])
        fullpath = os.path.join(config['app_conf']['avatarDirectory'], savename)
    elif type == 'slideshow':
        pathname = os.path.join(config['app_conf']['slideshowDirectory'])
        fullpath = os.path.join(config['app_conf']['slideshowDirectory'], savename)
    elif type == 'govtSphere':
        pathname = os.path.join(config['app_conf']['govtSphereDirectory'])
        fullpath = os.path.join(config['app_conf']['govtSphereDirectory'], savename)
    try:
        f = open(fullpath, 'wb')
        shutil.copyfileobj(file, f)
        f.close()
        log.info('Successfully saved %s to disk', hash)
    except:
        log.info('Unable to save %s to %s with hash %s' % (name, fullpath, hash))

def resizeImage(name, hash, x, y, postfix, type):
    
    """ Resize the image with the given dimensions.  
        *Should* only be used to size down an image. """
    filename = hash + '.png'
    if type == 'avatar':
        fullpath = os.path.join(config['app_conf']['avatarDirectory'], filename)
        pathname = os.path.join(config['app_conf']['avatarDirectory'])
    elif type == 'slideshow':
        fullpath = os.path.join(config['app_conf']['slideshowDirectory'], filename)
        pathname = os.path.join(config['app_conf']['slideshowDirectory'])
    elif type == 'govtSphere':
        fullpath = os.path.join(config['app_conf']['govtSphereDirectory'], filename)
        pathname = os.path.join(config['app_conf']['govtSphereDirectory'])
    try:
        dims = x, y
        im = Image.open(fullpath)
        im.thumbnail(dims, Image.ANTIALIAS)
        im.save(pathname + '/' + hash + '.' + postfix, 'PNG')
        log.info('Successfully resized %s' % name)
    except:
        log.info('Unable to resize %s to %s with hash %s' % (name, fullpath, hash))
