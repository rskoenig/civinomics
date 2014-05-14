import os, shutil, logging, re
from PIL import Image
from time import time
from hashlib import md5
import csv as helper

from pylons import config
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.imageIdentifier import ImageIdentifier, getImageIdentifier

log = logging.getLogger(__name__)

EMAIL = 'Email Address'
NAME = 'Full Name'
ZIP_CODE = 'Zip Code'


def saveCsv(fileitem):
    pathname = "pylowiki/public/temp"
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    log.info(fileitem)
    fn = os.path.basename(fileitem.filename)
    fullpath = os.path.join(pathname, fn)
    log.info(fullpath)
    try:
        log.info(fn)
        open(fullpath, 'wb').write(fileitem.file.read())
        fileitem.fullpath = fullpath
        return fileitem
    except:
        log.error('Unable to save')
        return False

def parseCsv(filepath):
    with open(filepath, 'rU') as f:
        r = helper.DictReader(f)
        users = []    
        for row in r:
            user = {}
            user['name'] = row[NAME]
            user['email'] = row[EMAIL]
            user['zip'] = row[ZIP_CODE]
            users.append(user)
        log.info(users)
    return users