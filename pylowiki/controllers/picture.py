import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from pylowiki.lib.base import BaseController, render

from pylowiki.model import commit, get_user

from hashlib import md5
import os, shutil
from pylons import config
from PIL import Image

log = logging.getLogger(__name__)

class PictureController(BaseController):

    def index(self):
        return render('/derived/upload.html')

    def hashPicture(self, username, title):
         return md5(username + title).hexdigest()

    def uploadPicture(self):
        """TODO: Check uploaded file to see if it actually is an image"""
        """Grab the file, make the hash"""
        picture = request.POST['pictureFile']
        hash = self.hashPicture(c.authuser.name, picture.filename)

        """Save the associated hash to the user's database entry """
        user = get_user(c.authuser.name)
        user.pictureHash = hash
        commit(user)

        """Save original to disk"""
        savename = hash + '.png'
        pathname = os.path.join(config['app_conf']['avatarDirectory'])
        fullpath = os.path.join(config['app_conf']['avatarDirectory'], savename)
        file = open(fullpath, 'wb')
        shutil.copyfileobj(picture.file, file)
        picture.file.close()
        file.close()

        """Create two thumbnails - one for the topbar, and one for the user's information page"""
        topbarDims = 25, 25
        profileDims = 200, 200
        im = Image.open(fullpath)
        im.thumbnail(topbarDims, Image.ANTIALIAS)
        im.save(pathname + '/' + hash + '.thumbnail', 'PNG')

        im = Image.open(fullpath)
        im.thumbnail(profileDims, Image.ANTIALIAS)
        im.save(pathname + '/' + hash + '.profile', 'PNG')

        return redirect(session['return_to'])

    """ avatar directory can be accessed via 'config['app_conf']['avatarDirectory']' """
