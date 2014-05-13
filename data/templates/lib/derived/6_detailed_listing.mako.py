# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544345.1853709
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_detailed_listing.mako'
_template_uri = u'/lib/derived/6_detailed_listing.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showListing', 'getDisabledMessage', 'showIdeaListing']


# SOURCE LINE 1

import pylowiki.lib.db.user          as userLib
import pylowiki.lib.db.discussion    as discussionLib
import pylowiki.lib.db.event         as eventLib
import pylowiki.lib.db.facilitator   as facilitatorLib


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 8
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        __M_writer(u'\n\n')
        # SOURCE LINE 209
        __M_writer(u'\n\n')
        # SOURCE LINE 341
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showListing(context,thing,*args):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        session = context.get('session', UNDEFINED)
        str = context.get('str', UNDEFINED)
        endif = context.get('endif', UNDEFINED)
        def getDisabledMessage(thing):
            return render_getDisabledMessage(context,thing)
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'\n   ')
        # SOURCE LINE 11

        target = "_self"
        if c.paginator != '':
           renderList = c.paginator
        else:
           if thing == 'discussion':
              renderList = c.discussions
           elif thing == 'resources':
              if 'condensed' in args:
                  renderList = c.resources[0:5]
              else:
                  renderList = c.resources
              target = "_blank"
           elif thing == 'ideas':
              renderList = c.ideas
              
           
        
        # SOURCE LINE 27
        __M_writer(u'\n   <ul class="unstyled">\n      ')
        # SOURCE LINE 29
        itemCounter = 0 
        
        __M_writer(u'\n')
        # SOURCE LINE 30
        for item in renderList:
            # SOURCE LINE 31
            __M_writer(u'         ')
 
            if c.demo:
               author = userLib.getUserByID(item.owner)
               if not c.privs['admin']:
                  if 'user' in session:
                     if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                        continue
                  else:
                     if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                        continue
            author = userLib.getUserByID(item.owner)
            
            authorClass = 'row-fluid list-item'
            addedAs = ''
            if item['addedAs'] == 'admin':
                authorClass += ' admin'
                addedAs += '(admin) '
            if item['addedAs'] == 'facilitator':
                authorClass += ' facilitator'
                addedAs += '(facilitator) '
            if item['addedAs'] == 'listener':
                authorClass += ' listener'
                addedAs += '(listener) '
                     
            
            # SOURCE LINE 54
            __M_writer(u'\n         <li>\n')
            # SOURCE LINE 56
            if item['disabled'] == '1':
                # SOURCE LINE 57
                __M_writer(u'                <div class="accordion" id="item-')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'">\n                    <div class="accordion-group no-border">\n                        <div class="accordion-heading disabled">\n                            <div class="collapsed-item-header">\n                                <button class="accordion-toggle inline btn btn-mini collapsed" data-toggle="collapse" data-parent="#item-')
                # SOURCE LINE 61
                __M_writer(escape(item['urlCode']))
                __M_writer(u'" href="#item-body-')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'">Show</button>\n                                ')
                # SOURCE LINE 62

                (disabler, reason) = getDisabledMessage(item)
                                                
                
                # SOURCE LINE 64
                __M_writer(u'\n                                <small>This item has been disabled by ')
                # SOURCE LINE 65
                __M_writer(escape(lib_6.userLink(disabler)))
                __M_writer(u' because: ')
                __M_writer(escape(reason))
                __M_writer(u'</small>\n                            </div>\n                            <div class="accordion-body collapse" id="item-body-')
                # SOURCE LINE 67
                __M_writer(escape(item['urlCode']))
                __M_writer(u'">\n                                <div class="row-fluid list-item">\n')
                # SOURCE LINE 69
                if thing != 'resources':
                    # SOURCE LINE 70
                    __M_writer(u'                                        <div class="span2 offset1">\n                                            ')
                    # SOURCE LINE 71
                    __M_writer(escape(lib_6.userImage(author, className = 'avatar')))
                    __M_writer(u'\n                                        </div> <!--/.span2-->\n')
                    pass
                # SOURCE LINE 74
                __M_writer(u'                                    <div class="span9 list-item-text" id="content_')
                __M_writer(escape(itemCounter))
                __M_writer(u'">\n                                        ')
                # SOURCE LINE 75
                itemTitle = '<h5 class="no-bottom"><a %s class="listed-item-title">%s</a></h5>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) 
                
                __M_writer(u'\n                                        ')
                # SOURCE LINE 76
                __M_writer(itemTitle )
                __M_writer(u'\n')
                # SOURCE LINE 77
                if item.objType == 'resource':
                    # SOURCE LINE 78
                    __M_writer(u'                                            <p>\n                                            ')
                    # SOURCE LINE 79
                    itemLink = '<small>(<a %s>%s</a>)</small>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), lib_6.ellipsisIZE(item['link'], 75)) 
                    
                    __M_writer(u'\n                                            ')
                    # SOURCE LINE 80
                    __M_writer(itemLink )
                    __M_writer(u'\n                                            </p>\n')
                    pass
                # SOURCE LINE 83
                __M_writer(u'                                        <p class="no-bottom">\n                                            <small>Posted by ')
                # SOURCE LINE 84
                __M_writer(escape(lib_6.userLink(item.owner)))
                __M_writer(u' ')
                __M_writer(escape(addedAs))
                __M_writer(u'from ')
                __M_writer(escape(lib_6.userGeoLink(item.owner)))
                __M_writer(u' ')
                __M_writer(escape(item.date))
                __M_writer(u'</small>\n                                        </p>\n                                            ')
                # SOURCE LINE 86
 
                comments = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'comments') 
                numComments = discussionLib.getDiscussionForThing(item)['numComments']
                                                            
                
                # SOURCE LINE 89
                __M_writer(u'\n')
                # SOURCE LINE 90
                if c.demo:
                    # SOURCE LINE 91
                    __M_writer(u'                                                See ')
                    __M_writer(comments )
                    __M_writer(u'\n')
                    # SOURCE LINE 92
                else:
                    # SOURCE LINE 93
                    __M_writer(u'                                                See ')
                    __M_writer(comments )
                    __M_writer(u' (')
                    __M_writer(escape(numComments))
                    __M_writer(u') \n')
                    pass
                # SOURCE LINE 95
                __M_writer(u'                                    </div><!--/.span9-->\n                                    ')
                # SOURCE LINE 108
                __M_writer(u'\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n                </div>\n')
                # SOURCE LINE 114
            else:
                # SOURCE LINE 115
                __M_writer(u'                <div class="row-fluid list-item border-bottom">\n')
                # SOURCE LINE 116
                if not 'condensed' in args:
                    # SOURCE LINE 117
                    __M_writer(u'                        <div class="span1 voteBlock" id="vote_')
                    __M_writer(escape(itemCounter))
                    __M_writer(u'">\n                            ')
                    # SOURCE LINE 118
                    __M_writer(escape(lib_6.upDownVote(item)))
                    __M_writer(u'\n                        </div>\n')
                    pass
                # SOURCE LINE 121
                __M_writer(u'                    ')

                if 'condensed' in args:
                    spanX = "span2"
                else:
                    spanX = "span1"
                                    
                
                # SOURCE LINE 126
                __M_writer(u'\n')
                # SOURCE LINE 127
                if thing == 'resources':
                    # SOURCE LINE 128
                    __M_writer(u'                        ')
 
                    iconClass = ""
                    if item['type'] == 'link' or item['type'] == 'general':
                        iconClass="icon-link"
                    elif item['type'] == 'photo':
                        iconClass="icon-picture"
                    elif item['type'] == 'video':
                        iconClass="icon-youtube-play"
                    elif item['type'] == 'rich':
                        iconClass="icon-file"
                    endif
                                            
                    
                    # SOURCE LINE 139
                    __M_writer(u'\n                        <div class="')
                    # SOURCE LINE 140
                    __M_writer(escape(spanX))
                    __M_writer(u'">\n                            <div class="spacer"></div>\n                            <i class="')
                    # SOURCE LINE 142
                    __M_writer(escape(iconClass))
                    __M_writer(u' icon-3x"></i>\n                        </div>\n')
                    # SOURCE LINE 144
                elif not 'condensed' in args:
                    # SOURCE LINE 145
                    __M_writer(u'                        <div class="')
                    __M_writer(escape(spanX))
                    __M_writer(u'">\n                            <div class="spacer"></div>\n                            <i class="icon-comments icon-3x"></i>\n                        </div> <!--/.span2-->\n')
                    pass
                # SOURCE LINE 150
                __M_writer(u'                    ')

                spanY = "span10"
                discStyle = ''
                if thing == 'discussion':
                    discStyle = "forum-topic"
                    if 'condensed' in args:
                        spanY = "span12"
                                    
                
                # SOURCE LINE 157
                __M_writer(u'\n                    <div class="')
                # SOURCE LINE 158
                __M_writer(escape(spanY))
                __M_writer(u' list-item-text" id="content_')
                __M_writer(escape(itemCounter))
                __M_writer(u'">\n                        <h4 class="media-heading ')
                # SOURCE LINE 159
                __M_writer(escape(discStyle))
                __M_writer(u'">\n                            ')
                # SOURCE LINE 160
                itemTitle = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) 
                
                __M_writer(u'\n                            ')
                # SOURCE LINE 161
                __M_writer(itemTitle )
                __M_writer(u'\n                        </h4>\n\n')
                # SOURCE LINE 164
                if item.objType == 'resource':
                    # SOURCE LINE 165
                    __M_writer(u'                            ')
 
                    if 'condensed' in args:
                        chars = 35
                    else:
                        chars = 70
                    itemLink = '<a %s>%s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=True), lib_6.ellipsisIZE(item['link'], chars)) 
                    
                    # SOURCE LINE 170
                    __M_writer(u'\n\n                            ')
                    # SOURCE LINE 172
                    __M_writer(itemLink )
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 174
                __M_writer(u'\n                            ')
                # SOURCE LINE 175
 
                comments = '<a %s class="listed-item-title"><i class="icon-comments"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), ' Comments') 
                numComments = discussionLib.getDiscussionForThing(item)['numComments']
                if 'views' in item:
                    numViews = str(item['views'])
                else:
                    numViews = "0"
                                            
                
                # SOURCE LINE 182
                __M_writer(u'\n                            <br />\n                            <ul class="horizontal-list iconListing">\n                                <li>\n')
                # SOURCE LINE 186
                if c.demo:
                    # SOURCE LINE 187
                    __M_writer(u'                                        ')
                    __M_writer(comments )
                    __M_writer(u'\n')
                    # SOURCE LINE 188
                else:
                    # SOURCE LINE 189
                    __M_writer(u'                                        ')
                    __M_writer(comments )
                    __M_writer(u' (')
                    __M_writer(escape(numComments))
                    __M_writer(u')\n')
                    pass
                # SOURCE LINE 191
                __M_writer(u'                                </li>\n                                <li>\n                                    <i class="icon-eye-open"></i> Views ')
                # SOURCE LINE 193
                __M_writer(escape(numViews))
                __M_writer(u'\n                                </li>\n\n')
                # SOURCE LINE 196
                if item.objType != 'resource':
                    # SOURCE LINE 197
                    if not 'condensed' in args:
                        # SOURCE LINE 198
                        __M_writer(u'                                    <li><span id="author_')
                        __M_writer(escape(itemCounter))
                        __M_writer(u'" class="left-space">')
                        __M_writer(escape(lib_6.userImage(author, className = 'avatar topbar-avatar')))
                        __M_writer(u'</span><small> Posted by ')
                        __M_writer(escape(lib_6.userLink(item.owner)))
                        __M_writer(u' ')
                        __M_writer(escape(addedAs))
                        __M_writer(u' from ')
                        __M_writer(escape(lib_6.userGeoLink(item.owner)))
                        __M_writer(u' ')
                        __M_writer(escape(item.date))
                        __M_writer(u'</small></li>\n')
                        pass
                    pass
                # SOURCE LINE 201
                __M_writer(u'                            </ul>\n                    </div><!--/.span9-->\n                </div><!--/.row-fluid-->\n')
                pass
            # SOURCE LINE 205
            __M_writer(u'         </li>\n         ')
            # SOURCE LINE 206
            itemCounter += 1 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 208
        __M_writer(u'   </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_getDisabledMessage(context,thing):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 343
        __M_writer(u'\n    ')
        # SOURCE LINE 344

        event = eventLib.getEventsWithAction(thing, 'disabled')[0]
        disabler = userLib.getUserByID(event.owner)
        reason = event['reason']
        return (disabler, reason)
            
        
        # SOURCE LINE 349
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showIdeaListing(context,thing):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        int = context.get('int', UNDEFINED)
        def getDisabledMessage(thing):
            return render_getDisabledMessage(context,thing)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 211
        __M_writer(u'\n   ')
        # SOURCE LINE 212

        target = "_self"
        if c.paginator != '':
           renderList = c.paginator
        else:
           if thing == 'ideas':
              renderList = c.ideas
              
           
        
        # SOURCE LINE 220
        __M_writer(u'\n   <ul class="unstyled">\n      ')
        # SOURCE LINE 222
        itemCounter = 0 
        
        __M_writer(u'\n')
        # SOURCE LINE 223
        for item in renderList:
            # SOURCE LINE 224
            __M_writer(u'         ')
 
            if c.demo:
               author = userLib.getUserByID(item.owner)
               if not c.privs['admin']:
                  if 'user' in session:
                     if ((author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w)) and author.id != c.authuser.id):
                        continue
                  else:
                     if author['accessLevel'] != '300' and not facilitatorLib.isFacilitator(author, c.w):
                        continue
            author = userLib.getUserByID(item.owner)
            
            authorClass = 'row-fluid list-item'
            addedAs = ''
            if item['addedAs'] == 'admin':
                authorClass += ' admin'
                addedAs += '(admin) '
            if item['addedAs'] == 'facilitator':
                authorClass += ' facilitator'
                addedAs += '(facilitator) '
            if item['addedAs'] == 'listener':
                authorClass += ' listener'
                addedAs += '(listener) '
                     
            
            # SOURCE LINE 247
            __M_writer(u'\n         <li>\n')
            # SOURCE LINE 249
            if item['disabled'] == '1':
                # SOURCE LINE 250
                __M_writer(u'                <div class="accordion" id="item-')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'">\n                    <div class="accordion-group no-border">\n                        <div class="accordion-heading disabled">\n                            <div class="collapsed-item-header">\n                                <button class="accordion-toggle inline btn btn-mini collapsed" data-toggle="collapse" data-parent="#item-')
                # SOURCE LINE 254
                __M_writer(escape(item['urlCode']))
                __M_writer(u'" href="#item-body-')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'">Show</button>\n                                ')
                # SOURCE LINE 255

                (disabler, reason) = getDisabledMessage(item)
                                                
                
                # SOURCE LINE 257
                __M_writer(u'\n                                <small>This item has been disabled by ')
                # SOURCE LINE 258
                __M_writer(escape(lib_6.userLink(disabler)))
                __M_writer(u' because: ')
                __M_writer(escape(reason))
                __M_writer(u'</small>\n                            </div>\n                            <div class="accordion-body collapse" id="item-body-')
                # SOURCE LINE 260
                __M_writer(escape(item['urlCode']))
                __M_writer(u'">\n                                <div class="row-fluid list-item border-bottom">\n                                    <div class="span9 offset1 list-item-text ideaListing" style="position:relative;" id="content_')
                # SOURCE LINE 262
                __M_writer(escape(itemCounter))
                __M_writer(u'">\n                                        ')
                # SOURCE LINE 263
                itemTitle = '<p class="ideaListingTitle"><a %s class="listed-item-title">%s</a></p>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) 
                
                __M_writer(u'\n                                        ')
                # SOURCE LINE 264
                __M_writer(itemTitle )
                __M_writer(u'\n')
                # SOURCE LINE 265
                if item['adopted'] == '1':
                    # SOURCE LINE 266
                    __M_writer(u'                                            <small><i class="icon-star"></i> This idea adopted!</small>\n')
                    pass
                # SOURCE LINE 268
                __M_writer(u'                                        <p style="margin-top: 10px;">')
                __M_writer(escape(lib_6.ellipsisIZE(item['text'], 250)))
                __M_writer(u'</p>\n                                            ')
                # SOURCE LINE 269
 
                comments = '<a %s class="listed-item-title"><i class="icon-comment"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Comments')
                fullText = '<a %s class="listed-item-title"><i class="icon-file-text"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Read full text') 
                numComments = discussionLib.getDiscussionForThing(item)['numComments']
                
                totalVotes = int(item['ups']) + int(item['downs'])
                                                            
                
                # SOURCE LINE 275
                __M_writer(u'\n                                            <ul class="horizontal-list iconListing">\n                                                <li>')
                # SOURCE LINE 277
                __M_writer(escape(lib_6.userImage(author, className = 'avatar topbar-avatar')))
                __M_writer(u'</span> Posted by ')
                __M_writer(escape(lib_6.userLink(item.owner)))
                __M_writer(u' ')
                __M_writer(escape(addedAs))
                __M_writer(u' ')
                __M_writer(escape(item.date))
                __M_writer(u'</li>\n                                                <li>')
                # SOURCE LINE 278
                __M_writer(fullText )
                __M_writer(u'</li>\n')
                # SOURCE LINE 279
                if c.demo:
                    # SOURCE LINE 280
                    __M_writer(u'                                                    <li>')
                    __M_writer(comments )
                    __M_writer(u'</li>\n')
                    # SOURCE LINE 281
                else:
                    # SOURCE LINE 282
                    __M_writer(u'                                                    <li>')
                    __M_writer(comments )
                    __M_writer(u' (')
                    __M_writer(escape(numComments))
                    __M_writer(u')</li>\n')
                    pass
                # SOURCE LINE 284
                __M_writer(u'                                            </ul>\n                                    </div><!--/.span9-->\n                                    <div class="span3 voteBlock ideaListing" id="vote_')
                # SOURCE LINE 286
                __M_writer(escape(itemCounter))
                __M_writer(u'">\n                                        ')
                # SOURCE LINE 287
                __M_writer(escape(lib_6.yesNoVote(item)))
                __M_writer(u'\n                                    </div>\n                                </div><!--/.row-fluid-->\n                            </div><!-- accordion body -->\n                        </div><!-- accordion heading -->\n                    </div><!-- accordion group -->\n                </div><!-- accordion --> \n')
                # SOURCE LINE 294
            else:
                # SOURCE LINE 295
                __M_writer(u'                <div class="row-fluid list-item border-bottom">\n                    <div class="span9 list-item-text ideaListing" id="content_')
                # SOURCE LINE 296
                __M_writer(escape(itemCounter))
                __M_writer(u'">\n                        ')
                # SOURCE LINE 297
                itemTitle = '<p class="ideaListingTitle"><a %s class="listed-item-title">%s</a></p>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), lib_6.ellipsisIZE(item['title'], 150)) 
                
                __M_writer(u'\n                        ')
                # SOURCE LINE 298
                __M_writer(itemTitle )
                __M_writer(u'\n')
                # SOURCE LINE 299
                if item['adopted'] == '1':
                    # SOURCE LINE 300
                    __M_writer(u'                            <small><i class="icon-star"></i> This idea adopted!</small>\n')
                    pass
                # SOURCE LINE 302
                __M_writer(u'                        <p style="margin-top: 10px;">')
                __M_writer(escape(lib_6.ellipsisIZE(item['text'], 250)))
                __M_writer(u'</p>\n                            ')
                # SOURCE LINE 303
 
                comments = '<a %s class="listed-item-title"><i class="icon-comment"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Comments')
                fullText = '<a %s class="listed-item-title"><i class="icon-file-text"></i> %s</a>' %(lib_6.thingLinkRouter(item, c.w, embed=True, directLink=False), 'Read full text')
                numComments = "0"
                if 'numComments' in item:
                    numComments = item['numComments']
                    
                #numComments = discussionLib.getDiscussionForThing(item)['numComments']
                if 'views' in item:
                    numViews = str(item['views'])
                else:
                    numViews = "0"
                views = '<i class="icon-eye-open"></i> Views %s</a>'%numViews
                
                totalVotes = int(item['ups']) + int(item['downs'])
                                            
                
                # SOURCE LINE 318
                __M_writer(u'\n                            <ul class="horizontal-list iconListing">\n                                <li>')
                # SOURCE LINE 320
                __M_writer(escape(lib_6.userImage(author, className = 'avatar topbar-avatar')))
                __M_writer(u'</span> Posted by ')
                __M_writer(escape(lib_6.userLink(item.owner)))
                __M_writer(u' ')
                __M_writer(escape(addedAs))
                __M_writer(u' on ')
                __M_writer(escape(item.date))
                __M_writer(u'</li>\n                            </ul><br />\n                            <ul class="horizontal-list iconListing">\n                                <li>')
                # SOURCE LINE 323
                __M_writer(fullText )
                __M_writer(u'</li>\n')
                # SOURCE LINE 324
                if c.demo:
                    # SOURCE LINE 325
                    __M_writer(u'                                    <li>')
                    __M_writer(comments )
                    __M_writer(u'</li>\n')
                    # SOURCE LINE 326
                else:
                    # SOURCE LINE 327
                    __M_writer(u'                                    <li>')
                    __M_writer(comments )
                    __M_writer(u' (')
                    __M_writer(escape(numComments))
                    __M_writer(u')</li>\n')
                    pass
                # SOURCE LINE 329
                __M_writer(u'                                <li>')
                __M_writer(views )
                __M_writer(u'</li>\n                            </ul>\n                    </div><!--/.span9-->\n                    <div class="span3 voteBlock ideaListing well" style="background-color: whiteSmoke;" id="vote_')
                # SOURCE LINE 332
                __M_writer(escape(itemCounter))
                __M_writer(u'">\n                        ')
                # SOURCE LINE 333
                __M_writer(escape(lib_6.yesNoVote(item)))
                __M_writer(u'\n                    </div>\n                </div><!--/.row-fluid-->\n')
                pass
            # SOURCE LINE 337
            __M_writer(u'         </li>\n         ')
            # SOURCE LINE 338
            itemCounter += 1 
            
            __M_writer(u'\n')
            pass
        # SOURCE LINE 340
        __M_writer(u'   </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


