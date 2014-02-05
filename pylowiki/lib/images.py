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
    2)  Generate the hash associated with this image through use of generateHash().
    3)  Save original image with saveImage(imObj).  The identifier will depend on the overall function (e.g. 'avatar', 'background', 'slide', etc...)
        The sub identifier depends on the specific function (e.g. 'thumbnail', 'orig', 'slideshow').  Here you will want to save as 'orig'.
    4)  Process imgObj as necessary with cropImage() and resizeImage()
    5)  Save the modified imgObj with the same identifier, but different sub identifier (e.g. identifier = 'avatar', sub identifier = 'thumbnail')

"""

def resizeImage(image, imageHash, width, height, **kwargs):
    """
        Given an object of type PIL.Image, resize that object and return it.
        
        Inputs:
            image       ->  An object of type PIL.Image
            imageHash   ->  A string, this is the unique identifier for this image.  Used for debugging and logging purposes.
            width       ->  An int, exactly as titled.  However, if set to the string 'max', then this is the width of the image.
            height      ->  An int, exactly as titled.  However, if set to the string 'max', then this is the height of the image.
        
        Optional inputs:
            preserveAspectRatio ->  Exactly as it sounds.  Boolean value.
        
        Outputs:
            image       ->  An object of type PIL.Image, now resized.
        
    """
    
    try:
        ratio = 1
        if width == 'max':
            width = image.size[0]
        if height == 'max':
            height = image.size[1]
        dims = (width, height)
        if 'preserveAspectRatio' in kwargs:
            if kwargs['preserveAspectRatio'] == True:
                maxwidth = width
                maxheight = height
                width, height = image.size
                ratio = min(float(maxwidth)/width, float(maxheight)/height)
                dims = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        image = image.resize(dims, Image.ANTIALIAS)
        
        return image
    except Exception as e:
        log.error('Error resizing image with hash %s, error given was %s' %(imageHash, e))
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
    
    # Some validation.
    # Here, image.size is a tuple of the form (width, height)
    imageDims = image.size
    if 'clientWidth' in kwargs:
        clientWidth = kwargs['clientWidth']
        if clientWidth != -1:
            ratio = float(clientWidth) / imageDims[0]
            width /= ratio
            x /= ratio
        
    if 'clientHeight' in kwargs:
        clientHeight = kwargs['clientHeight']
        if clientHeight != -1:
            ratio = float(clientHeight) / imageDims[1]
            height /= ratio
            y /= ratio
    
    if x > imageDims[0]:
        x = 0
    if y > imageDims[1]:
        y = 0
    if x + width > imageDims[0]:
        width = imageDims[0] - x
    if y + height > imageDims[1]:
        height = imageDims[1] - y
    
    try:
        # The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
        box = (x, y, x + width, y + height)
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

def openImage(file):
    """
        The PIL.Image.open() function will also verify that the passed in file actually is an image.
    """
    try:
        image = Image.open(file)
        return image
    except:
        return False

def generateHash(filename, thing):
    s = '%s_%s_%f' %(filename, thing['urlCode'], time())
    return md5(s).hexdigest()

def saveImage(image, imageHash, identifier, subIdentifier, **kwargs):
    """
        Save an image to disk
        Directories are created based on the identifier that gets passed in
        Each identifier object contains an 'imageNum' field that is a running tally of
        all images that have the same identifier.  When we get to 30k images in a
        directory (via integer division), we create a new directory and save images in there.
        
        Inputs:
            image           ->  The PIL.Image object
            imageHash       ->  Obtained by calling generateHash()
            identifier      ->  The general function of this image (e.g. 'avatar', 'background', 'slide', etc...)
            subIdentifier   ->  The specific function of this image (e.g. 'thumbnail', 'orig', etc...)
            
        Optional:
            thing           ->  A Thing object.  This needs to be passed in so that we can store the directory number in the Thing.
                                Only needs to be passed in once...this 'should' be when we are saving the 'orig' subidentifier.
            
        Outputs:
            If successful, returns the PIL.Image object.
            If unsuccessful, returns False.
    """
    i = getImageIdentifier(identifier)
    if not i:
        i = ImageIdentifier(identifier)
    
    i['numImages'] = unicode(int(i['numImages']) + 1)
    commit(i)
    directoryNumber = str(int(i['numImages']) / numImagesInDirectory)
    pathname = os.path.join(config['app_conf']['imageDirectory'], identifier, directoryNumber, subIdentifier)
    savename = imageHash + '.png'
    
    if 'thing' in kwargs:
        thing = kwargs['thing']
        thing['directoryNum'] = directoryNumber
        directoryNumIdentifier = 'directoryNum_' + identifier
        imageHashIdentifier = 'pictureHash_' + identifier
        thing[directoryNumIdentifier] = directoryNumber
        thing[imageHashIdentifier] = imageHash
        commit(thing)
    
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    fullpath = os.path.join(pathname, savename)
	
    # Now convert and save
    # only gif conversions seem to give trouble.
    # tested formats:   tiff (lzw/packbits/no compression, alpha/no-alpha)
    #                   jpeg
    #                   png
    #                   tga
    #                   bmp
    #                   gif
    try:
        if image.format == 'GIF':
            transparency = image.info['transparency']
            image.save(fullpath, 'PNG', transparency=transparency)
        else:
            image.save(fullpath, 'PNG')
        return image
    except:
        log.error('Unable to save to %s with hash %s' % (fullpath, imageHash))
        return False
    
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
    
def userImageSource(user, **kwargs):
    # Assumes 'user' is a Thing.
    # Defaults to a gravatar source
    # kwargs:   forceSource:   Instead of returning a source based on the user-set preference in the profile editor,
    #                          we return a source based on the value given here (civ/gravatar)
    source = 'http://www.gravatar.com/avatar/%s?r=pg&d=identicon' % md5(user['email']).hexdigest()
    large = False
    gravatar = True

    if 'className' in kwargs:
        if 'avatar-large' in kwargs['className']:
            large = True
    if 'forceSource' in kwargs:
        if kwargs['forceSource'] == 'civ':
            gravatar = False
            if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
            else:
                source = '/images/hamilton.png'
        elif kwargs['forceSource'] == 'facebook':
            if large:
                source = user['facebookProfileBig']
            else:
                source = user['facebookProfileSmall']
        elif kwargs['forceSource'] == 'twitter':
            source = user['twitterProfilePic']

    else:
        if 'avatarSource' in user.keys():
            if user['avatarSource'] == 'civ':
                if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                    source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                    gravatar = False
            elif user['avatarSource'] == 'facebook':
                gravatar = False
                if large:
                    source = user['facebookProfileBig']
                else:
                    source = user['facebookProfileSmall']
            elif user['avatarSource'] == 'twitter':
                gravatar = False
                source = user['twitterProfilePic']

        elif 'extSource' in user.keys():
            # this is needed untl we're sure all facebook connected users have properly 
            # functioning profile pics - the logic here is now handled 
            # with the above user['avatarSource'] == 'facebook': ..
            if 'facebookSource' in user.keys():
                if user['facebookSource'] == u'1':
                    gravatar = False
                    # NOTE - when to provide large or small link?
                    if large:
                        source = user['facebookProfileBig']
                    else:
                        source = user['facebookProfileSmall']
    if large and gravatar:
        source += '&s=200'
    return source


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