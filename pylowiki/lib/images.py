import os, shutil, logging, re
from PIL import Image
from time import time
from hashlib import md5

from pylons import config
#from pylowiki.model import Thing
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.imageIdentifier import ImageIdentifier, getImageIdentifier

log = logging.getLogger(__name__)
numImagesInDirectory = 30000
   
# Save images into a subdirectory identified primarily by the identifier and secondarily by the postfix
# Example: identifier = 'slide', postfix = 'thumbnail'.  The directory is /.../images/slide/thumbnail/filename.thumbnail
def resizeImage(identifier, hash, x, y, postfix):
    i = getImageIdentifier(identifier)
    directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
    
    origPathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber,'orig')
    origFullpath = origPathname + '/%s.orig' %(hash)
    
    try:
        dims = x, y
        im = Image.open(origFullpath)
        im.thumbnail(dims, Image.ANTIALIAS)
        
        pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, postfix)
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        
        quality = 80
        im.save(pathname + '/' + hash + '.' + postfix, 'JPEG', quality=quality)
        #log.info('Successfully resized %s' % hash)
        return True
    except:
        return False
    
# Save an image to disk
# Directories are created based on the identifier that gets passed in
# Each identifier object contains an 'imageNum' field that is a running tally of
# all images that have the same identifier.  When we get to 30k images in a
# directory (via integer division), we create a new directory and save images in there.
def saveImage(image, filename, user, identifier, thing):
    hash = _generateHash(filename, user)

    if not getImageIdentifier(identifier):
        i = ImageIdentifier(identifier)
    i = getImageIdentifier(identifier)
    i['numImages'] = int(i['numImages']) + 1 
    directoryNumber = str(int(i['numImages']) / numImagesInDirectory)

    pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, 'orig')
    savename = hash + '.orig'
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    
    fullpath = os.path.join(pathname, savename)
    
    thing['directoryNumber'] = directoryNumber
    commit(thing)
    
    try:
        f = open(fullpath, 'wb')
        shutil.copyfileobj(image, f)
        f.close()
        #log.info('Successfully saved %s to disk as %s', filename, savename)
        return hash
    except:
        log.info('Unable to save to %s with hash %s' % (fullpath, hash))
        return False

def _generateHash(filename, user):
    s = '%s_%s_%s' %(filename, user['email'], int(time()))
    return md5(s).hexdigest()
    
    
def makeSurveyThumbnail(filename, directory, x, y, postfix):
    """
        Creates a thumbnail from an image at the specified location.  Saves the thumbnail in the same
        directory as the original image.  Images for thumbnails are separate images, named accordingly.
        
        inputs:     filename     ->    The filename of the image to be resized.  Ex: flash.png
                    directory    ->    The full directory path where the image is saved. Ex: /home/edolfo/images/
                    x            ->    The width of the thumbnail
                    y            ->    The height of the thumbnail
                    postfix      ->    The postfix to be used when saving the thumbnail.  Ex: thumbnail
                    
        Outputs:    True if everything went according to plan, False otherwise
        
        Example:    result = makeSurveyThumbnail('flash.png', '/home/edolfo/images/', 50, 50, 'thumbnail')
                    If everything goes according to plan, the original file 'flash.png' remains in:
                        /home/edolfo/images/flash.jpg
                    And the thumbnail of size 50 pixels by 50 pixels is saved in:
                        /home/edolfo/images/flash.thumbnail
                    And the value for 'result' is 'True'.
                    Additionally, the naming scheme for the original image and the image used for the thumbnail is:
                    Original:        EastsideProject.001.png
                    Thumbnail:       EastsideProject.thumbnail.001.png
    """
    filename = filename.split('.')
    filename.insert(1, 'thumbnail')
    filename = '.'.join(filename)
    fullpath = os.path.join(directory, filename)
    filenameSplit = filename.split('.')
    if len(filenameSplit) > 1:
        filenameSplit.pop()
    saveFilename = '.'.join(filenameSplit)
    try:
        dims = x, y
        #log.info('attempting to open %s' % fullpath)
        im = Image.open(fullpath)
        im.thumbnail(dims, Image.ANTIALIAS)
        savepath = os.path.join(directory, '%s.%s'%(saveFilename, postfix))
        #log.info('saving to %s' % savepath)
        im.save(savepath, 'PNG')
        return True
    except:
        return False
    
def smartCrop(directory, filename):
    """
         Takes an image at the path specified by 'filepath' and scane each row for transparent pixels.
         If an entire row of transparent pixels is found, crops the image so that it contains only rows
         above the transparent row, then saves over the original image.
    """
    image = Image.open(os.path.join(directory, filename))
    image.convert("RGBA") # Convert this to RGBA if possible
    pixel_data = image.load()
    
    ROW_LENGTH = len(xrange(image.size[0]))
    if image.mode == 'RGBA':
        found = False
        for y in xrange(image.size[1]):
            for x in xrange(image.size[0]):
                if pixel_data[x, y][3] > 0:
                    # Go to next row
                    break
                else:
                    if x == ROW_LENGTH - 1:
                        found = True
            if found:
                break
                
        if found:
            # We can crop
            box = (0, 0, 1024, y)
            region = image.crop(box)
            region.save(os.path.join(directory, filename))

def cropHeader(directory, filename, cropAmount):
    try:
        image = Image.open(os.path.join(directory, filename))
        #The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
        box = (0, cropAmount, 1024, 768)
        region = image.crop(box)
        region.save(os.path.join(directory, filename))
    except:
        return False
    
def cropHeight(directory, filename, cropAmount, header):
    try:
        image = Image.open(os.path.join(directory, filename))
        #The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
        if header:
            box = (0, 0, 1024, cropAmount - 55)
        else:
            box = (0, 0, 1024, cropAmount)
        region = image.crop(box)
        region.save(os.path.join(directory, filename))
    except:
        return False