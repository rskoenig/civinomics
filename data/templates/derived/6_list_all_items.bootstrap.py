# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544364.2723019
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_list_all_items.bootstrap'
_template_uri = '/derived/6_list_all_items.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['extraScripts']


# SOURCE LINE 3
 
import pylowiki.lib.db.workshop     as workshopLib 
import pylowiki.lib.db.user         as userLib


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 8
 
        itemType = None
        if len(c.list) > 0:
            itemType = c.list[0].objType
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['itemType'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 12
        __M_writer(u'\n\n<div class="row-fluid">\n    <div class="span2">\n        <ul class="nav nav-list">\n            <li class="nav-header">Item Type</li>\n')
        # SOURCE LINE 18
        if itemType == 'user':
            # SOURCE LINE 19
            __M_writer(u'                <li class="active"><a href="/admin/users">Users</a></li>\n')
            # SOURCE LINE 20
        else:
            # SOURCE LINE 21
            __M_writer(u'                <li><a href="/admin/users">Users</a></li>\n')
            pass
        # SOURCE LINE 23
        __M_writer(u'            \n')
        # SOURCE LINE 24
        if itemType == 'workshop':
            # SOURCE LINE 25
            __M_writer(u'                <li class="active"><a href="/admin/workshops">Workshops</a></li>\n')
            # SOURCE LINE 26
        else:
            # SOURCE LINE 27
            __M_writer(u'                <li><a href="/admin/workshops">Workshops</a></li>\n')
            pass
        # SOURCE LINE 29
        __M_writer(u'            \n')
        # SOURCE LINE 30
        if itemType == 'idea':
            # SOURCE LINE 31
            __M_writer(u'                <li class="active"><a href="/admin/ideas">Ideas</a></li>\n')
            # SOURCE LINE 32
        else:
            # SOURCE LINE 33
            __M_writer(u'                <li><a href="/admin/ideas">Ideas</a></li>\n')
            pass
        # SOURCE LINE 35
        __M_writer(u'            \n')
        # SOURCE LINE 36
        if itemType == 'resource':
            # SOURCE LINE 37
            __M_writer(u'                <li class="active"><a href="/admin/resources">Resources</a></li>\n')
            # SOURCE LINE 38
        else:
            # SOURCE LINE 39
            __M_writer(u'                <li><a href="/admin/resources">Resources</a></li>\n')
            pass
        # SOURCE LINE 41
        __M_writer(u'            \n')
        # SOURCE LINE 42
        if itemType == 'discussion':
            # SOURCE LINE 43
            __M_writer(u'                <li class="active"><a href="/admin/discussions">Discussions</a></li>\n')
            # SOURCE LINE 44
        else:
            # SOURCE LINE 45
            __M_writer(u'                <li><a href="/admin/discussions">Discussions</a></li>\n')
            pass
        # SOURCE LINE 47
        __M_writer(u'            \n')
        # SOURCE LINE 48
        if itemType == 'comment':
            # SOURCE LINE 49
            __M_writer(u'                <li class="active"><a href="/admin/comments">Comments</a></li>\n')
            # SOURCE LINE 50
        else:
            # SOURCE LINE 51
            __M_writer(u'                <li><a href="/admin/comments">Comments</a></li>\n')
            pass
        # SOURCE LINE 53
        __M_writer(u'            \n')
        # SOURCE LINE 54
        if itemType == 'photo':
            # SOURCE LINE 55
            __M_writer(u'                <li class="active"><a href="/admin/photos">Photos</a></li>\n')
            # SOURCE LINE 56
        else:
            # SOURCE LINE 57
            __M_writer(u'                <li><a href="/admin/photos">Photos</a></li>\n')
            pass
        # SOURCE LINE 59
        __M_writer(u'            \n')
        # SOURCE LINE 60
        if itemType == 'flaggedphoto':
            # SOURCE LINE 61
            __M_writer(u'                <li class="active"><a href="/admin/flaggedPhotos">Flagged Photos</a></li>\n')
            # SOURCE LINE 62
        else:
            # SOURCE LINE 63
            __M_writer(u'                <li><a href="/admin/flaggedPhotos">Flagged Photos</a></li>\n')
            pass
        # SOURCE LINE 65
        __M_writer(u'            \n')
        # SOURCE LINE 66
        if itemType == 'initiative':
            # SOURCE LINE 67
            __M_writer(u'                <li class="active"><a href="/admin/initiatives">Initiatives</a></li>\n')
            # SOURCE LINE 68
        else:
            # SOURCE LINE 69
            __M_writer(u'                <li><a href="/admin/initiatives">Initiatives</a></li>\n')
            pass
        # SOURCE LINE 71
        __M_writer(u'            \n')
        # SOURCE LINE 72
        if itemType == 'flaggedinitiative':
            # SOURCE LINE 73
            __M_writer(u'                <li class="active"><a href="/admin/flaggedInitiatives">Flagged Initiatives</a></li>\n')
            # SOURCE LINE 74
        else:
            # SOURCE LINE 75
            __M_writer(u'                <li><a href="/admin/flaggedInitiatives">Flagged Initiatives</a></li>\n')
            pass
        # SOURCE LINE 77
        __M_writer(u'        </ul>\n    </div><!--/.span3-->\n\n    <div class="span10">\n        <table class="table table-striped">\n            <thead>\n                <tr>\n                    <th>id</th>\n                    <th>owner</th>\n                    <th>date</th>\n                    <th>link</th>\n                    <th>status</th>\n                </tr>\n            </thead>\n            <tbody>\n')
        # SOURCE LINE 92
        for item in c.list:
            # SOURCE LINE 93
            __M_writer(u'                    <tr>\n                        <td>')
            # SOURCE LINE 94
            __M_writer(escape(item.id))
            __M_writer(u'</td>\n')
            # SOURCE LINE 95
            if item.owner != 0:
                # SOURCE LINE 96
                __M_writer(u'                            ')
                owner = userLib.getUserByID(item.owner) 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['owner'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\n                            <td>')
                # SOURCE LINE 97
                __M_writer(escape(lib_6.userImage(owner, className = 'avatar small-avatar')))
                __M_writer(u' ')
                __M_writer(escape(lib_6.userLink(owner)))
                __M_writer(u' (')
                __M_writer(escape(owner.id))
                __M_writer(u')</td>\n')
                # SOURCE LINE 98
            else:
                # SOURCE LINE 99
                __M_writer(u'                            <td>None</td>\n')
                pass
            # SOURCE LINE 101
            __M_writer(u'                        <td>')
            __M_writer(escape(item.date))
            __M_writer(u'</td>\n                        ')
            # SOURCE LINE 102
            activated = "" 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['activated'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            # SOURCE LINE 103
            if itemType == 'user':
                # SOURCE LINE 104
                __M_writer(u'                            <td>')
                __M_writer(escape(lib_6.userImage(item, className = 'avatar small-avatar')))
                __M_writer(u' ')
                __M_writer(escape(lib_6.userLink(item)))
                __M_writer(u'</td>\n')
                # SOURCE LINE 105
            elif itemType == 'workshop':
                # SOURCE LINE 106
                __M_writer(u'                            <td>')
                __M_writer(escape(lib_6.workshopImage(item)))
                __M_writer(u' <a ')
                __M_writer(escape(lib_6.workshopLink(item)))
                __M_writer(u' class="expandable">')
                __M_writer(escape(item['title']))
                __M_writer(u'</a></td>\n')
                # SOURCE LINE 107
            elif itemType in ['idea', 'discussion', 'resource'] and 'workshopCode' in item:
                # SOURCE LINE 108
                __M_writer(u'                            ')
                workshop = workshopLib.getWorkshopByCode(item['workshopCode']) 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['workshop'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\n                            <td><a ')
                # SOURCE LINE 109
                __M_writer(escape(lib_6.thingLinkRouter(item, workshop)))
                __M_writer(u' class="expandable">')
                __M_writer(escape(item['title']))
                __M_writer(u'</a></td>\n')
                # SOURCE LINE 110
            elif itemType == 'comment' and 'workshopCode' in item:
                # SOURCE LINE 111
                __M_writer(u'                            ')
                workshop = workshopLib.getWorkshopByCode(item['workshopCode']) 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['workshop'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\n                            <td><a ')
                # SOURCE LINE 112
                __M_writer(escape(lib_6.thingLinkRouter(item, workshop, id='accordion-%s'%item['urlCode'])))
                __M_writer(u' class="expandable">')
                __M_writer(escape(item['data']))
                __M_writer(u'</a></td>\n')
                # SOURCE LINE 113
            elif itemType == 'photo':
                # SOURCE LINE 114
                __M_writer(u'                            ')
                imgSrc = "/images/photos/" + item['directoryNum_photos'] + "/thumbnail/" + item['pictureHash_photos'] + ".png" 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['imgSrc'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\n                            <td><a href="/profile/')
                # SOURCE LINE 115
                __M_writer(escape(owner['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(owner['url']))
                __M_writer(u'/photo/show/')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'"><img src="')
                __M_writer(escape(imgSrc))
                __M_writer(u'">')
                __M_writer(escape(item['title']))
                __M_writer(u'</a></td>\n')
                # SOURCE LINE 116
            elif itemType == 'initiative':
                # SOURCE LINE 117
                __M_writer(u'                            ')
 
                if 'directoryNum_photos' in item:
                    imgSrc = "/images/photos/" + item['directoryNum_photos'] + "/thumbnail/" + item['pictureHash_photos'] + ".png"
                else:
                    imgSrc = "/images/slide/thumbnail/supDawg.thumbnail"
                                            
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['imgSrc'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 122
                __M_writer(u'\n                            <td><a href="/initiative/')
                # SOURCE LINE 123
                __M_writer(escape(item['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(item['url']))
                __M_writer(u'/show"><img src="')
                __M_writer(escape(imgSrc))
                __M_writer(u'">')
                __M_writer(escape(item['title']))
                __M_writer(u'</a></td>\n')
                pass
            # SOURCE LINE 125
            __M_writer(u'                        <td>                             \n')
            # SOURCE LINE 126
            if 'activated' in item and item['activated'] == "1":
                # SOURCE LINE 127
                __M_writer(u'                            Activated\n')
                # SOURCE LINE 128
            elif 'activated' in item and item['activated'] == "0":
                # SOURCE LINE 129
                __M_writer(u'                            <button class="btn btn-civ activateButton notactivated" data-URL-list="user_')
                __M_writer(escape(item['urlCode']))
                __M_writer(u'_')
                __M_writer(escape(item['url']))
                __M_writer(u'" rel="tooltip" data-placement="bottom" data-original-title="Activate this user" id="userActivate"> \n                            <span><i class="icon-user btn-height icon-light"></i><strong> Activate </strong></span>\n                            </button>\n')
                pass
            # SOURCE LINE 133
            if 'disabled' in item:
                # SOURCE LINE 134
                __M_writer(u'                            Disabled: ')
                __M_writer(escape(item['disabled']))
                __M_writer(u' \n')
                # SOURCE LINE 135
            elif 'deleted' in item:
                # SOURCE LINE 136
                __M_writer(u'                            Deleted: ')
                __M_writer(escape(item['deleted']))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 138
            __M_writer(u'                        </td>\n                    </tr>\n')
            pass
        # SOURCE LINE 141
        __M_writer(u'            </tbody>\n        </table>\n    </div><!--/.span9-->\n</div> <!--/.row-fluid-->\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 146
        __M_writer(u'\n    <script src="')
        # SOURCE LINE 147
        __M_writer(escape(lib_6.fingerprintFile('/js/activate.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="/js/vendor/jquery.tablesorter.min.js" type="text/javascript"></script>\n    <script src="/js/vendor/jquery.expander.min.js" type="text/javascript"></script>\n    <script type="text/javascript">\n        $(document).ready(function() {\n            $(\'.expandable\').expander({\n                slicePoint: 95,\n                widow: 2,\n                expandText: \' ...->\',\n                expandPrefix: \'\',\n                userCollapseText: \' <-\',\n                userCollapsePrefix: \'\'\n            });\n            $(".table").tablesorter(); \n        });\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


