##############################################
#    
#    Creation/editing/deletion functions for comments and discussions.
#    
##############################################

import logging, traceback

from pylowiki.model import Comment, Discussion, Revision, getComment, Event, commit, getIssueByID
from pylowiki.model import getSuggestionByID, getDiscussionByID, getUserByID
from pylowiki.lib.utils import urlify

from pylons import tmpl_context as c

log = logging.getLogger(__name__)

# A discussion is a new topic.  Each topic can have multiple comment trees.  A new comment tree will
# be a direct response to the discussion (topic).
def addDiscussion(title, data = ''):
    url = urlify(title)
    d = Discussion(title, url)
    r = Revision(data)
    u = c.authuser
    e = Event('createDiscussion', 'User %d created a discussion'%c.authuser.id)
    d.revisions.append(r)
    d.events.append(e)
    d.owner = u
    u.events.append(e)
    r.event = e
    return d
    
def addComment(discussionID, data, parentID, commentType):
    """
        Adds a comment to a discussion.  If it is not a reply to another comment, the
        incoming comment gets added as a root comment to the discussion.  Database commit
        is done here.
        
        inputs:
                discussionID    ->    The id of the discussion to which the comment is being added
                data            ->    The body of the comment
                parentID        ->    The id of the parent comment.  0 if no parent exists.
                
        outputs:
                comment         ->    The comment object.  This is false if something goes wrong.
    """
    try:
        r = Revision(data)
        d = getDiscussionByID(discussionID)
        u = c.authuser
        if int(parentID) == 0:
            # Adding a new comment tree - has no children, since nobody has had a chance to respond.
            comment = Comment(data)
            e = Event('addRootComment', 'User %d added a root comment' %c.authuser.id)
            d.children.append(comment)
        else:
            # Create a new comment, update the parent's children
            parentCom = getComment(parentID)
            comment = Comment(data, parentCom)
            e = Event('addChildComment', 'User %d added a child comment' %c.authuser.id)
        
        # Actions common to both cases
        comment.revisions.append(r)
        comment.events.append(e)
        r.event = e
        if commentType == "background":
            d.issue.page.comments.append(comment)
        elif commentType == "suggestionMain":
            d.suggestionMain.comments.append(comment)
        u.events.append(e)
        u.comments.append(comment)
        d.events.append(e)
        try:
            commit(e)
            if parentID != 0:
                parentCom.children[comment.id] = comment
            return comment
        except:
            return False
    except:
        log.info("Exception in user code:")
        log.info('-'*60)
        log.info(traceback.print_exc())
        log.info('-'*60)
    
def editComment(commentID, discussionID, data):
    comment = getComment(commentID)
    comment.data = data
    r = Revision(data)
    e = Event('editComment', 'User %s edited comment %s'%(c.authuser.id, comment.id))
    u = c.authuser
    comment.events.append(e)
    r.event = e
    d = comment.discussion
    d.events.append(e)
    u.events.append(e)
    try:
        commit(e)
        return comment
    except:
        return False