log = logging.getLogger(__name__)

""" Given a list, return the list with only unique entries.  Taken from peterbe.com """
def unique(l, idfun = None):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    
    for item in l:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    
    return result
