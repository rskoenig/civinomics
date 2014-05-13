# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398492171.5535109
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/derived/6_main_listing.mako'
_template_uri = u'/lib/derived/6_main_listing.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['showActivity', 'show_workshop']


# SOURCE LINE 1
 
from pylowiki.lib.db.user import getUserByID
import pylowiki.lib.db.workshop      as workshopLib
import pylowiki.lib.db.initiative    as initiativeLib
import pylowiki.lib.db.follow        as followLib
import pylowiki.lib.db.activity      as activityLib
import pylowiki.lib.db.goal          as goalLib
import pylowiki.lib.db.mainImage     as mainImageLib


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 10
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 9
        __M_writer(u'\n')
        # SOURCE LINE 10
        __M_writer(u'\n\n')
        # SOURCE LINE 85
        __M_writer(u'\n\n')
        # SOURCE LINE 105
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_showActivity(context,item,**kwargs):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 87
        __M_writer(u'\n   <div class="media">\n      ')
        # SOURCE LINE 89

        if 'workshopCode' in item:
            parent = workshopLib.getWorkshopByCode(item['workshopCode'])
        elif 'initiativeCode' in item:
            parent = initiativeLib.getInitiative(item['initiativeCode'])
        else:
            parent = item
        
        thisUser = getUserByID(item.owner)
              
        
        # SOURCE LINE 98
        __M_writer(u'\n      <div class="pull-left"> ')
        # SOURCE LINE 99
        __M_writer(escape(lib_6.userImage(thisUser, className = 'avatar', linkClass = 'media-object')))
        __M_writer(u'</div> \n      <div class="media-body">\n         ')
        # SOURCE LINE 101
        __M_writer(escape(lib_6.userLink(thisUser, className = 'green green-hover', maxChars = 25)))
        __M_writer(u' \n         ')
        # SOURCE LINE 102
        __M_writer(escape(lib_6.showItemInActivity(item, parent, **kwargs)))
        __M_writer(u'\n      </div>\n   </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_show_workshop(context,w):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        str = context.get('str', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n   ')
        # SOURCE LINE 13
 
        goals = goalLib.getGoalsForWorkshop(w) 
        mainImage = mainImageLib.getMainImage(w)
           
        
        # SOURCE LINE 16
        __M_writer(u'\n   <div class="viewport">\n      <a ')
        # SOURCE LINE 18
        __M_writer(escape(lib_6.workshopLink(w)))
        __M_writer(u'>\n         <span class="dark-background">\n')
        # SOURCE LINE 20
        if not goals:
            # SOURCE LINE 21
            __M_writer(u'               This workshop has no goals!\n')
            # SOURCE LINE 22
        else:
            # SOURCE LINE 23
            __M_writer(u'               <div class="goals-preview">\n                  Goals:\n                  <br>\n                  <ul>\n                  ')
            # SOURCE LINE 27
            count = 0 
            
            __M_writer(u'\n')
            # SOURCE LINE 28
            for goal in goals:
                # SOURCE LINE 29
                if count <= 2:
                    # SOURCE LINE 30
                    if goal['status'] == u'100':
                        # SOURCE LINE 31
                        __M_writer(u'                           <li class="done-true">')
                        __M_writer(escape(goal['title']))
                        __M_writer(u'</li>\n')
                        # SOURCE LINE 32
                    else:
                        # SOURCE LINE 33
                        __M_writer(u'                           <li>')
                        __M_writer(escape(goal['title']))
                        __M_writer(u'</li>\n')
                        pass
                    # SOURCE LINE 35
                    __M_writer(u'                        ')
                    count += 1
                    
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 38
            __M_writer(u'                  </ul>\n')
            # SOURCE LINE 39
            if len(goals) > 3:
                # SOURCE LINE 40
                __M_writer(u'                     ')
                moreGoals = len(goals) - 3 
                
                __M_writer(u'\n                     <p class="centered more">')
                # SOURCE LINE 41
                __M_writer(escape(moreGoals))
                __M_writer(u' more</p>\n')
                pass
            # SOURCE LINE 43
            __M_writer(u'               </div>\n')
            pass
        # SOURCE LINE 45
        __M_writer(u'         </span>\n         ')
        # SOURCE LINE 46
 
        if mainImage['pictureHash'] == 'supDawg':
           imgSrc="/images/slide/thumbnail/supDawg.thumbnail"
        elif 'format' in mainImage.keys():
            imgSrc="/images/mainImage/%s/listing/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
        else:
           imgSrc="/images/mainImage/%s/listing/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
                 
        
        # SOURCE LINE 53
        __M_writer(u'\n         <div style="background-image:url(\'')
        # SOURCE LINE 54
        __M_writer(escape(imgSrc))
        __M_writer(u'\');"></div>\n      </a>\n   </div>\n   <div class="span workshop-listingTitle">\n      <strong><a ')
        # SOURCE LINE 58
        __M_writer(escape(lib_6.workshopLink(w)))
        __M_writer(u'> ')
        __M_writer(escape(lib_6.ellipsisIZE(w['title'], 60)))
        __M_writer(u' </a></strong>\n   </div>\n   <div class="workshop-listing-info">\n      ')
        # SOURCE LINE 61

        if 'numBookmarks' in w:
            numBookmarks = w['numBookmarks']
        else:
            numBookmarks = len(followLib.getWorkshopFollowers(w))
            
        if 'numPosts' in w:
            numPosts = w['numPosts']
        else:
            numPosts = len(activityLib.getActivityForWorkshop(w['urlCode']))
              
        
        # SOURCE LINE 71
        __M_writer(u'\n      <span class="workshop-listing-info-icons"> \n         <img class="small-bookmark" data-toggle="tooltip" title="Members who have bookmarked this workshop" src="/images/glyphicons_pro/glyphicons/png/glyphicons_072_bookmark.png">\n         <a ')
        # SOURCE LINE 74
        __M_writer(escape(lib_6.workshopLink(w)))
        __M_writer(u'> <!-- Num watchers -->\n            <strong>')
        # SOURCE LINE 75
        __M_writer(escape(str(numBookmarks)))
        __M_writer(u'</strong>\n         </a><span>BOOKMARKS</span> <!-- /Num watchers -->\n      </span>\n      <span class="workshop-listing-info-icons"> \n         <img class="small-bulb" data-toggle="tooltip" title="Ideas, conversations, resources, comments" src="/images/glyphicons_pro/glyphicons/png/glyphicons_150_edit.png">\n         <a ')
        # SOURCE LINE 80
        __M_writer(escape(lib_6.workshopLink(w)))
        __M_writer(u'> <!-- Num inputs -->\n            <strong>')
        # SOURCE LINE 81
        __M_writer(escape(str(numPosts)))
        __M_writer(u'</strong>\n         </a><span>POSTS</span> <!-- /Num inputs -->\n      </span>\n   </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


