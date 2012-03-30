import os, shutil, logging, re
from PIL import Image
from time import time
from hashlib import md5

from pylons import config
from pylowiki.model import Blob
from pylowiki.lib.db.dbHelpers import commit

log = logging.getLogger(__name__)

"""
    Saves an image to a Thing's blob property.  Sets the image as the main image, given an identifier.
    
    owner        ->    a Thing object representing a user
    file         ->    the image itself
    filename     ->    the image's original filename
    identifier   ->    Used to indicate what kind of image is being saved (e.g. slide, avatar, splash, logo, etc...)
"""
"""
def saveImage(owner, file, filename, thing, identifier):
    keyNumImages = 'numImages_%s' % identifier
    keyFilename = 'image_filename_%s' % identifier
    keyBlob = 'image_%s' % identifier
    
    if keyNumImages not in thing.keys():
        # Set new entries to main
        
        thing[keyNumImages] = 1
        counter = 1
        thing[keyFilename] = filename
        thing.blob[keyBlob] = Blob(keyBlob, file)
        
    else:
        
        numImages = thing[keyNumImages]
        thing[keyNumImages] += 1
        oldFilename = thing[keyFilename]
        oldBlob = thing.blob[keyBlob].value
        
        keyOldFilename = '%s_%s' % (keyFilename, numImages)
        keyOldBlob =  '%s_%s' % (keyBlob, numImages)
        
        # Update the list; take main image and add to the end
        thing[keyOldFilename] = oldFilename
        thing.blob[keyOldBlob] = Blob(keyOldBlob, oldBlob)
        
        thing[keyFilename] = filename
        thing.blob[keyBlob].value = file
    
    if commit(thing):
        log.info('Successfully saved image %s to db' % filename)
        return thing
    else:
        log.info('Failed to save image %s submitted by user %s to db' %(filename, owner.id))
        return False
    
    """

"""
    Resizes an existing image.  Saves a new version of that image.  *Should* only be used to size down.
    Assumes an image already exists and is linked to the Thing via the blob property.
    
    owner        ->    A user Thing
    thing        ->    The Thing whose image you are resizing
    x            ->    The image's new width, in number of pixels
    y            ->    The image's new height, in number of pixels
    identifier   ->    A string, used to identify the image type (e.g. thumbnail, original, etc...)
"""

"""
def resizeImage(owner, thing, x, y, identifier):
    #newImage = Thing('image', owner.id)
    
    try:
        oldImage = thing.blob['file']
        im = Image.open(oldImage)
        
        # PIL-specific commands
        dims = x, y
        im.thumbnail(dims, Image.ANTIALIAS)
        im.save(oldImage, 'PNG')
        
        # Retain original image(s), set resized image as main image
        # Here we will take the current image (thing.blob['image'] and append that to our list of images (thing.blob['image_n'])
        # Then we set the resized image to be the current image.
        counter = int(thing['numImages'])
        keyTo = 'image_%d_%s' % (counter - 1, identifier) # counter - 1 so we begin at 0
        keyFrom = 'image_%s' % identifier
        thing.blob[keyTo] = Blob(key, thing.blob[keyFrom])
        
        # TODO: finish from here onwards
        key = 'image_%d_filename' %counter
        thing[key] = thing['image_filename'] 
        
        thing.blob['image'] = Blob('image', oldImage)
        thing['filename'] = thing[key]
        thing['numImages'] += 1
        newImage['filename'] = image['filename']
        return newImage
    except:
        log.info('Unable to resize %s from user %s'%(filename, owner.id))
        return False
"""


"""
def resizeImage(owner, thing, identifier, postfix, x, y):
    # Resize the image with the given dimensions.  
    #    *Should* only be used to size down an image.
    # Assumes saveImage() has already been called.  Only works on the main image, given the proper identifier. 
    
    keyNumImages = 'numImages_%s' % identifier
    keyFilename = 'image_filename_%s' % identifier
    keyHash = 'image_hash_%s' % identifier
    keyPostfix = 'image_postfix_%s' % identifier
    keyOwner = 'image_owner_%s' % identifier
    
    hash = thing[keyHash]
    oldPostfix = thing[keyPostfix]
    pathname = os.path.join(config['app_conf']['imageDirectory'], identifier)
    #fullpath = os.path.join(pathname, hash oldPostfix)
    fullpath = pathname + '/%s%s' %(hash, oldPostfix)
    
    try:
        dims = x, y
        im = Image.open(fullpath)
        im.thumbnail(dims, Image.ANTIALIAS)
        im.save(pathname + '/' + hash + postfix, 'PNG')
        log.info('Successfully resized %s' % hash)
        return True
    
    except:
        log.info('Unable to resize %s' % fullpath)
        raise
        return False
"""    
   
# Save images into a subdirectory identified primarily by the identifier and secondarily by the postfix
# Example: identifier = 'slide', postfix = 'thumbnail'.  The directory is /.../images/slide/thumbnail/filename.thumbnail
def resizeImage(identifier, hash, x, y, postfix):
    origPathname = os.path.join(config['app_conf']['imageDirectory'], identifier, 'orig')
    origFullpath = origPathname + '/%s.orig' %(hash)
    
    try:
        dims = x, y
        im = Image.open(origFullpath)
        im.thumbnail(dims, Image.ANTIALIAS)
        
        pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, postfix)
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        
        im.save(pathname + '/' + hash + '.' + postfix, 'PNG')
        log.info('Successfully resized %s' % hash)
        return True
    except:
        return False
    
# Save an image to disk
# Directories are created based on the identifier that gets passed in
def saveImage(image, filename, user, identifier):
    hash = _generateHash(filename, user)

    pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, 'orig')
    savename = hash + '.orig'
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    
    fullpath = os.path.join(pathname, savename)
    
    try:
        f = open(fullpath, 'wb')
        shutil.copyfileobj(image, f)
        f.close()
        log.info('Successfully saved %s to disk as %s', filename, savename)
        return hash
    except:
        log.info('Unable to save to %s with hash %s' % (fullpath, hash))
        return False

"""
# Save an image to disk
# Directories are created based on the identifier that gets passed in
def saveImage(owner, image, filename, thing, identifier):    
    hash = _generateHash(filename, owner)
    postfix = '.orig'
    savename = hash + postfix
    keyNumImages = 'numImages_%s' % identifier
    keyFilename = 'image_filename_%s' % identifier
    keyHash = 'image_hash_%s' % identifier
    keyPostfix = 'image_postfix_%s' % identifier
    keyOwner = 'image_owner_%s' % identifier
    
    if keyNumImages not in thing.keys():
        thing[keyNumImages] = 1
        thing[keyFilename] = filename
        thing[keyHash] = hash
        thing[keyPostfix] = postfix
        thing[keyOwner] = owner.id
    else:
        numImages = thing[keyNumImages]
        thing[keyNumImages] += 1
        oldFilename = thing[keyFilename]
        oldHash = thing[keyHash]
        oldPostfix = thing[keyPostfix]
        oldOwner = thing[keyOwner]
        
        # Grab the head of the list
        keyOldFilename = '%s_%s' % (keyFilename, numImages)
        keyOldHash = '%s_%s' %(keyHash, numImages)
        keyOldPostfix = '%s_%s' %(keyPostfix, numImages)
        keyOldOwner = '%s_%s' %(keyOwner, numImages)
        
        # Update the list's tail with what is currently the list's head
        thing[keyOldFilename] = oldFilename
        thing[keyOldHash] = oldHash
        thing[keyOldPostfix] = oldPostfix
        thing[keyOldOwner] = oldOwner
        
        # Update the head of the list
        thing[keyFilename] = filename
        thing[keyHash] = hash
        thing[keyPostfix] = postfix
        thing[keyOwner] = owner.id
        
    pathname = os.path.join(config['app_conf']['imageDirectory'], identifier)
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    
    fullpath = os.path.join(pathname, savename)
    
    try:
        f = open(fullpath, 'wb')
        shutil.copyfileobj(image, f)
        f.close()
        log.info('Successfully saved %s to disk as %s', filename, savename)
        commit(thing)
        return thing
    except:
        log.info('Unable to save %s to %s with hash %s' % (name, fullpath, hash))
        return False
"""

def _generateHash(filename, user):
    s = '%s_%s_%s' %(filename, user['email'], int(time()))
    return md5(s).hexdigest()
    