# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398543921.2985251
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_profile_photos.bootstrap'
_template_uri = '/derived/6_profile_photos.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts2', 'extraScripts', 'extraStyles', 'extraScripts2']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 6
    ns = runtime.TemplateNamespace(u'photos', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_photos.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'photos')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'helpers')] = ns

    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'dashboard', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_profile_dashboard.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'dashboard')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        photos = _mako_get_namespace(context, 'photos')
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        dashboard = _mako_get_namespace(context, 'dashboard')
        lib = _mako_get_namespace(context, 'lib')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\r\n')
        # SOURCE LINE 2
        __M_writer(u'\r\n')
        # SOURCE LINE 3
        __M_writer(u'\r\n')
        # SOURCE LINE 4
        __M_writer(u'\r\n')
        # SOURCE LINE 5
        __M_writer(u'\r\n')
        # SOURCE LINE 6
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 8

        lib.return_to()
        import pylowiki.lib.db.photo            as photoLib
        import pylowiki.lib.db.discussion       as discussionLib
        import pylowiki.lib.db.event            as eventLib
        import pylowiki.lib.db.user             as userLib
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['discussionLib','photoLib','eventLib','userLib'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 14
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 16
 
        if c.user['memberType'] == 'organization':
            who = "Our"
        else:
            who = "My"
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['who'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 21
        __M_writer(u'\r\n\r\n<div class="spacer"></div>\r\n<div class="row-fluid" ng-controller="ProfileEditController" ng-init="fullName = \'')
        # SOURCE LINE 24
        __M_writer(escape(c.user['name']))
        __M_writer(u'\'; ">\r\n')
        # SOURCE LINE 26
        __M_writer(u'    <div class="span8">\r\n        <div class="tabbable">\r\n            <ul class="nav nav-tabs" id="editTabs">\r\n            <li class="active"><a href="#tab-edit" data-toggle="tab" class="green green-hover">')
        # SOURCE LINE 29
        __M_writer(escape(who))
        __M_writer(u' Pictures</a></li>\r\n            <li class="pull-right"><a href="/profile/')
        # SOURCE LINE 30
        __M_writer(escape(c.user['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.user['url']))
        __M_writer(u'">Back to Profile</a></li>\r\n            </ul>\r\n            <div class="tab-content">\r\n                <div class="tab-pane active" id="tab-photos">\r\n                    ')
        # SOURCE LINE 34
        __M_writer(escape(photos.uploadPhoto()))
        __M_writer(u'\r\n')
        # SOURCE LINE 35
        for photo in c.photos:
            # SOURCE LINE 36
            __M_writer(u'                        ')
 
            pdiscussion = discussionLib.getDiscussionForThing(photo)
            numComments = pdiscussion['numComments']
                                    
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['pdiscussion','numComments'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 39
            __M_writer(u'\r\n                        \r\n')
            # SOURCE LINE 41
            if photo['disabled'] == '0' and photo['deleted'] == '0':
                # SOURCE LINE 42
                __M_writer(u'                            <div class="row-fluid">\r\n                                <div class="span1">\r\n                                    ')
                # SOURCE LINE 44
                __M_writer(escape(lib_6.upDownVote(photo)))
                __M_writer(u'\r\n                                </div><!-- span1 -->\r\n                                <div class="span3">\r\n                                    ')
                # SOURCE LINE 47
                imgSrc = "/images/photos/" + photo['directoryNum_photos'] + "/thumbnail/" + photo['pictureHash_photos'] + ".png" 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['imgSrc'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\r\n                                    <img src="')
                # SOURCE LINE 48
                __M_writer(escape(imgSrc))
                __M_writer(u'" class="wrap-photo">\r\n                                </div><!-- span3 -->\r\n                                <div class="span8">\r\n                                    <a href="/profile/')
                # SOURCE LINE 51
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/photo/show/')
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">')
                __M_writer(escape(photo['title']))
                __M_writer(u'</a><br />\r\n                                    ')
                # SOURCE LINE 52
                tags = photo['tags'].split('|') 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['tags'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\r\n                                    Tags: \r\n')
                # SOURCE LINE 54
                for tag in tags:
                    # SOURCE LINE 55
                    if tag != '':
                        # SOURCE LINE 56
                        __M_writer(u'                                            <span class="label workshop-tag ')
                        __M_writer(escape(tag))
                        __M_writer(u'">')
                        __M_writer(escape(tag))
                        __M_writer(u'</span>\r\n')
                        pass
                    pass
                # SOURCE LINE 59
                __M_writer(u'                                    <br />\r\n                                    Added: ')
                # SOURCE LINE 60
                __M_writer(escape(photo.date))
                __M_writer(u'\r\n                                    <br />\r\n                                    Photo Location: ')
                # SOURCE LINE 62
                __M_writer(escape(photoLib.getPhotoLocation(photo)))
                __M_writer(u'<br />\r\n                                    <a href="/profile/')
                # SOURCE LINE 63
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/photo/show/')
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">View or Add Comments (')
                __M_writer(escape(numComments))
                __M_writer(u')</a>\r\n                                </div><!-- span8 -->\r\n                            </div><!-- row-fluid -->\r\n')
                # SOURCE LINE 66
            elif photo['disabled'] == '1' and photo['deleted'] == '0':
                # SOURCE LINE 67
                __M_writer(u'                            <div class="accordion" id="item-')
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">\r\n                                <div class="accordion-group no-border">\r\n                                    <div class="accordion-heading disabled">\r\n                                        <div class="collapsed-item-header">\r\n                                            <button class="accordion-toggle inline btn btn-mini collapsed" data-toggle="collapse" data-parent="#item-')
                # SOURCE LINE 71
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'" href="#item-body-')
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">Show</button>\r\n                                            ')
                # SOURCE LINE 72

                event = eventLib.getEventsWithAction(photo, 'disabled')[0]
                disabler = userLib.getUserByID(event.owner)
                reason = event['reason']
                                                            
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['reason','event','disabler'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 76
                __M_writer(u'\r\n                                            <small>This item has been disabled by ')
                # SOURCE LINE 77
                __M_writer(escape(lib_6.userLink(disabler)))
                __M_writer(u' because: ')
                __M_writer(escape(reason))
                __M_writer(u'</small>\r\n                                        </div><!-- collapsed-item-header -->\r\n                                        <div class="accordion-body collapse" id="item-body-')
                # SOURCE LINE 79
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">\r\n                                            <div class="row-fluid list-item">\r\n                                                <div class="span1">\r\n                                                    ')
                # SOURCE LINE 82
                __M_writer(escape(lib_6.upDownVote(photo)))
                __M_writer(u'\r\n                                                </div><!-- span1 -->\r\n                                                <div class="span3">\r\n                                                    ')
                # SOURCE LINE 85
                imgSrc = "/images/photos/" + photo['directoryNum_photos'] + "/thumbnail/" + photo['pictureHash_photos'] + ".png" 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['imgSrc'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\r\n                                                    <img src="')
                # SOURCE LINE 86
                __M_writer(escape(imgSrc))
                __M_writer(u'" class="wrap-photo">\r\n                                                    <div class="spacer"></div>\r\n                                                </div><!-- span3 -->\r\n                                                <div class="span8">\r\n                                                    <a href="/profile/')
                # SOURCE LINE 90
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/photo/show/')
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">')
                __M_writer(escape(photo['title']))
                __M_writer(u'</a><br />\r\n                                                    Tags: {{photo.tags}}\r\n                                                    <br />\r\n                                                    Added: ')
                # SOURCE LINE 93
                __M_writer(escape(photo.date))
                __M_writer(u'\r\n                                                    <br />\r\n                                                    Photo Location: ')
                # SOURCE LINE 95
                __M_writer(escape(photoLib.getPhotoLocation(photo)))
                __M_writer(u'<br />\r\n                                                    <a href="/profile/')
                # SOURCE LINE 96
                __M_writer(escape(c.user['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.user['url']))
                __M_writer(u'/photo/show/')
                __M_writer(escape(photo['urlCode']))
                __M_writer(u'">View or Add Comments (')
                __M_writer(escape(numComments))
                __M_writer(u')</a>\r\n                                                </div><!-- span8 -->\r\n                                            </div><!-- row-fluid -->\r\n                                        </div><!-- accordian-body-collapse -->\r\n                                    </div><!-- accordian-heading -->\r\n                                </div><!-- accordian-group -->\r\n                            </div><!-- accordian -->\r\n')
                pass
            # SOURCE LINE 104
            __M_writer(u'                        <div class="spacer"></div>\r\n')
            pass
        # SOURCE LINE 106
        __M_writer(u'                </div><!-- tab-photos -->\r\n            </div><!-- tab-content -->\r\n        </div><!-- tabbable -->\r\n    </div><!-- span8 -->\r\n    <div class="span4">\r\n        ')
        # SOURCE LINE 111
        __M_writer(escape(dashboard.profileDashboard()))
        __M_writer(u'\r\n    </div><!--/.span4-->\r\n</div>\r\n\r\n')
        # SOURCE LINE 118
        __M_writer(u'\r\n            \r\n')
        # SOURCE LINE 152
        __M_writer(u'\r\n\r\n')
        # SOURCE LINE 157
        __M_writer(u'\r\n\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts2(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 115
        __M_writer(u'\r\n    <script src="/js/bootstrap/bootstrap-collapse.js"></script>\r\n    <script src="/js/geo.js" type="text/javascript"></script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 120
        __M_writer(u'\r\n    <script type="text/javascript">\r\n        $(\'.hoverTip\').tooltip();\r\n    </script>\r\n    <script src="')
        # SOURCE LINE 124
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/profile_edit.js')))
        __M_writer(u'" type="text/javascript"></script>\r\n    <script src="/js/vendor/jquery.expander.min.js" type="text/javascript"></script>\r\n    <script type="text/javascript">\r\n        $(document).ready(function() {\r\n            $(\'.expandable\').expander({\r\n                slicePoint: 35,\r\n                widow: 2,\r\n                expandText: \' ...->\',\r\n                expandPrefix: \'\',\r\n                userCollapseText: \' <-\',\r\n                userCollapsePrefix: \'\'\r\n            });\r\n        });\r\n    </script>\r\n')
        # SOURCE LINE 138
        if 'user' in session:
            # SOURCE LINE 139
            __M_writer(u'        <script src="')
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.ui.widget.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 140
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/load-image.min.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 141
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/canvas-to-blob.min.js')))
            __M_writer(u'"></script>\r\n')
            # SOURCE LINE 143
            __M_writer(u'        <script src="')
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.iframe-transport.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 144
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 145
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-process.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 146
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-resize.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 147
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-validate.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 148
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/jquery.fileupload-angular.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 149
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/blueimp/app.js')))
            __M_writer(u'"></script>\r\n        <script src="')
            # SOURCE LINE 150
            __M_writer(escape(lib_6.fingerprintFile('/js/vendor/jquery.Jcrop.js')))
            __M_writer(u'"></script>\r\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraStyles(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 154
        __M_writer(u'\r\n    <link rel="stylesheet" href="/styles/vendor/jquery.Jcrop.css">\r\n    <link rel="stylesheet" href="/styles/vendor/blueimp.css">\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 159
        __M_writer(u'\r\n    <script src="')
        # SOURCE LINE 160
        __M_writer(escape(lib_6.fingerprintFile('/js/upDown.js')))
        __M_writer(u'" type="text/javascript"></script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


