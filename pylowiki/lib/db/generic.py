# Defines a standard for object linking.
# All objects that get accessed through a URL need the following two fields:
# 
# urlCode: obtained from toBase62() in pylowiki/lib/utils.py
# url: obtained from urlify() in pylowiki/lib/utils.py
# 
# Because the urlCode field is unique, this is what we use to link objects.

import logging
log = logging.getLogger(__name__)

def linkChildToParent(child, parent):
   try:
      code = parent['urlCode']
   except:
      log.error("linkChildToParent(): parent object missing 'ulrCode' field.")
      return False
   
   key = '%s%s' %(parent.objType, 'Code')
   value = code
   child[key] = value
   return child