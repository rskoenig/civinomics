# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398492182.2551479
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/6_comments.mako'
_template_uri = u'/lib/6_comments.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['loginToAddComment', 'displayDiscussion', 'sortComments', 'commentClubRule', 'recurseCommentTree', 'commentFooter', 'commentComparison', 'comments', 'commentContent', 'continueThread', 'activateToAddComment', 'commentHeading', 'displayComment', 'addCommentToDiscussion']


# SOURCE LINE 1

from pylowiki.lib.db.user import getUserByID, isAdmin
import pylowiki.lib.db.user         as userLib
import pylowiki.lib.db.revision     as revisionLib
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.comment import getComment
import logging, random
from datetime import datetime
import misaka as misaka

log = logging.getLogger(__name__)



def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 16
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 15
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 13
        __M_writer(u'\n\n')
        # SOURCE LINE 15
        __M_writer(u'\n')
        # SOURCE LINE 16
        __M_writer(u'\n\n')
        # SOURCE LINE 34
        __M_writer(u'\n\n')
        # SOURCE LINE 54
        __M_writer(u'\n\n')
        # SOURCE LINE 74
        __M_writer(u'\n\n')
        # SOURCE LINE 121
        __M_writer(u'\n\n')
        # SOURCE LINE 137
        __M_writer(u'\n\n')
        # SOURCE LINE 144
        __M_writer(u'\n\n')
        # SOURCE LINE 152
        __M_writer(u'\n\n')
        # SOURCE LINE 161
        __M_writer(u'\n\n')
        # SOURCE LINE 196
        __M_writer(u'\n\n')
        # SOURCE LINE 232
        __M_writer(u'\n\n')
        # SOURCE LINE 310
        __M_writer(u'\n\n')
        # SOURCE LINE 341
        __M_writer(u'\n\n')
        # SOURCE LINE 410
        __M_writer(u'\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_loginToAddComment(context,thing):
    context.caller_stack._push_frame()
    try:
        url = context.get('url', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 36
        __M_writer(u'\n')
        # SOURCE LINE 42
        __M_writer(u'\n    <fieldset>\n        <legend></legend>\n        <div class="span1">\n            <img src="/images/hamilton.png" class="avatar med-avatar">\n        </div>\n        <a href="#signupLoginModal" data-toggle=\'modal\'><textarea rows="2" class="span11" name="comment-textarea" placeholder="Add a comment..."></textarea></a>\n        <span class="help-block pull-right right-space">Please keep comments civil and on-topic.\n        <a href="')
        # SOURCE LINE 50
        __M_writer(escape(url))
        __M_writer(u'" title="Login to comment." class="btn btn-civ" type="button">Submit</a>\n    </fieldset>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayDiscussion(context,thing,discussion):
    context.caller_stack._push_frame()
    try:
        def recurseCommentTree(node,commentType,maxDepth,curDepth):
            return render_recurseCommentTree(context,node,commentType,maxDepth,curDepth)
        __M_writer = context.writer()
        # SOURCE LINE 154
        __M_writer(u'\n    ')
        # SOURCE LINE 155

        maxDepth = 8
        curDepth = 0
        if 'children' in discussion.keys():
            recurseCommentTree(discussion, thing.objType, maxDepth, curDepth)
            
        
        # SOURCE LINE 160
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_sortComments(context,commentIDs):
    context.caller_stack._push_frame()
    try:
        sorted = context.get('sorted', UNDEFINED)
        def commentComparison(com1,com2):
            return render_commentComparison(context,com1,com2)
        __M_writer = context.writer()
        # SOURCE LINE 139
        __M_writer(u'\n    ')
        # SOURCE LINE 140

        commentList = [getComment(commentID) for commentID in commentIDs]
        return sorted(commentList, cmp = commentComparison)
            
        
        # SOURCE LINE 143
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentClubRule(context):
    context.caller_stack._push_frame()
    try:
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 123
        __M_writer(u'\n')
        # SOURCE LINE 129
        __M_writer(u'    ')

        rules = []
        rules.append("Rule #2 of comment club: Do you talk to your mother with that voice?")
        rules.append("Rule #3 of comment club: You do not talk about comment club.")
        rules.append("Rule #4 of comment club: Gold Five: Stay on <del>target</del> topic!")
        ruleNum = random.randint(0, len(rules) - 1)
            
        
        # SOURCE LINE 135
        __M_writer(u'\n    ')
        # SOURCE LINE 136
        __M_writer(rules[ruleNum] )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_recurseCommentTree(context,node,commentType,maxDepth,curDepth):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        map = context.get('map', UNDEFINED)
        type = context.get('type', UNDEFINED)
        def sortComments(commentIDs):
            return render_sortComments(context,commentIDs)
        def displayComment(comment,commentType,maxDepth,curDepth,parent=None):
            return render_displayComment(context,comment,commentType,maxDepth,curDepth,parent)
        __M_writer = context.writer()
        # SOURCE LINE 163
        __M_writer(u'\n    ')
        # SOURCE LINE 164

        if not node:
            return
        if type(node) == int:
            node = getComment(node)
        if curDepth >= maxDepth or node['children'] == 0:
            return
        parent = node
        if node.objType == 'comment':
            if curDepth == 0:
                if node.objType == 'discussion':
                    parent = node
                else:
                    parent = getComment(node['parent'])
                childList = [int(node.id)]
            else:
                childList = map(int, node['children'].split(','))
        else:
            childList = map(int, node['children'].split(','))
            
        childList = sortComments(childList)
        for child in childList:
            # Hack to resolve slight difference between discussion objects and comment objects
            if type(child) == type(1L):
                child = node.children[child]
            if child == 0:
                pass
            try:
                displayComment(child, commentType, maxDepth, curDepth, parent)
            except:
                raise
            
        
        # SOURCE LINE 195
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentFooter(context,comment,author):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 343
        __M_writer(u'\n')
        # SOURCE LINE 352
        __M_writer(u'    ')

        replyID = 'reply-%s' % comment['urlCode']
        flagID = 'flag-%s' % comment['urlCode']
        editID = 'edit-%s' % comment['urlCode']
        adminID = 'admin-%s' % comment['urlCode']
            
        
        # SOURCE LINE 357
        __M_writer(u'\n    <div class="row-fluid">\n        <div class="span11 offset1">\n            <div class="btn-group">\n')
        # SOURCE LINE 361
        if 'user' in session and not c.privs['provisional']:
            # SOURCE LINE 362
            __M_writer(u'                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            __M_writer(escape(replyID))
            __M_writer(u'">reply</a>\n                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
            # SOURCE LINE 363
            __M_writer(escape(flagID))
            __M_writer(u'">flag</a>\n')
            # SOURCE LINE 364
            if c.privs['facilitator'] or c.privs['admin'] or c.authuser.id == comment.owner:
                # SOURCE LINE 365
                __M_writer(u'                        <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
                __M_writer(escape(editID))
                __M_writer(u'">edit</a>>\n')
                pass
            # SOURCE LINE 367
            if c.privs['facilitator'] or c.privs['admin']:
                # SOURCE LINE 368
                __M_writer(u'                        <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#')
                __M_writer(escape(adminID))
                __M_writer(u'">admin</a>\n')
                pass
            # SOURCE LINE 370
        elif not c.privs['provisional']:
            # SOURCE LINE 371
            __M_writer(u'                    <a class="btn btn-mini accordion-toggle" data-toggle="modal" data-target="#signupLoginModal">reply</a>\n                    <a class="btn btn-mini accordion-toggle" data-toggle="modal" data-target="#signupLoginModal">flag</a>\n')
            pass
        # SOURCE LINE 374
        __M_writer(u'            </div>\n            Added ')
        # SOURCE LINE 375
        __M_writer(escape(comment.date))
        __M_writer(u'\n            ')
        # SOURCE LINE 376

        revisions = revisionLib.getRevisionsForThing(comment)
        lib_6.revisionHistory(revisions, comment)
                    
        
        # SOURCE LINE 379
        __M_writer(u'\n        </div><!--/.span11.offset1-->\n    </div><!--/.row-fluid-->\n    \n')
        # SOURCE LINE 384
        __M_writer(u'    <div class="row-fluid collapse" id="')
        __M_writer(escape(replyID))
        __M_writer(u'">\n        <div class="span11 offset1">\n            <form action="/comment/add/handler" method="post" id="commentAddHandler_reply">\n                <label>reply</label>\n                <textarea name="comment-textarea" class="comment-reply span12" placeholder="Add a reply..."></textarea>\n                <input type="hidden" name="parentCode" value="')
        # SOURCE LINE 389
        __M_writer(escape(comment['urlCode']))
        __M_writer(u'" />\n                <input type="hidden" name="thingCode" value = "')
        # SOURCE LINE 390
        __M_writer(escape(c.thing['urlCode']))
        __M_writer(u'" />\n                <button type="submit" class="btn btn-civ pull-right" name = "submit" value = "reply">Submit</button>\n            </form>\n        </div>\n    </div>\n    \n')
        # SOURCE LINE 397
        __M_writer(u'    ')
        __M_writer(escape(lib_6.flagThing(comment)))
        __M_writer(u'\n    \n')
        # SOURCE LINE 399
        if 'user' in session:
            # SOURCE LINE 401
            if c.privs['admin'] or c.authuser.id == comment.owner or c.privs['facilitator']:
                # SOURCE LINE 402
                __M_writer(u'            ')
                __M_writer(escape(lib_6.editThing(comment)))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 404
            __M_writer(u'    \n')
            # SOURCE LINE 406
            if c.privs['facilitator'] or c.privs['admin']:
                # SOURCE LINE 407
                __M_writer(u'            ')
                __M_writer(escape(lib_6.adminThing(comment)))
                __M_writer(u'\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentComparison(context,com1,com2):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 146
        __M_writer(u'\n    ')
        # SOURCE LINE 147

        rating1 = int(com1['ups']) - int(com1['downs'])
        rating2 = int(com2['ups']) - int(com2['downs'])
        return rating2 - rating1
            
        
        # SOURCE LINE 151
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_comments(context,thing,discussion,**kwargs):
    context.caller_stack._push_frame()
    try:
        def loginToAddComment(thing):
            return render_loginToAddComment(context,thing)
        c = context.get('c', UNDEFINED)
        def displayDiscussion(thing,discussion):
            return render_displayDiscussion(context,thing,discussion)
        def addCommentToDiscussion(thing,discussion):
            return render_addCommentToDiscussion(context,thing,discussion)
        session = context.get('session', UNDEFINED)
        def activateToAddComment(thing):
            return render_activateToAddComment(context,thing)
        __M_writer = context.writer()
        # SOURCE LINE 23
        __M_writer(u'\n    ')
        # SOURCE LINE 24

        if 'user' in session and discussion.objType != 'comment' and not c.privs['provisional']:
            if thing['disabled'] != '1':
                addCommentToDiscussion(thing, discussion)
        elif 'user' not in session and discussion.objType != 'comment':
                loginToAddComment(thing)
        elif c.privs['provisional']:
                activateToAddComment(thing)
        displayDiscussion(thing, discussion)
            
        
        # SOURCE LINE 33
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentContent(context,comment,commentType,curDepth,maxDepth,author,accordionID,collapseID):
    context.caller_stack._push_frame()
    try:
        def recurseCommentTree(node,commentType,maxDepth,curDepth):
            return render_recurseCommentTree(context,node,commentType,maxDepth,curDepth)
        def continueThread(comment):
            return render_continueThread(context,comment)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def commentFooter(comment,author):
            return render_commentFooter(context,comment,author)
        __M_writer = context.writer()
        # SOURCE LINE 312
        __M_writer(u'\n    ')
        # SOURCE LINE 313

        thisClass = 'accordion-body collapse'
        if comment['disabled'] == '0' and comment['deleted'] == '0':
            thisClass += ' in'
            
        
        # SOURCE LINE 317
        __M_writer(u'\n    <div id="')
        # SOURCE LINE 318
        __M_writer(escape(collapseID))
        __M_writer(u'" class="')
        __M_writer(escape(thisClass))
        __M_writer(u'">\n        <div class="accordion-inner">\n            <div class="row-fluid">\n                <div class="span1">\n                    ')
        # SOURCE LINE 322

        if c.thing['disabled'] == '0':
            lib_6.upDownVote(comment)
                            
        
        # SOURCE LINE 325
        __M_writer(u'\n                </div> <!--/.span1-->\n                <div class="span11 comment-data">\n                    ')
        # SOURCE LINE 328
        __M_writer(misaka.html(comment['data'], extensions=misaka.EXT_AUTOLINK, render_flags = misaka.HTML_SKIP_IMAGES) )
        __M_writer(u'\n')
        # SOURCE LINE 329
        if curDepth + 1 == maxDepth and comment['children'] != '0':
            # SOURCE LINE 330
            __M_writer(u'                        ')
            __M_writer(escape(continueThread(comment)))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 332
        __M_writer(u'                </div> <!--/.span11-->\n            </div> <!--/.row-fluid-->\n            ')
        # SOURCE LINE 334

        if c.thing['disabled'] == '0':
            commentFooter(comment, author)
                    
        
        # SOURCE LINE 337
        __M_writer(u'\n            ')
        # SOURCE LINE 338
        __M_writer(escape(recurseCommentTree(comment, commentType, maxDepth, curDepth + 1)))
        __M_writer(u'\n        </div><!--/.accordion-inner-->\n    </div><!--/.accordion-body.collapse-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_continueThread(context,comment):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 413
        __M_writer(u'\n    <br />\n    ')
        # SOURCE LINE 415

        if c.w:
            dparent = c.w
        elif c.user:
            dparent = c.user
        
        continueStr = '<a %s>%s</a>' %(lib_6.thingLinkRouter(comment, dparent, embed=True, commentCode=comment['urlCode']), "Continue this thread -->")
            
        
        # SOURCE LINE 422
        __M_writer(u'\n    ')
        # SOURCE LINE 423
        __M_writer(continueStr )
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_activateToAddComment(context,thing):
    context.caller_stack._push_frame()
    try:
        url = context.get('url', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 56
        __M_writer(u'\n')
        # SOURCE LINE 62
        __M_writer(u'\n    <fieldset>\n        <legend></legend>\n        <div class="span1">\n            ')
        # SOURCE LINE 66
        __M_writer(escape(lib_6.userImage(c.authuser, className="avatar med-avatar", linkClass="topbar-avatar-link")))
        __M_writer(u'\n        </div>\n        <a href="#activateAccountModal" data-toggle=\'modal\'><textarea rows="2" class="span11" name="comment-textarea" placeholder="Add a comment..."></textarea></a>\n        <span class="help-block pull-right right-space">Please keep comments civil and on-topic.\n        <a href="')
        # SOURCE LINE 70
        __M_writer(escape(url))
        __M_writer(u'" title="Login to comment." class="btn btn-civ" type="button">Submit</a>\n    </fieldset>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_commentHeading(context,comment,author,accordionID,collapseID,parent):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 234
        __M_writer(u'\n    ')
        # SOURCE LINE 235

        headerClass = "accordion-heading"
        if comment['addedAs'] == 'admin':
            headerClass += " admin"
        elif comment['addedAs'] == 'facilitator':
            headerClass += " facilitator"
        elif comment['addedAs'] == 'listener':
            headerClass += " listener"
        
        roleClass = ''
        roleLabel = ''
        
        try:
            if comment['commentRole']:
                roleClass = 'commentRole '
                roleLabel = ''
                if comment['commentRole'] == 'no':
                    roleClass += "red"
                    roleLabel += 'Con'
                    headerClass += " against"
        
                elif comment['commentRole'] == 'yes':
                    roleClass += "green"
                    roleLabel += "Pro"
                    headerClass += " favor"
        
                else:
                    roleClass +="grey"
                    roleLabel = "Neutral"
                    headerClass += " neutral"
        except:
            roleClass = ''
            roleLabel = ''
        
            
        
        # SOURCE LINE 269
        __M_writer(u'\n    <div class="')
        # SOURCE LINE 270
        __M_writer(escape(headerClass))
        __M_writer(u'">\n        <!--<button class="accordion-toggle inline btn btn-mini" data-toggle="collapse" data-parent="#')
        # SOURCE LINE 271
        __M_writer(escape(accordionID))
        __M_writer(u'" href="#')
        __M_writer(escape(collapseID))
        __M_writer(u'">\n            Hide\n        </button> -->\n        ')
        # SOURCE LINE 274

        lib_6.userImage(author, className="inline avatar small-avatar comment-avatar", linkClass="inline")
        lib_6.userLink(author, className="inline")
        role = ''
        roles = ['admin', 'facilitator', 'listener']
        if comment['addedAs'] in roles:
            role = '(%s)' % comment['addedAs']
                
        
        # SOURCE LINE 281
        __M_writer(u'\n        ')
        # SOURCE LINE 282
        __M_writer(escape(role))
        __M_writer(u'<span class="grey">')
        __M_writer(escape(lib_6.userGreetingMsg(author)))
        __M_writer(u'</span> from ')
        __M_writer(escape(lib_6.userGeoLink(author, comment=True)))
        __M_writer(u'\n        \n')
        # SOURCE LINE 284
        if roleClass != '':
            # SOURCE LINE 285
            __M_writer(u'            <span class="pull-right ')
            __M_writer(escape(roleClass))
            __M_writer(u'">')
            __M_writer(escape(roleLabel))
            __M_writer(u'</span>\n')
            pass
        # SOURCE LINE 287
        __M_writer(u'        <span class="pull-right disabledComment-notice">\n            <small>\n')
        # SOURCE LINE 289
        if parent:
            # SOURCE LINE 290
            if parent.objType == 'comment':
                # SOURCE LINE 291
                if parent['urlCode'] != comment['urlCode']:
                    # SOURCE LINE 292
                    __M_writer(u'                        ')
 
                    if c.w:
                        dparent = c.w
                    elif c.user:
                        dparent = c.user
                    elif c.initiative:
                        dparent = c.initiative
                                            
                    
                    # SOURCE LINE 299
                    __M_writer(u'\n                        <a ')
                    # SOURCE LINE 300
                    __M_writer(lib_6.thingLinkRouter(comment, dparent, embed=True, commentCode=parent['urlCode']) )
                    __M_writer(u' class="green green-hover">Parent</a>\n')
                    pass
                pass
            pass
        # SOURCE LINE 304
        if comment['disabled'] == '1':
            # SOURCE LINE 305
            __M_writer(u'                (comment disabled)\n')
            pass
        # SOURCE LINE 307
        __M_writer(u'            </small>\n        </span>\n    </div> <!--/.accordion-heading-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayComment(context,comment,commentType,maxDepth,curDepth,parent=None):
    context.caller_stack._push_frame()
    try:
        def commentContent(comment,commentType,curDepth,maxDepth,author,accordionID,collapseID):
            return render_commentContent(context,comment,commentType,curDepth,maxDepth,author,accordionID,collapseID)
        def commentHeading(comment,author,accordionID,collapseID,parent):
            return render_commentHeading(context,comment,author,accordionID,collapseID,parent)
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 198
        __M_writer(u'\n    ')
        # SOURCE LINE 199

        if comment:
            author = getUserByID(comment.owner)
            if comment['deleted'] == u'1':
                if 'user' in session:
                    if not isAdmin(c.authuser.id):
                        return
                else:
                    return
            if c.demo:
                if 'user' in session:
                    if ((author['accessLevel'] != '300' and not isFacilitator(author, c.w)) and author.id != c.authuser.id):
                        return
                else:
                    if author['accessLevel'] != '300' and not isFacilitator(author, c.w):
                        return
        else:
            return
        accordionID = 'accordion-%s' % comment['urlCode']
        collapseID = 'collapse-%s' % comment['urlCode']
        
        if curDepth % 2 == 1:
            backgroundShade = ' oddComment'
        else:
            backgroundShade = ' evenComment'
        
            
        
        # SOURCE LINE 225
        __M_writer(u'\n    <div class="accordion" id="')
        # SOURCE LINE 226
        __M_writer(escape(accordionID))
        __M_writer(u'">\n        <div class="accordion-group ')
        # SOURCE LINE 227
        __M_writer(escape(backgroundShade))
        __M_writer(u'">\n            ')
        # SOURCE LINE 228
        __M_writer(escape(commentHeading(comment, author, accordionID, collapseID, parent)))
        __M_writer(u'\n            ')
        # SOURCE LINE 229
        __M_writer(escape(commentContent(comment, commentType, curDepth, maxDepth, author, accordionID, collapseID)))
        __M_writer(u'\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addCommentToDiscussion(context,thing,discussion):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 76
        __M_writer(u'\n')
        # SOURCE LINE 82
        __M_writer(u'    <div class="spacer"></div>\n    <form action="/comment/add/handler" id="commentAddHandler_root">\n        <input type="hidden" id="type" name="type" value="')
        # SOURCE LINE 84
        __M_writer(escape(thing.objType))
        __M_writer(u'" />\n        <input type="hidden" name="discussionCode" value="')
        # SOURCE LINE 85
        __M_writer(escape(discussion['urlCode']))
        __M_writer(u'" />\n        <input type="hidden" name="parentCode" value="0" />\n        <input type="hidden" name="thingCode" value = "')
        # SOURCE LINE 87
        __M_writer(escape(c.thing['urlCode']))
        __M_writer(u'" />\n        <div class="row-fluid">\n            <div class="span1">\n                ')
        # SOURCE LINE 90
        __M_writer(escape(lib_6.userImage(c.authuser, className="avatar med-avatar", linkClass="topbar-avatar-link")))
        __M_writer(u'\n            </div>\n            <div class="span11">\n                <textarea rows="2" class="span12" name="comment-textarea" placeholder="Add a comment..."></textarea>\n            </div>\n        </div><!-- row-fluid -->\n')
        # SOURCE LINE 96
        if thing.objType == 'idea' or thing.objType == 'initiative':
            # SOURCE LINE 97
            __M_writer(u'            ')
            log.info("thing type is %s"%thing.objType) 
            
            __M_writer(u'\n            <div class="row-fluid">\n                <div class="span1">\n                </div>\n                <div class="span11">\n                    <label class="radio inline">\n                        <input type=radio name="commentRole" value="yes"> Pro\n                    </label>\n                    <label class="radio inline">\n                        <input type=radio name="commentRole" value="neutral" checked> Neutral\n                    </label>\n                    <label class="radio inline">\n                        <input type=radio name="commentRole" value="no"> Con\n                    </label>\n                    <button type="submit" class="btn btn-civ pull-right" name = "submit" value = "reply">Submit</button></span>\n                </div><!- span11 -->\n            </div><!-- row-fluid -->\n')
            # SOURCE LINE 114
        else:
            # SOURCE LINE 115
            __M_writer(u'        <div class="row-fluid">\n            <span class="help-block pull-right right-space">Please keep comments civil and on-topic.\n            <button type="submit" class="btn btn-civ" name = "submit" value = "reply">Submit</button></span>\n        </div><!-- row-fluid -->\n')
            pass
        # SOURCE LINE 120
        __M_writer(u'    </form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


