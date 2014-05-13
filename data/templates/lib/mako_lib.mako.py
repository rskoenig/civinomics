# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398463803.0434649
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/mako_lib.mako'
_template_uri = u'/lib/mako_lib.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['fields_alert', 'slideshowHandler', 'facilitator', 'civ_col_img', 'formatEmail', 'setLastPage', 'nav_thing', 'totalSuggestions', 'setProduct', 'setCurrentSurveyPage', 'add_a_text', 'displayProfilePicture', 'add_a', 'displayEvents', 'slideshow', 'displayWorkshopHeader', 'your_facilitator', 'return_to', 'displayFeedbackSlider', 'list_resources', 'gravatar', 'avatar', 'list_suggestions', 'totalResources']


# SOURCE LINE 1
    
import logging
from ordereddict import OrderedDict
log = logging.getLogger(__name__)
from pylowiki.lib.db.flag import getFlags
from pylowiki.lib.db.discussion import getDiscussionByID
from pylowiki.lib.db.user import isAdmin, getUserByID
from pylowiki.lib.db.facilitator import isFacilitator
from pylowiki.lib.db.resource import getResourcesByParentID


# SOURCE LINE 101
 
from pylowiki.lib.db.user import getUserByID
from pylowiki.lib.db.slideshow import getAllSlides
from pylowiki.lib.fuzzyTime import timeSince


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'\n\n')
        # SOURCE LINE 15
        __M_writer(u'\n')
        # SOURCE LINE 23
        __M_writer(u'\n\n')
        # SOURCE LINE 29
        __M_writer(u'\n\n')
        # SOURCE LINE 40
        __M_writer(u'\n\n')
        # SOURCE LINE 50
        __M_writer(u'\n\n')
        # SOURCE LINE 70
        __M_writer(u'\n\n')
        # SOURCE LINE 75
        __M_writer(u'\n')
        # SOURCE LINE 87
        __M_writer(u'\n\n')
        # SOURCE LINE 96
        __M_writer(u'\n\n')
        # SOURCE LINE 105
        __M_writer(u'\n\n')
        # SOURCE LINE 131
        __M_writer(u'\n\n')
        # SOURCE LINE 145
        __M_writer(u'\n\n')
        # SOURCE LINE 162
        __M_writer(u'\n\n')
        # SOURCE LINE 240
        __M_writer(u'\n\n')
        # SOURCE LINE 258
        __M_writer(u'\n\n')
        # SOURCE LINE 371
        __M_writer(u'\n\n')
        # SOURCE LINE 389
        __M_writer(u'\n\n')
        # SOURCE LINE 397
        __M_writer(u'\n\n')
        # SOURCE LINE 428
        __M_writer(u'\n\n')
        # SOURCE LINE 439
        __M_writer(u'\n\n')
        # SOURCE LINE 467
        __M_writer(u'\n\n')
        # SOURCE LINE 507
        __M_writer(u'\n\n')
        # SOURCE LINE 558
        __M_writer(u'\n\n')
        # SOURCE LINE 569
        __M_writer(u'\n\n')
        # SOURCE LINE 586
        __M_writer(u'\n\n')
        # SOURCE LINE 611
        __M_writer(u'\n\n')
        # SOURCE LINE 624
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_fields_alert(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 147
        __M_writer(u'\n')
        # SOURCE LINE 148
        if 'alert' in session:
            # SOURCE LINE 149
            __M_writer(u'        ')
            alert = session['alert'] 
            
            __M_writer(u' \n        <div class="alert alert-')
            # SOURCE LINE 150
            __M_writer(escape(alert['type']))
            __M_writer(u'">\n            <button data-dismiss="alert" class="close">x</button>\n            <strong>')
            # SOURCE LINE 152
            __M_writer(escape(alert['title']))
            __M_writer(u'</strong>\n')
            # SOURCE LINE 153
            if 'content' in alert:
                # SOURCE LINE 154
                __M_writer(u'                ')
                __M_writer(escape(alert['content']))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 156
            __M_writer(u'        </div>\n        ')
            # SOURCE LINE 157
 
            session.pop('alert')
            session.save()
                    
            
            # SOURCE LINE 160
            __M_writer(u'\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_slideshowHandler(context,counter):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 509
        __M_writer(u'\n\t<script type="text/javascript">\n    \tvar onAfter = function(curr, next, opts) {\n\t\t\t$(\'.caption')
        # SOURCE LINE 512
        __M_writer(escape(counter))
        __M_writer(u'\').html(next.firstElementChild.title);\n    \t}\n    \tvar pagerBuilder = function(index, slide) {\n    \t\timg = $(slide).find(\'img\');\n    \t\treturn "<li><a href=\'#\'><img src=\'" + img.attr(\'src\') + "\'></a></li>"\n    \t}\n    \t$(function(){\n    \t\t$(\'.caption')
        # SOURCE LINE 519
        __M_writer(escape(counter))
        __M_writer(u"').html(\n    \t\t\t$(this).parent('#slideshow")
        # SOURCE LINE 520
        __M_writer(escape(counter))
        __M_writer(u"').find('.slideshow>slide:visible').find('a').attr('title')\n\t\t\t);\n\t    \t$('.slideshow")
        # SOURCE LINE 522
        __M_writer(escape(counter))
        __M_writer(u"')\n\t    \t\t.cycle({\n\t\t    \t\tfx: 'fade',\n\t\t    \t\tpause: true,\n\t\t    \t\tnext: $('#next")
        # SOURCE LINE 526
        __M_writer(escape(counter))
        __M_writer(u"'),\n\t\t    \t\tprev: $('#prev")
        # SOURCE LINE 527
        __M_writer(escape(counter))
        __M_writer(u"'),\n\t\t    \t\tafter: onAfter,\n\t\t    \t\ttimeout: 0,\n\t\t    \t\tpager: '#nav")
        # SOURCE LINE 530
        __M_writer(escape(counter))
        __M_writer(u"',\n\t\t    \t\tpagerAnchorBuilder: pagerBuilder\n\t\t    \t})\n\t\t    \t.touchwipe({\n\t\t    \t\twipeLeft: function() {\n\t\t    \t\t\t$('#next")
        # SOURCE LINE 535
        __M_writer(escape(counter))
        __M_writer(u"').click();\n\t\t    \t\t},\n\t\t    \t\twipeRight: function() {\n\t\t    \t\t\t$('#prev")
        # SOURCE LINE 538
        __M_writer(escape(counter))
        __M_writer(u"').click();\n\t\t    \t\t},\n\t\t    \t\tmin_move_x: 20,\n\t\t    \t\tmin_move_y: 20,\n\t\t    \t\tpreventDefaultEvents: true\n\t\t\t\t});\n\t\t\t$('#pager")
        # SOURCE LINE 544
        __M_writer(escape(counter))
        __M_writer(u"').hover(\n\t\t\t\tfunction(){\n\t\t\t\t\t$(this).animate({\n\t\t\t\t\t\t'opacity': 100\n\t\t\t\t\t}, 1000);\n\t\t\t\t},\n\t\t\t\tfunction(){\n\t\t\t\t\t$(this).animate({\n\t\t\t\t\t\t'opacity': 0\n\t\t\t\t\t}, 1000);\n\t\t\t\t}\n\t\t\t);\n    \t})\n\t</script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_facilitator(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 391
        __M_writer(u'\n')
        # SOURCE LINE 392
        if len(c.facilitators) == 1:
            # SOURCE LINE 393
            __M_writer(u'\t\tfacilitator\n')
            # SOURCE LINE 394
        else:
            # SOURCE LINE 395
            __M_writer(u'\t\tfacilitators\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_civ_col_img(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 430
        __M_writer(u'\n\t<script type="text/javascript">\n\t\t$(window).load(function() {\n\t\t\t$(\'.civ-img-cap\').each(function(){\n\t\t\t\t$(this).width($(this).find(\'img\').width());\n\t\t\t})\n\t\t\t$(\'.civ-img-cap .cap\').css({\'textAlign\': \'left\', \'right\': 0});\n\t\t})\n\t</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_formatEmail(context,email,subject='',style=0):
    context.caller_stack._push_frame()
    try:
        ord = context.get('ord', UNDEFINED)
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 52
        __M_writer(u'\n\t')
        # SOURCE LINE 53

        half = (len(email) // 2) * 6 #*6 because each character will now be six chars long: &, #, ;, and three digits.
        email = ''.join(["&#" + str(ord(c)).zfill(3) + ";" for c in email]) #this might be overdoing it?
        cssclass = 'generatedemail'
        if style == 0:
                withspan = email[:half] + '<span class="emailhide">nope</span>' + email[half:]
        else:
                cssclass = 'generatedemail btn btn-large'
                if (style & 1) == 1:
                        cssclass += ' btn-default'
                if (style & 2) == 2:
                        cssclass += ' btn-primary'
                if (style & 4) == 4:
                        cssclass += ' btn-success'
                withspan = subject
                
        
        # SOURCE LINE 68
        __M_writer(u'\n\t<a class="')
        # SOURCE LINE 69
        __M_writer(escape(cssclass))
        __M_writer(u'" data-end="')
        __M_writer(email[half:] )
        __M_writer(u'" data-subject="')
        __M_writer(escape(subject))
        __M_writer(u'" data-start="')
        __M_writer(email[:half] )
        __M_writer(u'">')
        __M_writer(withspan )
        __M_writer(u'</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_setLastPage(context,pageNum,survey,slide):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 76
        __M_writer(u'\n    ')
        # SOURCE LINE 77
 
        if slide['surveySection'] == 'before':
            key = '%s_%s_lastPage' %(survey['urlCode'], survey['url'])
            if key in session:
                if int(session[key]) < pageNum:
                    session[key] = pageNum
            else:
                session[key] = pageNum
            session.save()
            
        
        # SOURCE LINE 86
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_nav_thing(context,page):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 441
        __M_writer(u'\n    ')
        # SOURCE LINE 442

        if 'user' in session:
               pages = OrderedDict([("home",""), ("dashboard", "dashboard"), ("background", "background"), ("leaderboard", "leaderboard"), ("discussion", "discussion")])
        else:
               pages = OrderedDict([("home",""), ("background", "background"), ("discussion", "discussion")])
            
        
        # SOURCE LINE 447
        __M_writer(u'\n\n\t<ul class="unstyled nav-thing">\n')
        # SOURCE LINE 450
        for li in pages.keys():
            # SOURCE LINE 451
            __M_writer(u'        ')
            lclass="nothingspecial" 
            
            __M_writer(u'\n')
            # SOURCE LINE 452
            if page == li:
                # SOURCE LINE 453
                __M_writer(u'            ')
                lclass="current" 
                
                __M_writer(u'\n')
                pass
            # SOURCE LINE 455
            if li == 'dashboard':
                # SOURCE LINE 456
                if c.conf['read_only.value'] == 'true':
                    # SOURCE LINE 457
                    __M_writer(u'                ')
                    continue 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 459
                if 'user' in session and (isAdmin(c.authuser.id) or isFacilitator(c.authuser.id, c.w.id)):
                    # SOURCE LINE 460
                    __M_writer(u'\t\t\t    <li class="')
                    __M_writer(escape(lclass))
                    __M_writer(u'"><a href="/workshop/')
                    __M_writer(escape(c.w['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.w['url']))
                    __M_writer(u'/')
                    __M_writer(escape(pages[li]))
                    __M_writer(u'">')
                    __M_writer(escape(li.capitalize()))
                    __M_writer(u'</a></li>\n')
                    pass
                # SOURCE LINE 462
            else:
                # SOURCE LINE 463
                __M_writer(u'            <li class="')
                __M_writer(escape(lclass))
                __M_writer(u'"><a href="/workshop/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/')
                __M_writer(escape(pages[li]))
                __M_writer(u'">')
                __M_writer(escape(li.capitalize()))
                __M_writer(u'</a></li>\n')
                pass
            pass
        # SOURCE LINE 466
        __M_writer(u'\t</ul> <!-- /.nav-thing -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_totalSuggestions(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 373
        __M_writer(u'\n    ')
        # SOURCE LINE 374

        if c.suggestions:
            total = len(c.suggestions)
        else:
            total = 0
            
        
        # SOURCE LINE 379
        __M_writer(u'\n        <br />\n        <p class="total">\n                ')
        # SOURCE LINE 382
        __M_writer(escape(total))
        __M_writer(u'<br>\n                <span>Suggestions</span><br />\n')
        # SOURCE LINE 384
        if len(c.suggestions) > 15:
            # SOURCE LINE 385
            __M_writer(u'                    <span>Display Page ')
            __M_writer(escape( c.paginator.pager('~3~')))
            __M_writer(u'</span><br />\n')
            pass
        # SOURCE LINE 387
        __M_writer(u'                <span><a href="/workshop/')
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'">Back to Workshop</a></span>\n        </p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_setProduct(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 42
        __M_writer(u'\n\t')
        # SOURCE LINE 43

        if 'survey' in request.path_info:
                session['product'] = 'surveys'
        elif 'workshop' in request.path_info:
                session['product'] = 'workshops'
        session.save()
                
        
        # SOURCE LINE 49
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_setCurrentSurveyPage(context,survey,slide):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        map = context.get('map', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 89
        __M_writer(u'\n    ')
        # SOURCE LINE 90
 
        if slide.id in map(int, survey['slides'].split(',')):
            key = '%s_%s_currentPage' %(survey['urlCode'], survey['url'])
            session[key] = int(slide['slideNum'])
            session.save()
            
        
        # SOURCE LINE 95
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_add_a_text(context,thing,prefix):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 133
        __M_writer(u'\n')
        # SOURCE LINE 134
        if c.isScoped or c.isFacilitator or c.isAdmin:
            # SOURCE LINE 135
            if thing == 'resource' and (c.w['allowResources'] == '1' or c.isFacilitator or c.isAdmin):
                # SOURCE LINE 136
                __M_writer(u'\t        ')
                __M_writer(escape(prefix))
                __M_writer(u' <a href="/newResource/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'" title="Click to add a new information resource to this workshop">Add Resource</a>\n')
                # SOURCE LINE 137
            elif thing == 'sresource' and (c.s['allowComments'] == '1' or c.isFacilitator or c.isAdmin):
                # SOURCE LINE 138
                __M_writer(u'\t        ')
                __M_writer(escape(prefix))
                __M_writer(u' <a href="/newSResource/')
                __M_writer(escape(c.s['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.s['url']))
                __M_writer(u'" title="Click to add a new information resource to this suggestion">Add Resource</a>\n')
                # SOURCE LINE 139
            elif thing == 'suggestion' and (c.w['allowSuggestions'] == '1' or c.isFacilitator or c.isAdmin):
                # SOURCE LINE 140
                __M_writer(u'\t        ')
                __M_writer(escape(prefix))
                __M_writer(u' <a href="/newSuggestion/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'" title="Click to add a new suggestion to this workshop">Add Suggestion</a>\n')
                # SOURCE LINE 141
            elif thing == 'discussion':
                # SOURCE LINE 142
                __M_writer(u'\t        ')
                __M_writer(escape(prefix))
                __M_writer(u' <a href="/workshop/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/addDiscussion" title="Click to add a general discussion topic to this workshop">Add Discussion Topic</a>\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayProfilePicture(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 560
        __M_writer(u'\n        <br />\n')
        # SOURCE LINE 562
        if c.authuser['pictureHash'] == 'flash':
            # SOURCE LINE 563
            __M_writer(u'\t\t<a href="/profile/')
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'"><img src="/images/avatars/flash.profile" alt="')
            __M_writer(escape(c.authuser['name']))
            __M_writer(u'" title="')
            __M_writer(escape(c.authuser['name']))
            __M_writer(u'" style="display:block; margin-left:auto; margin-right:auto; vertical-align:middle;" class="thumbnail"></a>\n')
            # SOURCE LINE 564
        else:
            # SOURCE LINE 565
            __M_writer(u'\t\t<a href="/profile/')
            __M_writer(escape(c.authuser['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.authuser['url']))
            __M_writer(u'">\n\t\t\t<img src="/images/avatar/')
            # SOURCE LINE 566
            __M_writer(escape(c.authuser['directoryNumber']))
            __M_writer(u'/profile/')
            __M_writer(escape(c.authuser['pictureHash']))
            __M_writer(u'.profile" alt="')
            __M_writer(escape(c.authuser['name']))
            __M_writer(u'" title="')
            __M_writer(escape(c.authuser['name']))
            __M_writer(u'" style="display:block; margin-left:auto; margin-right:auto; vertical-align:middle;" class="thumbnail">\n\t\t</a>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_add_a(context,thing):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 107
        __M_writer(u'\n')
        # SOURCE LINE 108
        if c.isScoped or c.isFacilitator or c.isAdmin:
            # SOURCE LINE 109
            if thing == 'resource' and (c.w['allowResources'] == '1' or c.isFacilitator or c.isAdmin):
                # SOURCE LINE 110
                __M_writer(u'\t        <a href="/newResource/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'" style="letter-spacing:normal;" title="Click to add a new information resource to this workshop" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>\n')
                # SOURCE LINE 111
            elif thing == 'sresource' and (c.s['allowComments'] == '1' or c.isFacilitator or c.isAdmin):
                # SOURCE LINE 112
                __M_writer(u'\t        <a href="/newSResource/')
                __M_writer(escape(c.s['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.s['url']))
                __M_writer(u'" title="Click to add a new information resource to this suggestion" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>\n')
                # SOURCE LINE 113
            elif thing == 'suggestion' and (c.w['allowSuggestions'] == '1' or c.isFacilitator or c.isAdmin):
                # SOURCE LINE 114
                __M_writer(u'\t        <a href="/newSuggestion/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'" title="Click to add a new suggestion to this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-pencil"></i></a>\n')
                # SOURCE LINE 115
            elif thing == 'discussion':
                # SOURCE LINE 116
                __M_writer(u'\t        <a href="/workshop/')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/addDiscussion" title="Click to add a general discussion topic to this workshop" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-folder-open"></i></a>\n')
                pass
            # SOURCE LINE 118
        else:
            # SOURCE LINE 119
            if 'user' not in session:
                # SOURCE LINE 120
                if thing == 'resource':
                    # SOURCE LINE 121
                    __M_writer(u'                <a href="/" style="letter-spacing:normal;" title="Sign Up or Log In to participate!" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>\n')
                    # SOURCE LINE 122
                elif thing == 'sresource':
                    # SOURCE LINE 123
                    __M_writer(u'                <a href="/" title="Sign Up or Log In to participate!" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-book"></i></a>\n')
                    # SOURCE LINE 124
                elif thing == 'suggestion':
                    # SOURCE LINE 125
                    __M_writer(u'                <a href="/" title="Sign Up or Log In to participate!" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-pencil"></i></a>\n')
                    # SOURCE LINE 126
                elif thing == 'discussion':
                    # SOURCE LINE 127
                    __M_writer(u'                <a href="/" title="Sign Up or Log In to participate!" style="text-decoration:none" class="btn btn-success btn-mini">add<i class="icon-white icon-folder-open"></i></a>\n')
                    pass
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayEvents(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 613
        __M_writer(u'\n')
        # SOURCE LINE 614
        if c.events:
            # SOURCE LINE 615
            __M_writer(u'        <h2 class="civ-col">Change Log</h2>\n\n        <ul class="unstyled">\n')
            # SOURCE LINE 618
            for e in c.events:
                # SOURCE LINE 619
                __M_writer(u'            ')
                eOwner = getUserByID(e.owner) 
                
                __M_writer(u'\n            <li>')
                # SOURCE LINE 620
                __M_writer(escape(e['title']))
                __M_writer(u' : by <a href="/profile/')
                __M_writer(escape(eOwner['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(eOwner['url']))
                __M_writer(u'">')
                __M_writer(escape(eOwner['name']))
                __M_writer(u'</a> ')
                __M_writer(escape(e.date))
                __M_writer(u' : ')
                __M_writer(escape(e['data']))
                __M_writer(u'</li>\n')
                pass
            # SOURCE LINE 622
            __M_writer(u'        </ul>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_slideshow(context,counter):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 469
        __M_writer(u'\n\t<div id="slideshow')
        # SOURCE LINE 470
        __M_writer(escape(counter))
        __M_writer(u'" class="slideshow-container" style="border:1px solid black; padding:4px;">\n\t\t<div id="pager')
        # SOURCE LINE 471
        __M_writer(escape(counter))
        __M_writer(u'" class="pager">\n\t\t\t<ul id="nav')
        # SOURCE LINE 472
        __M_writer(escape(counter))
        __M_writer(u'" class="unstyled">\n\t\t\t</ul>\n\t\t</div>\n\t\t<div id="prevNext')
        # SOURCE LINE 475
        __M_writer(escape(counter))
        __M_writer(u'" class="prevNext">\n\t\t\t<a id="prev')
        # SOURCE LINE 476
        __M_writer(escape(counter))
        __M_writer(u'" href="#"><i class=\'icon-backward icon-white\'></i></a>\n\t\t\t<a id="next')
        # SOURCE LINE 477
        __M_writer(escape(counter))
        __M_writer(u'" href="#"><i class=\'icon-forward icon-white\'></i></a>\n\t\t</div>\n\t\t<div class="slideshow')
        # SOURCE LINE 479
        __M_writer(escape(counter))
        __M_writer(u'">\n                ')
        # SOURCE LINE 480
 
        if c.slides:
            slideList = c.slides
        else:
            slideshowID = c.w['mainSlideshow_id']
            slideList = getAllSlides(slideshowID)
                        
        
        # SOURCE LINE 486
        __M_writer(u'\n')
        # SOURCE LINE 487
        for slide in slideList:
            # SOURCE LINE 488
            if slide['deleted'] != '1':
                # SOURCE LINE 489
                if slide['pictureHash'] == 'supDawg':
                    # SOURCE LINE 490
                    __M_writer(u'\t\t\t<div class="slide">\n\t\t\t\t<a title="')
                    # SOURCE LINE 491
                    __M_writer(escape(slide['title']))
                    __M_writer(u'<br/>')
                    __M_writer(escape(slide['caption']))
                    __M_writer(u'" href="#">\n                                <img src="/images/slide/slideshow/')
                    # SOURCE LINE 492
                    __M_writer(escape(slide['pictureHash']))
                    __M_writer(u'.slideshow" alt="<strong>')
                    __M_writer(escape(slide['title']))
                    __M_writer(u'</strong> ')
                    __M_writer(escape(slide['caption']))
                    __M_writer(u'"/>\n\t\t\t\t</a>\n\t\t\t</div> <!-- /.slide -->\n')
                    # SOURCE LINE 495
                else:
                    # SOURCE LINE 496
                    __M_writer(u'\t\t\t<div class="slide">\n\t\t\t\t<a title="')
                    # SOURCE LINE 497
                    __M_writer(escape(slide['title']))
                    __M_writer(u'<br/>')
                    __M_writer(escape(slide['caption']))
                    __M_writer(u'" href="#">\n                                <img src="/images/slide/')
                    # SOURCE LINE 498
                    __M_writer(escape(slide['directoryNumber']))
                    __M_writer(u'/slideshow/')
                    __M_writer(escape(slide['pictureHash']))
                    __M_writer(u'.slideshow" alt="<strong>')
                    __M_writer(escape(slide['title']))
                    __M_writer(u'</strong> ')
                    __M_writer(escape(slide['caption']))
                    __M_writer(u'"/>\n\t\t\t\t</a>\n\t\t\t</div> <!-- /.slide -->\n')
                    pass
                pass
            pass
        # SOURCE LINE 504
        __M_writer(u'\t\t</div> <!-- /.slideshow -->\n\t\t<div class="caption')
        # SOURCE LINE 505
        __M_writer(escape(counter))
        __M_writer(u' caption"></div>\n\t</div> <!-- slideshow -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayWorkshopHeader(context,page):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        def nav_thing(page):
            return render_nav_thing(context,page)
        __M_writer = context.writer()
        # SOURCE LINE 571
        __M_writer(u'\n   <div class="row-fluid">\n       <div class="span2">\n')
        # SOURCE LINE 574
        if c.w['mainImage_hash'] == 'supDawg':
            # SOURCE LINE 575
            __M_writer(u'                <a href="/workshops/')
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'"><img src="/images/')
            __M_writer(escape(c.w['mainImage_identifier']))
            __M_writer(u'/thumbnail/')
            __M_writer(escape(c.w['mainImage_hash']))
            __M_writer(u'.thumbnail" class="thumbnail" alt="')
            __M_writer(escape(c.w['title']))
            __M_writer(u'" title="')
            __M_writer(escape(c.w['title']))
            __M_writer(u'" style="width: 120px; height: 80px;"/></a>\n')
            # SOURCE LINE 576
        else:
            # SOURCE LINE 577
            __M_writer(u'                <a href="/workshops/')
            __M_writer(escape(c.w['urlCode']))
            __M_writer(u'/')
            __M_writer(escape(c.w['url']))
            __M_writer(u'"><img src="/images/')
            __M_writer(escape(c.w['mainImage_identifier']))
            __M_writer(u'/')
            __M_writer(escape(c.w['mainImage_directoryNum']))
            __M_writer(u'/thumbnail/')
            __M_writer(escape(c.w['mainImage_hash']))
            __M_writer(u'.thumbnail" alt="')
            __M_writer(escape(c.w['title']))
            __M_writer(u'" title="')
            __M_writer(escape(c.w['title']))
            __M_writer(u'" class="thumbnail left" style = "width: 120px; height: 80px;"/></a>\n')
            pass
        # SOURCE LINE 579
        __M_writer(u'        </div><!-- span3 -->\n        <div class="span9">\n            <h1><a href="/workshop/')
        # SOURCE LINE 581
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'">')
        __M_writer(escape(c.w['title']))
        __M_writer(u'</a></h1>\n            <br/>\n            ')
        # SOURCE LINE 583
        __M_writer(escape(nav_thing(page)))
        __M_writer(u'\n        </div><!-- span9 -->\n   </div><!-- row-fluid -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_your_facilitator(context):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 399
        __M_writer(u'\n')
        # SOURCE LINE 400
        if c.facilitators == '0' or len(c.facilitators) == 0:
            # SOURCE LINE 401
            __M_writer(u'        <div class="alert alert-warning">No facilitators!</div>\n')
            # SOURCE LINE 402
        else:
            # SOURCE LINE 403
            __M_writer(u'        <ul class="unstyled civ-col-list">\n')
            # SOURCE LINE 404
            for facilitator in c.facilitators:
                # SOURCE LINE 405
                __M_writer(u'            <li>\n            ')
                # SOURCE LINE 406
                fuser = getUserByID(facilitator.owner) 
                
                __M_writer(u'\n            <div class="row-fluid">\n                <div class="span2">\n')
                # SOURCE LINE 409
                if fuser['pictureHash'] == 'flash':
                    # SOURCE LINE 410
                    __M_writer(u'                    <a href="/profile/')
                    __M_writer(escape(fuser['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(fuser['url']))
                    __M_writer(u'"><img src="/images/avatars/flash.profile" style="width:40px;" alt="')
                    __M_writer(escape(fuser['name']))
                    __M_writer(u'" title="')
                    __M_writer(escape(fuser['name']))
                    __M_writer(u'" class="thumbnail"></a>\n')
                    # SOURCE LINE 411
                else:
                    # SOURCE LINE 412
                    __M_writer(u'                    <a href="/profile/')
                    __M_writer(escape(fuser['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(fuser['url']))
                    __M_writer(u'"><img src="/images/avatar/')
                    __M_writer(escape(fuser['directoryNumber']))
                    __M_writer(u'/profile/')
                    __M_writer(escape(fuser['pictureHash']))
                    __M_writer(u'.profile" style="width:40px;" alt="')
                    __M_writer(escape(fuser['name']))
                    __M_writer(u'" title="')
                    __M_writer(escape(fuser['name']))
                    __M_writer(u'" class="thumbnail"></a>\n')
                    pass
                # SOURCE LINE 414
                __M_writer(u'                </div><!-- span2 -->\n                <div class="span8">\n                    <a href="/profile/')
                # SOURCE LINE 416
                __M_writer(escape(fuser['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(fuser['url']))
                __M_writer(u'">')
                __M_writer(escape(fuser['name']))
                __M_writer(u'</a>\n                </div><!-- span8 -->\n            </div><!-- row-fluid --> \n            </li>\n')
                pass
            # SOURCE LINE 421
            __M_writer(u'        </ul>\n')
            # SOURCE LINE 422
            if c.motd and int(c.motd['enabled']) == '1':
                # SOURCE LINE 423
                __M_writer(u'            <p>Facilitator message:</p> ')
                __M_writer(escape(c.motd['messageSummary']))
                __M_writer(u'\n')
                # SOURCE LINE 424
            else:
                # SOURCE LINE 425
                __M_writer(u'\n')
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_return_to(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 16
        __M_writer(u'\n\n    ')
        # SOURCE LINE 18
 
        session['return_to'] = request.path_info 
        session.save()
        
        
        # SOURCE LINE 21
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_displayFeedbackSlider(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 588
        __M_writer(u'\n')
        # SOURCE LINE 589
        if "user" in session and c.isScoped:
            # SOURCE LINE 590
            __M_writer(u'        <h2 class="civ-col"><i class="icon-volume-up"></i> Feedback</h2>\n        <div class="civ-col-inner">\n            <div class="well workshop_header">\n                Provide feedback for the workshop facilitators.\n                What do you think about the running of this workshop?\n                <br /> <br />\n\n                <div id="ratings0" class="rating pull-left">\n                    <div id="overall_slider" class="ui-slider-container clearfix">\n')
            # SOURCE LINE 599
            if c.rating:
                # SOURCE LINE 600
                __M_writer(u'                            <div id="')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(c.w['url']))
                __M_writer(u'" class="small_slider" data1="0_')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(c.rating['rating']))
                __M_writer(u'_overall_true_rateFacilitation" data2="')
                __M_writer(escape(c.w['url']))
                __M_writer(u'"></div>\n')
                # SOURCE LINE 601
            else:
                # SOURCE LINE 602
                __M_writer(u'                            <div id="')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(c.w['url']))
                __M_writer(u'" class="small_slider" data1="0_')
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'_0_overall_false_rateFacilitation" data2="')
                __M_writer(escape(c.w['url']))
                __M_writer(u'"></div>\n')
                pass
            # SOURCE LINE 604
            __M_writer(u'                    </div><!-- overall_slider -->\n                </div><!-- ratings0 -->\n                <br /> <br />\n                <br /> <br />\n            </div><!-- well -->\n        </div><!-- civ-col-inner -->\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_list_resources(context,errorMsg,numDisplay=10):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 164
        __M_writer(u'\n')
        # SOURCE LINE 165
        if len(c.resources) == 0:
            # SOURCE LINE 166
            __M_writer(u'            <p><div class="alert alert-warning">')
            __M_writer(escape(errorMsg))
            __M_writer(u'</div></p>\n')
            # SOURCE LINE 167
        else:
            # SOURCE LINE 168
            __M_writer(u'        ')

            if numDisplay == 0:
                rList = c.paginator
            else:
                rList = c.resources
                    
            
            # SOURCE LINE 173
            __M_writer(u'\n\t\t<div class="civ-col-list">\n            ')
            # SOURCE LINE 175
            counter = 0 
            
            __M_writer(u'\n            <ul class="unstyled civ-col-list">\n')
            # SOURCE LINE 177
            for resource in rList:
                # SOURCE LINE 178
                __M_writer(u'\t\t\t')
 
                author = getUserByID(resource.owner)
                flags = getFlags(resource) 
                
                if flags:
                    numFlags = len(flags)
                else:
                    numFlags = 0
                             
                disc = getDiscussionByID(resource['discussion_id'])
                numComments = 0 
                            
                if disc:
                    numComments = disc['numComments']
                            
                
                # SOURCE LINE 192
                __M_writer(u'\n\n')
                # SOURCE LINE 194
                if resource['type'] == "post":
                    # SOURCE LINE 195
                    __M_writer(u'                ')
                    rating = int(resource['ups']) - int(resource['downs']) 
                    
                    __M_writer(u'\n                <li>\n                    <div class="row-fluid">\n                        <h3>\n                            <a href="/workshop/')
                    # SOURCE LINE 199
                    __M_writer(escape(c.w['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.w['url']))
                    __M_writer(u'/resource/')
                    __M_writer(escape(resource['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(resource['url']))
                    __M_writer(u'">')
                    __M_writer(escape(resource['title']))
                    __M_writer(u'</a>\n                        </h3>\n')
                    # SOURCE LINE 201
                    if resource['deleted'] == '0':
                        # SOURCE LINE 202
                        if len(resource['comment']) > 50:
                            # SOURCE LINE 203
                            __M_writer(u'                                ')
                            __M_writer(escape(resource['comment'][:50]))
                            __M_writer(u'... <a href="/workshop/')
                            __M_writer(escape(c.w['urlCode']))
                            __M_writer(u'/')
                            __M_writer(escape(c.w['url']))
                            __M_writer(u'/resource/')
                            __M_writer(escape(resource['urlCode']))
                            __M_writer(u'/')
                            __M_writer(escape(resource['url']))
                            __M_writer(u'">more</a>\n')
                            # SOURCE LINE 204
                        else:
                            # SOURCE LINE 205
                            __M_writer(u'                                ')
                            __M_writer(escape(resource['comment']))
                            __M_writer(u'\n')
                            pass
                        # SOURCE LINE 207
                    else:
                        # SOURCE LINE 208
                        __M_writer(u'                            Deleted\n')
                        pass
                    # SOURCE LINE 210
                    __M_writer(u'                    </div><!-- row-fluid -->\n                    <div class="row-fluid">\n                        <div class="span2">\n')
                    # SOURCE LINE 213
                    if author['pictureHash'] == 'flash':
                        # SOURCE LINE 214
                        __M_writer(u'                                <a href="/profile/')
                        __M_writer(escape(author['urlCode']))
                        __M_writer(u'/')
                        __M_writer(escape(author['url']))
                        __M_writer(u'"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="')
                        __M_writer(escape(author['name']))
                        __M_writer(u'" title="')
                        __M_writer(escape(author['name']))
                        __M_writer(u'"></a>\n')
                        # SOURCE LINE 215
                    else:
                        # SOURCE LINE 216
                        __M_writer(u'                                <a href="/profile/')
                        __M_writer(escape(author['urlCode']))
                        __M_writer(u'/')
                        __M_writer(escape(author['url']))
                        __M_writer(u'"><img src="/images/avatar/')
                        __M_writer(escape(author['directoryNumber']))
                        __M_writer(u'/profile/')
                        __M_writer(escape(author['pictureHash']))
                        __M_writer(u'.profile" class="thumbnail" style="width:30px;" alt="')
                        __M_writer(escape(author['name']))
                        __M_writer(u'" title="')
                        __M_writer(escape(author['name']))
                        __M_writer(u'"></a>\n')
                        pass
                    # SOURCE LINE 218
                    __M_writer(u'                        </div><!-- span2 -->\n                        <div class="span10">\n                             <a href="/profile/')
                    # SOURCE LINE 220
                    __M_writer(escape(author['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(author['url']))
                    __M_writer(u'">')
                    __M_writer(escape(author['name']))
                    __M_writer(u'</a><br>\n                             <span class="badge badge-info" title="Resource rating"><i class="icon-white icon-ok-sign"></i> ')
                    # SOURCE LINE 221
                    __M_writer(escape(rating))
                    __M_writer(u'</span>\n                             <span class="badge badge-info" title="Resource comments"><i class="icon-white icon-comment"></i>')
                    # SOURCE LINE 222
                    __M_writer(escape(numComments))
                    __M_writer(u'</span>\n                             <span class="badge badge-inverse"><i class="icon-white icon-flag" title="Resource flags"></i>')
                    # SOURCE LINE 223
                    __M_writer(escape(numFlags))
                    __M_writer(u'</span>\n                             <br />\n                             <i class="icon-time"></i> Added <span class="old">')
                    # SOURCE LINE 225
                    __M_writer(escape(timeSince(resource.date)))
                    __M_writer(u'</span> ago<br /> \n                             <a href="/workshop/')
                    # SOURCE LINE 226
                    __M_writer(escape(c.w['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.w['url']))
                    __M_writer(u'/resource/')
                    __M_writer(escape(resource['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(resource['url']))
                    __M_writer(u'">Rate and discuss this resource</a>\n                             <br /><br />\n                         </div><!-- span10 -->\n                    </div><!-- row-fluid -->\n                </li>\n')
                    pass
                # SOURCE LINE 232
                __M_writer(u'            ')
                counter += 1 
                
                __M_writer(u'\n')
                # SOURCE LINE 233
                if counter == numDisplay:
                    # SOURCE LINE 234
                    __M_writer(u'                ')
                    break 
                    
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 237
            __M_writer(u'            </ul>\n        </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_gravatar(context,email,size,float='none'):
    context.caller_stack._push_frame()
    try:
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 25
        __M_writer(u'\n    ')
        # SOURCE LINE 26
        from hashlib import md5
        
        __M_writer(u'\n    ')
        # SOURCE LINE 27
        gravatar = md5(email).hexdigest() 
        
        __M_writer(u'\n    <img src="http://www.gravatar.com/avatar/')
        # SOURCE LINE 28
        __M_writer(escape(gravatar))
        __M_writer(u'.jpg?s=')
        __M_writer(escape(size))
        __M_writer(u'&d=http%3A%2F%2F')
        __M_writer(escape(request.environ.get("HTTP_HOST")))
        __M_writer(u'%2Fimages%2Fpylo.jpg" style="width: ')
        __M_writer(escape(size))
        __M_writer(u'px; float: ')
        __M_writer(escape(float))
        __M_writer(u'; padding-right: 5px; vertical-align: middle;">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_avatar(context,hash,size,float='none'):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 31
        __M_writer(u'\n    ')
        # SOURCE LINE 32
        avatarURL = "/images/avatars/%s.thumbnail" %(hash) 
        
        __M_writer(u'\n    <ul class="thumbnails">\n    <li>\n        <div class="thumbnail">\n            <img src= "')
        # SOURCE LINE 36
        __M_writer(escape(avatarURL))
        __M_writer(u'" style = "width: ')
        __M_writer(escape(size))
        __M_writer(u'px; float: ')
        __M_writer(escape(float))
        __M_writer(u'; padding-right: 5px; vertical-align: middle;">\n        </div>\n    </li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_list_suggestions(context,sList,errorMsg,numDisplay,doSlider=0):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        len = context.get('len', UNDEFINED)
        endif = context.get('endif', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 260
        __M_writer(u'\n')
        # SOURCE LINE 261
        if len(sList) == 0:
            # SOURCE LINE 262
            __M_writer(u'            <p><div class="alert alert-warning">')
            __M_writer(escape(errorMsg))
            __M_writer(u'</div></p>\n')
            # SOURCE LINE 263
        else:
            # SOURCE LINE 264
            __M_writer(u'            ')

            if doSlider == 0:
                badgeSpan = "span10"
                slideSpan = "span0" 
            else:
                if numDisplay == 0:
                    badgeSpan = "span2"
                    slideSpan = "span8"
                    sliderSize="normal"
                else:
                    badgeSpan = "span4"
                    slideSpan = "span5"
                    sliderSize="small"
                        
            
            # SOURCE LINE 277
            __M_writer(u'\n\n            <div class="civ-col-list">\n            ')
            # SOURCE LINE 280
            counter = 1 
            
            __M_writer(u'\n            <ul class="unstyled civ-col-list">\n')
            # SOURCE LINE 282
            for suggestion in sList:
                # SOURCE LINE 283
                __M_writer(u'                ')
 
                author = getUserByID(suggestion.owner)
                flags = getFlags(suggestion)
                resources = getResourcesByParentID(suggestion.id)
                if flags:
                    numFlags = len(flags)
                else:
                    numFlags = 0
                disc = getDiscussionByID(suggestion['discussion_id'])
                numComments = 0
                if disc:
                    numComments = disc['numComments']
                                
                
                # SOURCE LINE 295
                __M_writer(u'\n                <li>\n                <div class="row-fluid">\n                    <h3>\n                    <a href="/workshop/')
                # SOURCE LINE 299
                __M_writer(escape(c.w['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.w['url']))
                __M_writer(u'/suggestion/')
                __M_writer(escape(suggestion['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(suggestion['url']))
                __M_writer(u'">')
                __M_writer(escape(suggestion['title']))
                __M_writer(u'</a>\n                    </h3>\n')
                # SOURCE LINE 301
                if suggestion['deleted'] == '0':
                    # SOURCE LINE 302
                    __M_writer(u'                        ')
                    __M_writer(escape(suggestion['data'][:50]))
                    __M_writer(u'... <a href="/workshop/')
                    __M_writer(escape(c.w['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.w['url']))
                    __M_writer(u'/suggestion/')
                    __M_writer(escape(suggestion['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(suggestion['url']))
                    __M_writer(u'">more</a>\n')
                    # SOURCE LINE 303
                else:
                    # SOURCE LINE 304
                    __M_writer(u'                        Deleted\n')
                    pass
                # SOURCE LINE 306
                __M_writer(u'                    <br /><br />\n                </div><!-- row-fluid -->\n                <div class="row-fluid">\n                    <div class="span2">\n')
                # SOURCE LINE 310
                if author['pictureHash'] == 'flash':
                    # SOURCE LINE 311
                    __M_writer(u'                        <a href="/profile/')
                    __M_writer(escape(author['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(author['url']))
                    __M_writer(u'"><img src="/images/avatars/flash.profile" style="width:30px;" class="thumbnail" alt="')
                    __M_writer(escape(author['name']))
                    __M_writer(u'" title="')
                    __M_writer(escape(author['name']))
                    __M_writer(u'"></a>\n')
                    # SOURCE LINE 312
                else:
                    # SOURCE LINE 313
                    __M_writer(u'                        <a href="/profile/')
                    __M_writer(escape(author['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(author['url']))
                    __M_writer(u'"><img src="/images/avatar/')
                    __M_writer(escape(author['directoryNumber']))
                    __M_writer(u'/profile/')
                    __M_writer(escape(author['pictureHash']))
                    __M_writer(u'.profile" class="thumbnail" style="width:30px;" alt="')
                    __M_writer(escape(author['name']))
                    __M_writer(u'" title="')
                    __M_writer(escape(author['name']))
                    __M_writer(u'"></a>\n')
                    pass
                # SOURCE LINE 315
                __M_writer(u'                    </div><!-- span2 -->\n                    <div class="')
                # SOURCE LINE 316
                __M_writer(escape(badgeSpan))
                __M_writer(u'">\n                    <a href="/profile/')
                # SOURCE LINE 317
                __M_writer(escape(author['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(author['url']))
                __M_writer(u'">')
                __M_writer(escape(author['name']))
                __M_writer(u'</a><br />\n                    <span class="badge badge-info" title="Suggestion information resources"><i class="icon-white icon-book"></i>')
                # SOURCE LINE 318
                __M_writer(escape(len(resources)))
                __M_writer(u'</span>\n                    <span class="badge badge-info" title="Suggestion comments"><i class="icon-white icon-comment"></i>')
                # SOURCE LINE 319
                __M_writer(escape(numComments))
                __M_writer(u'</span>\n                    <span class="badge badge-inverse" title="Suggestion flags"><i class="icon-white icon-flag"></i>')
                # SOURCE LINE 320
                __M_writer(escape(numFlags))
                __M_writer(u'</span>\n                    </div><!-- ')
                # SOURCE LINE 321
                __M_writer(escape(badgeSpan))
                __M_writer(u' -->\n')
                # SOURCE LINE 322
                if 'user' in session and c.isScoped and doSlider == 1 and suggestion['disabled'] == '0' and suggestion['deleted'] == '0':
                    # SOURCE LINE 323
                    __M_writer(u'                    <div class="')
                    __M_writer(escape(slideSpan))
                    __M_writer(u'">\n                        <div id="ratings')
                    # SOURCE LINE 324
                    __M_writer(escape(counter))
                    __M_writer(u'" class="rating wide pull-right">\n                            <div id="overall_slider" class="ui-slider-container">\n')
                    # SOURCE LINE 326
                    if suggestion.rating:
                        # SOURCE LINE 327
                        __M_writer(u'                                    <div id="')
                        __M_writer(escape(suggestion['urlCode']))
                        __M_writer(u'_')
                        __M_writer(escape(suggestion['url']))
                        __M_writer(u'" class="')
                        __M_writer(escape(sliderSize))
                        __M_writer(u'_slider" data1="0_')
                        __M_writer(escape(suggestion['urlCode']))
                        __M_writer(u'_')
                        __M_writer(escape(suggestion.rating['rating']))
                        __M_writer(u'_overall_true_rateSuggestion" data2="')
                        __M_writer(escape(suggestion['url']))
                        __M_writer(u'"></div>\n')
                        # SOURCE LINE 328
                    else:
                        # SOURCE LINE 329
                        __M_writer(u'                                    <div id="')
                        __M_writer(escape(suggestion['urlCode']))
                        __M_writer(u'_')
                        __M_writer(escape(suggestion['url']))
                        __M_writer(u'" class="')
                        __M_writer(escape(sliderSize))
                        __M_writer(u'_slider" data1="0_')
                        __M_writer(escape(suggestion['urlCode']))
                        __M_writer(u'_0_overall_false_rateSuggestion" data2="')
                        __M_writer(escape(suggestion['url']))
                        __M_writer(u'"></div>\n')
                        pass
                    # SOURCE LINE 331
                    __M_writer(u'                             </div> <!-- /#overall_slider -->\n                         </div> <!-- /#ratings')
                    # SOURCE LINE 332
                    __M_writer(escape(counter))
                    __M_writer(u' -->\n                    </div><!-- ')
                    # SOURCE LINE 333
                    __M_writer(escape(slideSpan))
                    __M_writer(u' -->\n')
                    # SOURCE LINE 334
                else:
                    # SOURCE LINE 335
                    if 'user' not in session and doSlider == 1 and suggestion['disabled'] == '0' and suggestion['deleted'] == '0':
                        # SOURCE LINE 336
                        __M_writer(u'                        <div class="')
                        __M_writer(escape(slideSpan))
                        __M_writer(u'">\n                            <div id="ratings')
                        # SOURCE LINE 337
                        __M_writer(escape(counter))
                        __M_writer(u'" class="rating wide pull-right">\n                                <div id="overall_slider" class="ui-slider-container">\n                                    <div id="')
                        # SOURCE LINE 339
                        __M_writer(escape(suggestion['urlCode']))
                        __M_writer(u'_')
                        __M_writer(escape(suggestion['url']))
                        __M_writer(u'" class="')
                        __M_writer(escape(sliderSize))
                        __M_writer(u'_slider"  data2="')
                        __M_writer(escape(suggestion['url']))
                        __M_writer(u'"></div>\n                                 </div> <!-- /#overall_slider -->\n                             </div> <!-- /#ratings')
                        # SOURCE LINE 341
                        __M_writer(escape(counter))
                        __M_writer(u' -->\n                        </div><!-- ')
                        # SOURCE LINE 342
                        __M_writer(escape(slideSpan))
                        __M_writer(u' -->\n')
                        pass
                    pass
                # SOURCE LINE 345
                __M_writer(u'                </div><!-- row-fluid -->\n                <div class="row-fluid">\n                    <i class="icon-time"></i> Added <span class="old">')
                # SOURCE LINE 347
                __M_writer(escape(timeSince(suggestion.date)))
                __M_writer(u'</span> ago \n')
                # SOURCE LINE 348
                if 'user' in session and c.isScoped and doSlider == '1':
                    # SOURCE LINE 349
                    __M_writer(u'                        | <a href="/workshop/')
                    __M_writer(escape(c.w['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.w['url']))
                    __M_writer(u'/suggestion/')
                    __M_writer(escape(suggestion['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(suggestion['url']))
                    __M_writer(u'">Leave comment</a>\n')
                    pass
                # SOURCE LINE 351
                __M_writer(u'                    <br /><br />\n                </div><!-- row-fluid -->\n                </li>\n                ')
                # SOURCE LINE 354
 
                counter += 1
                if counter == int(numDisplay):
                    break
                endif
                                
                
                # SOURCE LINE 359
                __M_writer(u'\n')
                pass
            # SOURCE LINE 361
            __M_writer(u'            </ul>\n')
            # SOURCE LINE 362
            if c.paginator and (len(c.paginator) != len(c.suggestions)):
                # SOURCE LINE 363
                __M_writer(u'                ')
                state = True 
                
                __M_writer(u'\n')
                # SOURCE LINE 364
                for p in c.paginator:
                    # SOURCE LINE 365
                    __M_writer(u'                    ')
                    state = not state 
                    
                    __M_writer(u'\n')
                    pass
                # SOURCE LINE 367
                __M_writer(u'                <p>Total Suggestions: ')
                __M_writer(escape(c.count))
                __M_writer(u' | View ')
                __M_writer(escape( c.paginator.pager('~3~') ))
                __M_writer(u'</p>\n')
                pass
            # SOURCE LINE 369
            __M_writer(u'            </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_totalResources(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 242
        __M_writer(u'\n        ')
        # SOURCE LINE 243
 
        if c.resources:
            total = len(c.resources)
        else:
            total = 0 
                
        
        # SOURCE LINE 248
        __M_writer(u'\n        <br />\n        <p class="total">\n                ')
        # SOURCE LINE 251
        __M_writer(escape(total))
        __M_writer(u'<br>\n                <span>Resources</span><br />\n')
        # SOURCE LINE 253
        if len(c.resources) > 15:
            # SOURCE LINE 254
            __M_writer(u'                    <span>Display Page ')
            __M_writer(escape( c.paginator.pager('~3~')))
            __M_writer(u'</span><br />\n')
            pass
        # SOURCE LINE 256
        __M_writer(u'                <span><a href="/workshop/')
        __M_writer(escape(c.w['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.w['url']))
        __M_writer(u'">Back to Workshop</a></span>\n        </p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


