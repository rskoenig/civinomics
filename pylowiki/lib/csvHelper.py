import os, shutil, logging, re
from PIL import Image
from time import time
from hashlib import md5
import csv as helper

from pylons import config
from pylowiki.lib.db.dbHelpers import commit
from pylowiki.lib.db.imageIdentifier import ImageIdentifier, getImageIdentifier

log = logging.getLogger(__name__)

# Constants for parsing CSV fields

EMAIL = 'Email'
NAME = 'Full Name'
ZIP_CODE = 'Zip Code'
POLL = 'Poll Name'
NUM_RATINGS = '#ratings'
RATING_CODE = 'Code'
RATING_VALUE = 'Rating'

# End of constants

#
# saveCsv (void)
# Saves a copy of the file in the temporal directory to process it in a future.
# 
# input: fileitem
#
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

#
# parseCsv (list of users[dict])
#
# From the file path, parses the fields into user dictionaries.
# If the number of user ratings is greater than zero, 
# it parses the different ratings with the code and the rating.
#
# input: path to the file
#


def parseCsv(filepath):
    with open(filepath, 'rU') as f:
        r = helper.DictReader(f)
        users = []    
        for row in r:
            user = {}
            user['name'] = row[NAME]
            user['email'] = row[EMAIL]
            user['zip'] = row[ZIP_CODE]
            user['poll'] = row[POLL]
            if row[NUM_RATINGS] > 0:
                user['num_ratings'] = row[NUM_RATINGS]
                for i in range(0, int(row[NUM_RATINGS])):
                    auxCode = "code" + str(i)
                    auxRating = "rating" + str(i)
                    user[auxCode] = row[RATING_CODE + str(i+1)]
                    user[auxRating] = row[RATING_VALUE + str(i+1)]
#                    log.info("contents of " + auxCode + " are " + user[auxCode])
            users.append(user)
        log.info(users)
    return users