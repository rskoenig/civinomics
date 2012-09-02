from pylowiki.model import Thing, meta, Blob
from dbHelpers import commit, with_characteristic

def getScope(id):
    try:
        return meta.Session.query(Thing).filter_by(id = id).one()
    except:
        return False

def getScopes():
    try:
        return meta.Session.query(Thing).filter(objType = 'govtSphere').all()
    except:
        return False

# Takes in a thing ID and a picture file
def editPicture(gS, picture):
    try:
        gs.blob['picture'] = Blob('picture', picture)
        commit(gS)
        return gS
    except:
        return False

class Scope(object):
    def __init__(self, name, imageFile, filename):
        gS = Thing('scope')
        gS['name'] = name
        gS['filename'] = filename
        gS.blob['image'] = Blob('image', imageFile)
