# -*- coding: utf-8 -*-
"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from pylowiki.model import meta

#fox added following imports
from hashlib import md5
from pylons import config
import datetime as d
from sqlalchemy.ext.sqlsoup import SqlSoup

# Logging for debugging purposes
import logging
log = logging.getLogger(__name__)

def init_model(engine):
    meta.Session.configure(bind=engine)
    meta.engine = engine
    
t_user = sa.Table( 'user', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'firstName', sa.types.String(50), unique = False, nullable = False ),
    sa.Column( 'lastName', sa.types.String(50), unique = False, nullable = False ),
    sa.Column( 'name', sa.types.String(256), unique = True, nullable = False ),
    sa.Column( 'password', sa.types.String(50), nullable = False ),
    sa.Column( 'email', sa.types.String(50), unique=True, nullable = False),
    sa.Column( 'regdate', sa.types.DateTime, default = d.datetime.now ),
    sa.Column( 'laston', sa.types.Integer, default = 0),
    sa.Column( 'disabled', sa.types.Boolean, default = False ),
    sa.Column( 'zipCode', sa.types.Integer, nullable = True),
    sa.Column( 'pictureHash', sa.types.String(128), nullable = True),
    sa.Column( 'activated', sa.types.Integer, nullable = True), 
    sa.Column( 'activationHash', sa.types.String(20), nullable = True),
    sa.Column( 'address', sa.types.Text, nullable = True),
    sa.Column( 'city', sa.types.Text, nullable = True),
    sa.Column( 'state', sa.types.String(40), nullable = True),
    sa.Column( 'homeTown', sa.types.Text, nullable = True),
    sa.Column( 'homeState', sa.types.String(40), nullable = True),
    sa.Column( 'birthMonth', sa.types.Integer, nullable = True),
    sa.Column( 'birthDay', sa.types.Integer, nullable = True),
    sa.Column( 'birthYear', sa.types.Integer, nullable = True),
    sa.Column( 'hideBirth', sa.types.Integer, nullable = True),
    sa.Column( 'culturalBackground1', sa.types.Text, nullable = True),
    sa.Column( 'culturalBackground2', sa.types.Text, nullable = True),
    sa.Column( 'hideCultBack', sa.types.Integer, nullable = True),
    sa.Column( 'gender', sa.types.String(20), nullable = True),
    sa.Column( 'hideGender', sa.types.Integer, nullable = True),
    sa.Column( 'religion', sa.types.String(40), nullable = True),
    sa.Column( 'hideReligion', sa.types.Integer, nullable = True),
    sa.Column( 'tagline', sa.types.String(140), nullable = True),
    sa.Column( 'bio', sa.types.Text, nullable = True),
    sa.Column( 'connections', sa.types.Text, nullable = True),
    sa.Column( 'accessLevel', sa.types.Integer, nullable = True),
    sa.Column( 'signupType', sa.types.Integer, default = 0),
    sa.Column( 'signupPlatformID', sa.types.Integer, nullable = True),
    mysql_charset='utf8'
)

t_canvasser = sa.Table( 'canvasser', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey('user.id'), nullable = True),
    mysql_charset='utf8'
)

t_canvasserMetadata = sa.Table( 'canvasserMetadata', meta.metadata,
    sa.Column(' id', sa.types.Integer, primary_key = True),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey('user.id'), nullable = True),
    sa.Column( 'canvasser_id', sa.types.Integer, sa.ForeignKey('canvasser.id'), nullable = True),
    sa.Column( 'eventTime', sa.types.DateTime, default = d.datetime.now),
    sa.Column( 'surveyAns_id', sa.types.Integer, sa.ForeignKey('surveyAns.id'), nullable = True),
    mysql_charset = 'utf8'
)

t_surveyAns = sa.Table( 'surveyAns', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'canvasser_id', sa.types.Integer, sa.ForeignKey('canvasser.id'), nullable = True),
    sa.Column( 'survey_id', sa.types.Integer, sa.ForeignKey('survey.id'), nullable = True),
    sa.Column( 'questionNum', sa.types.Text, nullable = True),
    sa.Column( 'answer', sa.types.Text, nullable = True),
    mysql_charset = 'utf8'
)

t_survey = sa.Table( 'survey', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key = True),
    sa.Column('creator_id', sa.types.Integer, sa.ForeignKey('user.id'), nullable = True),
    sa.Column('title', sa.types.String(256), unique = True, nullable = False),
    sa.Column('description', sa.types.Text, nullable = True),
    sa.Column('lastEdited', sa.types.DateTime, default = d.datetime.now),
    mysql_charset = 'utf8'
)

t_userWork = sa.Table( 'userWork', meta.metadata,
    sa.Column( 'entry', sa.types.Integer, primary_key = True),
    sa.Column( 'id', sa.types.Integer, nullable = False),
    sa.Column( 'type', sa.types.String(100), nullable = True),
    sa.Column( 'data', sa.types.String(100), nullable = True)
)

t_page = sa.Table( 'page', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'url', sa.types.String(256), unique=True, nullable = False ),
    sa.Column( 'deleted', sa.types.Boolean, default = False ),
    sa.Column( 'private', sa.types.Boolean, default = False),
    sa.Column( 'type', sa.types.String(64), unique=False, nullable = False),
    sa.Column( 'title', sa.types.String(256), unique = True, nullable = False),
    sa.Column( 'related', sa.types.String(120), unique = False, nullable = True),
    sa.Column( 'owners', sa.types.Text, unique = False, nullable = False),
    mysql_charset='utf8'
)

t_revision = sa.Table( 'revision', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'page_id', sa.types.Integer, sa.ForeignKey( 'page.id' ), nullable = True),
    sa.Column( 'event_id', sa.types.Integer, sa.ForeignKey( 'event.id' ), nullable = True),
    sa.Column( 'suggestion_id', sa.types.Integer, sa.ForeignKey( 'suggestion.id' ), nullable = True),
    sa.Column( 'comment_id', sa.types.Integer, sa.ForeignKey('comment.id'), nullable = True),
    sa.Column( 'discussion_id', sa.types.Integer, sa.ForeignKey('discussion.id'), nullable = True),
    sa.Column( 'data', sa.types.Text, nullable = False),
    mysql_charset='utf8'
)

t_comment = sa.Table( 'comment', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'page_id', sa.types.Integer, sa.ForeignKey( 'page.id' ), nullable = True),
    sa.Column( 'suggestion_id', sa.types.Integer, sa.ForeignKey( 'suggestion.id' ), nullable = True),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey( 'user.id' ), nullable = True),
    sa.Column( 'discussion_id', sa.types.Integer, sa.ForeignKey('discussion.id'), nullable = True),
    sa.Column( 'parent_id', sa.types.Integer, sa.ForeignKey('comment.id') ),
    sa.Column( 'isRoot', sa.types.Boolean, default = False),
    sa.Column( 'data', sa.types.Text, nullable = False),
    sa.Column( 'disabled', sa.types.Boolean, default = False ),
    sa.Column( 'pending', sa.types.Boolean, default = True),
    sa.Column( 'avgRating', sa.types.Float, nullable = True),
    sa.Column( 'lastModified', sa.types.DateTime, default = d.datetime.now),
    mysql_charset='utf8'
)

t_discussion = sa.Table('discussion', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key = True),
    sa.Column('title', sa.types.String(256), unique = False, nullable = False),
    sa.Column('url', sa.types.String(256), unique = False, nullable = False),
    sa.Column('issue_id', sa.types.Integer, sa.ForeignKey('issue.id'), nullable = True),
    sa.Column('suggestion_id', sa.types.Integer, sa.ForeignKey('suggestion.id'), nullable = True),
    sa.Column('user_id', sa.types.Integer, sa.ForeignKey('user.id'), nullable = False),
    mysql_charset='utf8'
)

t_event = sa.Table( 'event', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey( 'user.id' ), nullable = True),
    sa.Column( 'page_id', sa.types.Integer, sa.ForeignKey( 'page.id' ), nullable = True),
    sa.Column( 'suggestion_id', sa.types.Integer, sa.ForeignKey( 'suggestion.id' ), nullable = True),
    sa.Column( 'issue_id', sa.types.Integer, sa.ForeignKey( 'issue.id' ), nullable = True),
    sa.Column( 'article_id', sa.types.Integer, sa.ForeignKey( 'article.id' ), nullable = True),
    sa.Column( 'rating_id', sa.types.Integer, sa.ForeignKey( 'rating.id' ), nullable = True),
    sa.Column( 'comment_id', sa.types.Integer, sa.ForeignKey( 'comment.id' ), nullable = True),
    sa.Column( 'discussion_id', sa.types.Integer, sa.ForeignKey('discussion.id'), nullable = True),
    sa.Column( 'type', sa.types.String(100), nullable = False),
    sa.Column( 'remark', sa.types.String(512), nullable = True),
    sa.Column( 'date', sa.types.DateTime, default = d.datetime.now )    
)

t_points = sa.Table( 'points', meta.metadata,
    sa.Column( 'userId', sa.types.Integer, primary_key = True),
    sa.Column( 'points', sa.types.Integer, nullable = False, default = 0),
    sa.Column( 'solutions', sa.types.Text, nullable = True),
    sa.Column( 'suggestions', sa.types.Text, nullable = True),
    sa.Column( 'votes', sa.types.Text, nullable = True),
    sa.Column( 'issues', sa.types.Text, nullable = True),
    sa.Column( 'contributions', sa.types.Text, nullable = True),
    sa.Column( 'articles', sa.types.Text, nullable = True)
)

t_userTypes = sa.Table( 'userTypes', meta.metadata,
    sa.Column( 'userID', sa.types.Integer, primary_key = True, autoincrement = False),
    sa.Column( 'userLevel', sa.types.Integer, nullable = False)
)

t_article = sa.Table( 'article', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'url', sa.types.Text, nullable = False ),
    sa.Column( 'related', sa.types.String(256), nullable = False),
    sa.Column( 'title', sa.types.String(256), nullable = False),
    sa.Column( 'issue_id', sa.types.Integer, sa.ForeignKey( 'issue.id' ), nullable = True),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey( 'user.id' ), nullable = True),
    sa.Column( 'type', sa.types.String(20), default = 'post'),
    sa.Column( 'comment', sa.types.Text, nullable = True),
    sa.Column( 'pending', sa.types.Boolean, default = False),
    sa.Column( 'disabled', sa.types.Boolean, default = False)
)

t_votes = sa.Table( 'votes', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True ),
    sa.Column( 'amount', sa.types.Integer, nullable = False)
)

t_contributions = sa.Table( 'contributions', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'solutionID', sa.types.Integer, nullable = False),
    sa.Column( 'amount', sa.types.Integer, nullable = False)
)

t_issue = sa.Table( 'issue', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'user_id', sa.ForeignKey ('user.id'), nullable = True),
    sa.Column( 'name', sa.types.String(256), nullable = False),
    sa.Column( 'govtSphere', sa.types.Integer, nullable = True),
    sa.Column( 'goals', sa.types.Text, nullable = True),
    sa.Column( 'suggestionEnd', sa.types.String(10), nullable = True ), # dd/mm/yyyy
    sa.Column( 'solutionEnd', sa.types.String(10), nullable = True),
    sa.Column( 'solPkgEnd', sa.types.String(10), nullable = True),
    sa.Column( 'pageID', sa.types.Integer, nullable = False),
    sa.Column( 'page_id', sa.types.Integer, sa.ForeignKey( 'page.id' ), nullable = True),
    sa.Column( 'slideshowID', sa.types.Integer, nullable = True ),
    sa.Column( 'slideshowOrder', sa.types.Text, nullable = True),
    sa.Column( 'participants', sa.types.Text, nullable = True),
    mysql_charset='utf8'
)

t_slideshow = sa.Table ( 'slideshow', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'issue_id', sa.types.Integer, sa.ForeignKey( 'issue.id' ), nullable = True),
    sa.Column( 'pictureHash', sa.types.String(128), nullable = True),
    sa.Column( 'caption', sa.types.Text, nullable = True),
    sa.Column( 'title', sa.types.Text, nullable = True),
    sa.Column( 'deleted', sa.types.Boolean, default = False)
)

t_govtSphere = sa.Table( 'govtSphere', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'name', sa.types.String(256), nullable = False),
    sa.Column( 'pictureHash', sa.types.String(128), nullable = True)
)

t_suggestion = sa.Table( 'suggestion', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'issue_id', sa.types.Integer, sa.ForeignKey( 'issue.id' ), nullable = True),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey('user.id'), nullable = True),
    sa.Column( 'title', sa.types.String(256), nullable = False),
    sa.Column( 'tags', sa.types.Text, nullable = True),
    sa.Column( 'owners', sa.types.Text, unique = False, nullable = False),
    sa.Column( 'related', sa.types.Text, nullable = True),
    sa.Column( 'url', sa.types.String(256), nullable = True),
    sa.Column( 'deleted', sa.types.Boolean, default = False),
    sa.Column( 'pending', sa.types.Boolean, default = False),
    sa.Column( 'disabled', sa.types.Boolean, default = False),
    sa.Column( 'type', sa.types.String(100), nullable = True),
    sa.Column( 'avgRating', sa.types.Float, nullable = True)
)

t_rating = sa.Table( 'rating', meta.metadata,
    sa.Column( 'id', sa.types.Integer, primary_key = True),
    sa.Column( 'type', sa.types.String(128), nullable = True),
    sa.Column( 'rating', sa.types.Float, nullable = True),
    sa.Column( 'isCurrent', sa.types.Boolean, default = True),
    sa.Column( 'user_id', sa.types.Integer, sa.ForeignKey( 'user.id' ), nullable = True),
    sa.Column( 'suggestion_id', sa.types.Integer, sa.ForeignKey( 'suggestion.id'), nullable = True),
    sa.Column( 'article_id', sa.types.Integer, sa.ForeignKey('article.id'), nullable = True),
    sa.Column( 'issue_id', sa.types.Integer, sa.ForeignKey('issue.id'), nullable = True),
    sa.Column( 'comment_id', sa.types.Integer, sa.ForeignKey('comment.id'), nullable = True)
)

class Suggestion(object):
    def __init__(self, title, owners):
        self.title = title
        self.owners = owners

class User(object):
    def __init__( self, userName, password, email, firstName, lastName, zipCode ):
        """User Constructor"""
        self.name = userName
        self.email = email
        self.password = self.hash_password( password )
        self.firstName = firstName
        self.lastName = lastName
        self.zipCode = zipCode
        self.pictureHash = 'flash' # Default picture
        self.activated = 0

    def check_password( self, password ):
        """Test the given password against the user """
        if self.password == self.hash_password( password ): return True
        else: return False

    def change_password( self, password ):
        """Change the user password"""
        self.password = self.hash_password( password )
        return True

    def generate_password( self ):
        """Return a system generated password"""
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, 9
        return ''.join( [ choice( pool ) for i in range( size ) ] )

    def generateActivationHash(self):
        """Return a system generated hash for account activation"""
        from string import letters, digits
        from random import choice
        pool, size = letters + digits, 20
        return ''.join([choice(pool) for i in range(size)])

    def hash_password(  self, password ):
        """Return the password hash"""
        return md5( password + config['app_conf']['auth.pass.salt'] ).hexdigest()
        #return sha224( self.id + password ).hexdigest() # better password logic

class Page(object):
    def __init__( self, url, type, owners ):
        """Page Constructor"""
        self.url = url
        self.type = type
        self.owners = owners

class Revision(object):
    def __init__( self, data ):
        """Revision Constructor"""
        self.data = data

class Comment(object):
    def __init__( self, data, parent = None):
        """Comment Constructor"""
        self.disabled = False
        self.pending = False
        self.parent = parent
        if parent == None:
            self.isRoot = True
        else:
            self.isRoot = False
        self.data = data
        
    def disable( self ):
        """disable this comment"""
        self.disabled = True 
        meta.Session.commit( )
        #event = Event( "disable" )
        #user.events.append( event )
        #self.page.events.append( event )
        #self.event = event  
    def enable( self ):
        """enable the comment"""
        self.disabled = False
        meta.Session.commit( )

class Event(object):
    def __init__( self, type, remark="" ):
        """Revision Constructor"""
        self.type = type
        self.remark = remark

class Points(object):
    def __init__( self, userId):
        self.userId = userId
        self.points = 1

class UserTypes(object):
    def __init__(self, data):
        self.data = data

class Article(object):
    def __init__(self, url, title, related = ''):
        self.url = url
        self.related = related
        self.title = title
        self.pending = True

class Votes(object):
    def __init__(self, amount):
        self.amount = amount

class Contributions(object):
    def __init__(self, id, solutionID, amount):
        self.id = id
        self.amount = amount
        self.solutionID = solutionID

class UserWork(object):
    def __init__(self, id, type, data):
        self.id = id
        if type == 'work':
            self.type = 'work'
        else:
            self.type = 'school'
        self.data = data

class Issue(object):
    def __init__(self, name, pageID):
        self.name = name
        self.pageID = pageID

class Slideshow(object):
    def __init__(self, pictureHash, caption, title):
        self.pictureHash = pictureHash
        self.caption = caption
        self.title = title

    def delete( self ):
        """delete this slide"""
        self.deleted = True 
        meta.Session.commit( )
        #event = Event( "disable" )
        #user.events.append( event )
        #self.page.events.append( event )
        #self.event = event  

    def undelete( self ):
        """undelete this slide"""
        self.deleted = False
        meta.Session.commit( )

class GovtSphere(object):
    def __init__(self, name, pictureHash):
        self.name = name
        self.pictureHash = pictureHash

class Suggestion(object):
    def __init__(self, title, owners):
        self.title = title
        self.owners = owners

class Rating(object):
    def __init__(self, type, rating):
        self.type = type
        self.rating = rating

class Canvasser(object):
    def __init__(self):
        self = self

class CanvasserMetadata(object):
    def __init__(self, checkInTime):
        self.checkInTime = d.datetime.now

class SurveyAns(object):
    def __init__(self, questionNum, answer):
        self.questionNum = questionNum
        self.answer = answer

class Survey(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.lastEdited = d.datetime.now
        
class Discussion(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url

# orm.mapper(class, table, ...)
orm.mapper(User, t_user, properties = {
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref='user'),
    'comments':orm.relation(Comment, order_by=(sa.desc('comment.id')), backref = 'user'),
    'issues':orm.relation(Issue, order_by=(sa.desc('issue.id')), backref = 'user'),
    'ratings':orm.relation(Rating, order_by=(sa.desc('rating.id')), backref = 'user'),
    'suggestions':orm.relation(Suggestion, order_by=(sa.desc('suggestion.id')), backref = 'user')
})

orm.mapper(Page, t_page, properties = {
    'revisions':orm.relation(Revision, order_by=(sa.desc('revision.id')), backref='page'),
    'comments':orm.relation(Comment, order_by=(sa.desc('comment.id')), backref='page'),
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref='page'),
    'issue':orm.relation(Issue, uselist=False, backref='page')
})

orm.mapper(Event, t_event,
properties = {
    'revision':orm.relation(Revision, uselist=False, backref='event'),
    'rating':orm.relation(Rating, uselist=False, backref='event')
})

orm.mapper(Revision, t_revision)
orm.mapper(Comment, t_comment, properties = {
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref = 'comment'),
    'ratings':orm.relation(Rating, order_by = (sa.desc('rating.id')), backref = 'comment'),
    'revisions':orm.relation(Revision, order_by=(sa.desc('revision.id')), backref = 'comment'),
    'children':orm.relation(Comment, backref = orm.backref('parent', remote_side = t_comment.c.id), 
                            collection_class=orm.collections.attribute_mapped_collection('id') )
})

orm.mapper(Discussion, t_discussion, properties = {
    'owner':orm.relation(User, uselist = False, backref = 'discussion'),
    'children':orm.relation(Comment, order_by=(sa.desc('comment.id')), backref = 'discussion'),
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref = 'discussion'),
    'revisions':orm.relation(Revision, order_by=(sa.desc('revision.id')), backref = 'discussion')
})

orm.mapper(Points, t_points)
orm.mapper(UserTypes, t_userTypes)
orm.mapper(Article, t_article, properties = {
    'user':orm.relation(User, order_by=(sa.desc('user.id')), backref = 'article'),
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref = 'article'),
    'ratings':orm.relation(Rating, order_by=(sa.desc('rating.id')), backref = 'article')
})
orm.mapper(Votes, t_votes)
orm.mapper(Contributions, t_contributions)
orm.mapper(UserWork, t_userWork)
orm.mapper(Slideshow, t_slideshow)
orm.mapper(GovtSphere, t_govtSphere)

orm.mapper(Issue, t_issue, 
properties = {
    'slideshow':orm.relation(Slideshow, order_by=(sa.desc('slideshow.id')), backref = 'issue'),
    'suggestions':orm.relation(Suggestion, order_by=(sa.desc('suggestion.id')), backref = 'issue'),
    'articles':orm.relation(Article, order_by=(sa.desc('article.id')), backref = 'issue'),
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref = 'issue'),
    'ratings':orm.relation(Rating, order_by=(sa.desc('rating.id')), backref = 'issue'),
    'mainDiscussion':orm.relation(Discussion, uselist=False, backref = 'issueMain'),
    'discussions':orm.relation(Discussion, order_by=(sa.desc('discussion.id')), backref = 'issue')
})

orm.mapper(Suggestion, t_suggestion,
properties = {
    'revisions':orm.relation(Revision, order_by=(sa.desc('revision.id')), backref = 'suggestion'),
    'comments':orm.relation(Comment, order_by=(sa.desc('comment.id')), backref = 'suggestion'),
    'events':orm.relation(Event, order_by=(sa.desc('event.id')), backref = 'suggestion'),
    'ratings':orm.relation(Rating, order_by=(sa.desc('rating.id')), backref = 'suggestion'),
    'mainDiscussion':orm.relation(Discussion, uselist = False, backref = 'suggestionMain'),
    'discussions':orm.relation(Discussion, order_by=(sa.desc('discussion.id')), backref = 'suggestion')
})

orm.mapper(Rating, t_rating)

orm.mapper(Canvasser, t_canvasser,
properties = {
    'user':orm.relation(User, uselist = False, backref = 'canvasser'),
    'canvasserMetadata':orm.relation(CanvasserMetadata, order_by=(sa.desc('canvasserMetadata.id')), backref = 'canvasser')
})

orm.mapper(CanvasserMetadata, t_canvasserMetadata,
properties = {
    'user':orm.relation(User, uselist = False, backref = 'canvasserMetadata'),
    'surveyAns':orm.relation(SurveyAns, uselist = False, backref = 'canvasserMetadata')
})

orm.mapper(SurveyAns, t_surveyAns)

orm.mapper(Survey, t_survey,
properties = {
    'creator':orm.relation(User, uselist = False),
    'answers':orm.relation(SurveyAns, order_by=(sa.desc('surveyAns.id')), backref = 'survey')
})

##########################
# Commit Helpers
##########################

def commit( i ):
    """Create or save the object to database"""
    try:
        meta.Session.add( i )
        meta.Session.commit()
        return True
    except:
        log.info("Could not commit: ")
        log.info(i)
        return False


def commit_edit( url, user, data, type, remark ):
    """commit edit to database"""
    """controller that use this: edit, wiki, revision (revert)"""

    p = get_page( url )
    u = get_user( user )
    r = Revision( data )
    e = Event( type, remark )
 
    p.revisions.append( r )
    p.events.append( e )
    u.events.append( e )
    r.event = e  

    try:
        commit( e ) 
        return True
    except:
        return False

def commit_trash( url, user, action, remark):
    """commit delete or restore to database."""

    if action == "delete":
        p = get_page( url )
    if p == False: # Do not delete a deleted page.
        return False
    p.deleted = True
    
    if action == "restore":
        p = get_page( url, True )
    if p == False: # Do not restore a page not deleted.
        return False
    p.deleted = False  

    u = get_user( user )
    e = Event( action, remark )
    
    p.events.append( e )
    u.events.append( e )

    try:
        commit( e )
        return True
    except:
        return False


def commit_attach( user, action, remark ):
    """commit attach event"""

    u = get_user( user )
    e = Event( action, remark )
    u.events.append( e )
    try:
        commit( e ) 
        return True
    except:
        return False

def commit_comment( url, user, data, type ):
    """commit page comment to database"""

    u = get_user(user)
    c = Comment(data)
    e = Event("comment")

    if type == "background":
        p = get_page( url )
        p.comments.append( c )
        p.events.append( e )
    elif type == "suggestion":
        """ Here url will be a list.  Entry 0 -> title, Entry 1 -> issue ID """
        s = getSuggestion(url[0], url[1])
        s.comments.append(c)
        s.events.append(e)
    u.events.append(e)
    u.comments.append(c)
    c.events.append(e)
    
    try:
        commit( e ) 
        return True
    except:
        return False

##########################
# User functions
##########################

def get_user( name ):
    """Return user object by username."""
    try:
        return meta.Session.query( User ).filter_by( name = name ).one()
    except sa.orm.exc.NoResultFound:
        return False

def getUserByID( id ):
    try:
        return meta.Session.query( User ).filter_by( id = id ).one()
    except sa.orm.exc.NoResultFound:
        return False

def get_all_users( ):
    """Return a list of all user objects."""
    try:
        return meta.Session.query( User ).all()
    except sa.orm.exc.NoResultFound:
        return False

def get_user_by_email( email ):
    """Return user object by email.""" # could be refactored into get_user, using an or statement
    try:
        log.info('email = %s' %email)
        return meta.Session.query( User ).filter_by( email = email ).one()
    except sa.orm.exc.NoResultFound:
        return False

def getUserAccessLevel(userID):
    try:
        ans = meta.Session.query(UserTypes).filter_by(userID = userID).one()
        return ans.userLevel
    except sa.orm.exc.NoResultFound:
        return False   

def getUserSuggestions(user):
    
    pointsObj = getPoints(user.id)
    suggestionList = pointsObj.suggestions
    if suggestionList == None:
        return None
    else:
        suggestions = []        # List of dictionaries
        entry = {}              # The dictionaries to populate the list
        for num in suggestionList:
            page = getPageByID(num)
            if page.type == 'suggestion':
                entry['suggestionURL'] = page.url
                entry['suggestionTitle'] = page.title

                issue = page.related.split(',')[0]
                page = getPageByID(issue)
                entry['issueURL'] = page.url
                entry['issueTitle'] = page.title

            suggestions.append(entry)
        return suggestions

def getArticlesRead(user):
    pointsObj = getPoints(user.id)
    articleList = pointsObj.articles
    if articleList == None:
        return None
    else:
        articles = []        # List of dictionaries
        for num in articleList.split(','):
            article = getArticle(int(num))
            entry = {} # Dictionary that will populate the list
            entry['articleURL'] = article.url
            entry['articleTitle'] = article.title
            entry['type'] = article.type
            if article.type != 'background':
                page = getPageByID(article.related.split(',')[0])
                entry['issueURL'] = page.url
                entry['issueTitle'] = page.title

            articles.append(entry)
        return articles

def getVotes(user):
    pointsObj = getPoints(user.id)
    voteList = pointsObj.votes
    if voteList == None:
        return None
    else:
        votes = []        # List of dictionaries
        entry = {}              # The dictionaries to populate the list
        for num in voteList:
            vote = getVote(num)
            entry['amount'] = vote.amount
            page = getPageByID(num)
            entry['issueTitle'] = page.title
            entry['issueURL'] = page.url
            votes.append(entry)
        return votes

def getSolutions(user):
    pointsObj = getPoints(user.id)
    solutionList = pointsObj.solutions
    if solutionList == None:
        return None
    else:
        solutions = []
        entry = {}
        for num in solutionList:
            solution = getPageByID(num)
            entry['solutionTitle'] = page.title
            entry['solutionURL'] = page.URL
            page = getPageByID(solution.related.split(',')[0])
            entry['issueTitle'] = page.title
            entry['issueURL'] = page.url
            solutions.append(entry)
        return solutions

def getUserContributions(user):
    pointsObj = getPoints(user.id)
    contributionList = pointsObj.contributions
    if contributionList == None:
        return None
    else:
        contributions = []
        entry = {}
        for num in contributionList:
            contribution = getContribution(num)
            entry['amount'] = contribution.amount
            page = getPageByID(contribution.solutionID.split(',')[0])
            entry['solutionTitle'] = page.title
            entry['solutionURL'] = page.url
            contributions.append(entry)
    return contributions

def getUserConnections(user):
    connections = user.connections
    if connections == None:
        return None
    connectionList = []
    entry = {}
    for num in connectionList:
        connection = getUserByID(num)
        entry['profileURL'] = '/profile/%s' % connection.name
        entry['pictureHash'] = connection.pictureHash
        entry['name'] = connection.name
        entry['location'] = '%s, %s' % (connection.city, connection.state)
        connectionList.append(entry)
    return connectionList

##########################
# Page functions
##########################

def get_page( url, deleted = False ):
    """Return page object by url.
       If deleted = True get a deleted page object"""
    try:
        return meta.Session.query(Page).filter_by( url = url, deleted = deleted ).one()
    except sa.orm.exc.NoResultFound:
        return False

def getPageByID(id, deleted = False):
    """Return page object by id.
       If deleted = True, get a deleted page object"""
    try:
        return meta.Session.query(Page).filter_by(id = id, deleted = deleted).one()
    except sa.orm.exc.NoResultFound:
        return False

def get_all_pages( deleted = False ):
    """Return a list of all page objects.
       If deleted = True, return a list of all deleted page objects.
    """
    return meta.Session.query(Page).filter_by( deleted = deleted ).all()

def getIssues( deleted = False ):
    return meta.Session.query(Page).filter_by( deleted = deleted, type = 'issue' ).all()

def getSolutions( deleted = False ):
    return meta.Session.query(Page).filter_by( deleted = deleted, type = 'solution' ).all()

def get_all_events():
    """Return a list of all event objects"""
    return meta.Session.query( Event ).order_by( Event.id.desc() ).all()

def get_revision( id ): 
    """Return a revision object by id"""
    try:
        return meta.Session.query( Revision ).filter_by( id = id ).one()
    except sa.orm.exc.NoResultFound:
        return False

def get_prev_revision( id, page_id ): 
    """Return previous revision object by id and page_id."""
    try:
        return meta.Session.query( Revision ).order_by( Revision.id.desc() ).filter( Revision.id < id ).filter_by( page_id = page_id ).limit( 1 ).one()
    except sa.orm.exc.NoResultFound:
        return False

def get_all_revisions( page_id ):
    """Return a list of all revision objects by page_id"""
    try:
        return meta.Session.query( Revision ).order_by(Revision.id.desc() ).join(Event).filter_by( page_id = page_id ).all()
    except sa.orm.exc.NoResultFound:
        return False    

def get_search_results( needle ): 
    db = config['app_conf']['sqlalchemy.url'].split(":")
    if db[0] == "mysql":
        sql = meta.Session.execute("""

            SELECT 
                page.id AS page_id, page.url as page_url, avg(MATCH(data) AGAINST ('"""+needle+"""')) as score
            FROM 
                revision JOIN event ON revision.event_id = event.id JOIN page ON page.id = event.page_id
            WHERE 
                page.deleted = 0
            GROUP BY
                page_id
            HAVING 
                score <> 0
            ORDER BY
                score DESC
        """ )
        return 1, sql

    else:
        e = "Sorry but pylowiki currently only supports fulltext searching on mySQL."
        return 0, e

##########################
# Point functions
##########################
# q = session.query(SomeMappedClass)
# filter_by(column name = value)
def addPoints(userId, numPoints):
    #return meta.Session.query(Page).filter_by( url = url, deleted = deleted ).one()
    pointsObj = meta.Session.query(Points).filter_by(userId = userId).one()
    pointsObj.points = pointsObj.points + numPoints
    commit(pointsObj) 

# Returns a points object
def getPoints(userId):
    try:
        return meta.Session.query(Points).filter_by(userId = userId).one()
    except:
        return "No points!"

##########################
# Article functions
##########################
def getArticle(id):
    try:
        return meta.Session.query(Article).filter_by(id = id).one()
    except:
        return False

def getArticleByURL(url, issue_id):
    try:
        return meta.Session.query(Article).filter_by(url = url, issue_id = issue_id).one()
    except:
        return False

def getArticlesByIssueID(issue_id):
    try:
        return meta.Session.query(Article).order_by(Article.id.desc()).filter_by(issue_id = issue_id).all()
        """return meta.Session.query( Revision ).order_by( Revision.id.desc() ).filter( Revision.id < id ).filter_by( page_id = page_id ).limit( 1 ).one()"""
    except:
        return False

def getArticleByTitle(title, issue_id):
    try:
        return meta.Session.query(Article).filter_by(issue_id = issue_id, title = title).one()
    except:
        return False

def getAllArticles():
    try:
        return meta.Session.query(Article).all()
    except:
        return False

##########################
# Vote functions
##########################
def getVote(id):
    try:
        return meta.Session.query(Votes).filter_by(id = id).one()
    except:
        return False

##########################
# Contribution functions
##########################
def getContribution(id):
    try:
        return meta.Session.query(Contributions).filter_by(id = id).one()
    except:
        return False

##########################
# userWork functions
##########################

def getUserWork(id, type):
    try:
        return meta.Session.query(UserWork).filter_by(id = id, type = type).all()
    except:
        return False

##########################
# issue functions
##########################
def getIssueByID(id):
    try:
        return meta.Session.query(Issue).filter_by(page_id = id).one()
    except:
        return False

def getIssueByName(name):
    try:
        return meta.Session.query(Issue).filter_by(name = name).one()
    except:
        return False

def getParticipantsByID(id):
    try:
        return meta.Session.query(Event).filter_by(page_id = id).all()
    except:
        return False

##########################
# govtSphere functions
##########################

def getAllSpheres():
    try:
        return meta.Session.query(GovtSphere).order_by(GovtSphere.name.asc()).all()
    except:
        return False

def getSphere(id):
    try:
        return meta.Session.query(GovtSphere).filter_by(id = id).one()
    except:
        return False

##########################
# slideshow functions
##########################

def getSlideshow(issueID, deleted = False):
    try:
        return meta.Session.query(Slideshow).filter_by(issue_id = issueID, deleted = deleted).order_by(Slideshow.id.asc()).all()
    except:
        return False

def countSlideshow(issueID, deleted = False):
    try:
        return meta.Session.query(Slideshow).filter_by(issue_id = issueID, deleted = deleted).count()
    except:
        return False

def getSlide(slideID, deleted = False):
    try:
        return meta.Session.query(Slideshow).filter_by(id = slideID, deleted = deleted).one()
    except:
        return False

##########################
# suggestion functions
##########################
def getSuggestion(title, issue_id):
    try:
        return meta.Session.query(Suggestion).filter_by(issue_id = issue_id, title = title).one()
    except:
        return False

def getAllSuggestions(deleted = False):
    try:
        return meta.Session.query(Suggestion).filter_by(deleted = deleted).all()
    except:
        return False

def getSuggestionByID(id):
    try:
        return meta.Session.query(Suggestion).filter_by(id = id).one()
    except:
        return False

def getSuggestionByURL(url, issue_id):
    try:
        return meta.Session.query(Suggestion).filter_by(url = url, issue_id = issue_id).one()
    except:
        return False

##########################
# rating functions
##########################

def getRatingForSuggestion(suggestion_id, user_id):
    try:
        return meta.Session.query(Rating).filter_by(user_id = user_id, suggestion_id = suggestion_id).one()
    except:
        return False

def getAvgRatingForSuggestion(suggestion_id):
    try:
        cols = meta.Session.query(Rating).filter_by(suggestion_id = suggestion_id).all()
        l = []
        for item in cols:
            l.append(item.rating)
        return sum(l)/len(l)
    except:
        return False

def getNumRatingsForSuggestion(suggestion_id):
    try:
        return len(meta.Session.query(Rating).filter_by(suggestion_id = suggestion_id).all())
    except:
        return False

def getRatingForComment(comment_id, user_id):
    try:
        return meta.Session.query(Rating).filter_by(comment_id = comment_id, user_id = user_id).one()
    except:
        return False

def getAvgRatingForComment(comment_id):
    try:
        cols = meta.Session.query(Rating).filter_by(comment_id = comment_id).all()
        l = []
        for item in cols:
            l.append(item.rating)
            ##log.info('item = %s' % item)
        return sum(l)/len(l)
    except:
        return False

##########################
# survey functions
##########################

def getSurvey(title):
    try:
        return meta.Session.query(Survey).filter_by(title = title).one()
    except:
        return False

def getCanvasser(user_id):
    try:
        return meta.Session.query(Canvasser).filter_by(user_id = user_id).one()
    except:
        return False
    
##########################
# comment functions
##########################
def getComment( id ):
    try:
        return meta.Session.query( Comment ).filter_by( id = id ).one()
    except sa.orm.exc.NoResultFound:
        return False

##########################
# discussion functions
##########################
def getDiscussionByID( id ):
    try:
        return meta.Session.query( Discussion ).filter_by( id = id).one()
    except:
        return False