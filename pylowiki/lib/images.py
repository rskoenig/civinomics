import os, shutil, logging, re
from PIL import Image
from time import time
from hashlib import md5

from pylons import config
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.imageIdentifier import ImageIdentifier, getImageIdentifier

log = logging.getLogger(__name__)
numImagesInDirectory = 30000

"""
    General workflow for new images:
    1)  Given a file 'file', open image with openImage(file).  
        This checks that the file is indeed an image, and returns a PIL.Image object.  Call this object 'imObj'
    2)  Save original image with saveImage(imObj).  The identifier will depend on the overall function (e.g. 'avatar', 'background', 'slide', etc...)
        The sub identifier depends on the specific function (e.g. 'thumbnail', 'orig', 'slideshow').  Here you will want to save as 'orig'.
    3)  Process imgObj as necessary with resizeImage() and cropImage()
    4)  Save the modified imgObj with the same identifier, but different sub identifier (e.g. identifier = 'avatar', sub identifier = 'thumbnail')

"""


def resizeImage(identifier, hash, x, y, postfix, **kwargs):
    """
        Save images into a subdirectory identified primarily by the identifier and secondarily by the postfix
        Example: identifier = 'slide', postfix = 'thumbnail'.  The directory is /.../images/slide/thumbnail/filename.jpg
        
        optional arguments:
        preserveAspectRatio         ->      Exactly as it sounds.  Boolean value.
        
    """
    
    i = getImageIdentifier(identifier)
    directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
    
    origPathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber,'orig')
    origFullpath = origPathname + '/%s.png' %(hash)
    
    try:
        im = Image.open(origFullpath)
        ratio = 1
        dims = (x, y)
        if x == 99999 and y == 99999:
            dims = im.size
        if 'preserveAspectRatio' in kwargs:
            if kwargs['preserveAspectRatio'] == True:
                maxwidth = x
                maxheight = y
                width, height = im.size
                ratio = min(float(maxwidth)/width, float(maxheight)/height)
                dims = (int(im.size[0] * ratio), int(im.size[1] * ratio))
        pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, postfix)
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        
        im.save(pathname + '/' + hash + '.png' , 'PNG')
        return True
    except:
        return False
        
def cropImage(image, imageHash, dims, **kwargs):
    """
        If cropImage() fails at any step, it will return False.
        
        inputs:
            image       ->  An Image object obtained by opening the image as PIL.Image.open()
            imageHash   ->  A unique identifier for each image.  Used here for logging and debugging purposes
            dims        ->  A dictionary in the following format:
                            {'x': int,
                            'y': int,
                            'width': int,
                            'height': int}
                            The 'x' and 'y' values indicate the top-left corner where the cropping starts.
        outputs:
            image       ->  The modified Image object that was passed in.
    """
    
    try:
        x = dims['x']
        y = dims['y']
        width = dims['width']
        height = dims['height']
    except KeyError as e:
        log.error('lib/images/cropImage(): dims dict was lacking key %s' % e)
        return False
    
    try:
        box = (x, y, width, height)
        region = image.crop(box)
        return region
    except Exception as e:
        log.error('lib/images/cropImage(): unable to crop image with hash %s; error given was %s' % (imageHash, e))
        return False
    
def getImageLocation(slide):
    # Given a slide, return the image file's location on disk
    imgHash = slide['pictureHash']
    identifier = getImageIdentifier('slide')
    directoryNumber = str(int(identifier['numImages']) / numImagesInDirectory)
    origPathname = os.path.join(config['app_conf']['imageDirectory'], 'slide', directoryNumber,'orig')
    if 'format' in slide.keys():
        origFullpath = origPathname + '/%s.%s' %(imgHash, slide['format'])
    else:
        origFullpath = origPathname + '/%s.jpg' %(imgHash)
    return origFullpath, directoryNumber

def isImage(imgFile):
    try:
        im = Image.open(imgFile)
        return im
    except:
        return False

def openImage(file):
    image = isImage(file)
    if not image:
        return False
    return image

def saveImage(image, identifier, **kwargs):
    """
        Save an image to disk
        Directories are created based on the identifier that gets passed in
        Each identifier object contains an 'imageNum' field that is a running tally of
        all images that have the same identifier.  When we get to 30k images in a
        directory (via integer division), we create a new directory and save images in there.
    """
    hash = _generateHash(filename, thing)
    i = getImageIdentifier(identifier)
    if not i:
        i = ImageIdentifier(identifier)
    
    i['numImages'] = unicode(int(i['numImages']) + 1)
    directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
    pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, 'orig')
    savename = hash + '.png'
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    
    fullpath = os.path.join(pathname, savename)
    if 'thing' in kwargs:
        thing = kwargs['thing']
        thing['directoryNum'] = directoryNumber
        directoryNumIdentifier = 'directoryNum_' + identifier
        thing[directoryNumIdentifier] = directoryNumber
        commit(thing)
    
    # Now convert and save
    # only gif conversions seem to give trouble.
    # tested formats:   tiff (lzw/packbits/no compression, alpha/no-alpha)
    #                   jpeg
    #                   png
    #                   tga
    #                   bmp
    #                   gif
    try:
        im = Image.open(image)
        if im.format == 'GIF':
            transparency = im.info['transparency']
            im.save(fullpath, 'PNG', transparency=transparency)
        im.save(fullpath, 'PNG')
        return hash
    except:
        log.error('Unable to save to %s with hash %s' % (fullpath, hash))
        return False

def _generateHash(filename, thing):
    s = '%s_%s' %(filename, thing['urlCode'])
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
        im = Image.open(fullpath)
        im.thumbnail(dims, Image.ANTIALIAS)
        savepath = os.path.join(directory, '%s.%s'%(saveFilename, postfix))
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