# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398544378.0007541
_template_filename = u'/home/maria/civinomics/pylowiki/templates/base/base_initiative.bootstrap'
_template_uri = u'/base/base_initiative.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 5
    ns = runtime.TemplateNamespace('__anon_0x3079550', context._clean_inheritance_tokens(), templateuri=u'/lib/6_comments.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x3079550')] = ns

    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'ihelpers', context._clean_inheritance_tokens(), templateuri=u'/lib/derived/6_initiative_home.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ihelpers')] = ns

    # SOURCE LINE 6
    ns = runtime.TemplateNamespace(u'lib', context._clean_inheritance_tokens(), templateuri=u'/lib/mako_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base_indented.bootstrap', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x3079550')._populate(_import_ns, [u'comments'])
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        lib_6 = _mako_get_namespace(context, 'lib_6')
        ihelpers = _mako_get_namespace(context, 'ihelpers')
        lib = _mako_get_namespace(context, 'lib')
        next = _import_ns.get('next', context.get('next', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        # SOURCE LINE 5
        __M_writer(u'\n')
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        lib.return_to() 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<div class="darkened-workshop"></div>\n<div class="spacer"></div>\n<div class="row-fluid min-container" ng-app="civ">\n    <div class="row-fluid" style="position: relative;">\n        <div class="span9 well initiative-panel">\n            <div class="row-fluid">\n')
        # SOURCE LINE 15
        if c.initiativeHome:
            # SOURCE LINE 16
            __M_writer(u'                    <div class="row-fluid">\n                        <div class="thumbnail i-main-photo" style="height: 300px; color: #fff; background-image:url(\'')
            # SOURCE LINE 17
            __M_writer(escape(c.photo_url))
            __M_writer(u'\'); background-position: center center; background-size: cover;"></div>\n                    </div>\n                    ')
            # SOURCE LINE 19
            titleSpan = "row-fluid" 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['titleSpan'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            # SOURCE LINE 20
        else: 
            # SOURCE LINE 21
            __M_writer(u'                    <div class="span2">\n                        <img class="thumbnail tight initiative-thumb" src="')
            # SOURCE LINE 22
            __M_writer(escape(c.thumbnail_url))
            __M_writer(u'">\n                    </div>\n                    ')
            # SOURCE LINE 24
            titleSpan = "span10" 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['titleSpan'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 26
        __M_writer(u'                <div class="')
        __M_writer(escape(titleSpan))
        __M_writer(u'" style="position:relative;">\n                    <h2 class="initiative-title"><a class="no-highlight" href="/initiative/')
        # SOURCE LINE 27
        __M_writer(escape(c.initiative['urlCode']))
        __M_writer(u'/')
        __M_writer(escape(c.initiative['url']))
        __M_writer(u'" ng-init="initiativeTitle = \'')
        __M_writer(escape(c.initiative['title']))
        __M_writer(u'\'" ng-cloak>{{initiativeTitle}}</a></h2>\n                    <h4> \n                        <a href="')
        # SOURCE LINE 29
        __M_writer(escape(c.scopeHref))
        __M_writer(u'"><img class="thumbnail span flag small-flag border right-space" src="')
        __M_writer(escape(c.scopeFlag))
        __M_writer(u'"></a> Initiative for the <a href="')
        __M_writer(escape(c.scopeHref))
        __M_writer(u'" class="green">')
        __M_writer(escape(c.scopeTitle))
        __M_writer(u'</a>\n                        ')
        # SOURCE LINE 30
        __M_writer(escape(lib_6.showTags(c.initiative)))
        __M_writer(u'\n')
        # SOURCE LINE 31
        if c.iPrivs:
            # SOURCE LINE 32
            __M_writer(u'                        <span>\n')
            # SOURCE LINE 33
            if c.editInitiative:
                # SOURCE LINE 34
                __M_writer(u'                                <a class="btn pull-right" href="/initiative/')
                __M_writer(escape(c.initiative['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.initiative['url']))
                __M_writer(u'/show"><strong>View Initiative</strong></a>\n')
                # SOURCE LINE 35
            elif c.initiative.objType != 'revision':
                # SOURCE LINE 36
                __M_writer(u'                                <span class="pull-right">\n                                    <a class="btn" href="/initiative/')
                # SOURCE LINE 37
                __M_writer(escape(c.initiative['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.initiative['url']))
                __M_writer(u'/edit"><strong>Edit Initiative</strong></a>\n                                    <a class="btn" href="/initiative/')
                # SOURCE LINE 38
                __M_writer(escape(c.initiative['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.initiative['url']))
                __M_writer(u'/updateEdit/new"><strong>Add Update</strong></a>\n                                </span>\n')
                # SOURCE LINE 40
            else:
                # SOURCE LINE 41
                __M_writer(u'                                <a class="btn pull-right" href="/initiative/')
                __M_writer(escape(c.initiative['initiativeCode']))
                __M_writer(u'/')
                __M_writer(escape(c.initiative['initiative_url']))
                __M_writer(u'/show"><strong>View Current Version</strong></a>\n')
                pass
            # SOURCE LINE 43
            __M_writer(u'                        </span>\n')
            # SOURCE LINE 44
        elif c.initiativeHome and c.initiative.objType != 'revision':
            # SOURCE LINE 45
            __M_writer(u'                        <span>\n                            ')
            # SOURCE LINE 46
            __M_writer(escape(ihelpers.watchButton(c.initiative)))
            __M_writer(u'\n                        </span>\n')
            pass
        # SOURCE LINE 49
        __M_writer(u'                    </h4>\n                </div>\n')
        # SOURCE LINE 51
        if c.initiativeHome:
            # SOURCE LINE 52
            __M_writer(u'                    <hr class="narrow">\n                    <div class="row-fluid">\n                        ')
            # SOURCE LINE 54
            __M_writer(escape(ihelpers.showAuthor(c.initiative)))
            __M_writer(u'\n                    </div>\n')
            pass
        # SOURCE LINE 57
        __M_writer(u'            </div>\n            <hr class="narrow">\n')
        # SOURCE LINE 59
        if c.initiative['public'] == '0':
            # SOURCE LINE 60
            __M_writer(u'                    <div class="alert alert-warning" style=>This initiative is unpublished. It does not show up in searches or on public listings.</div>\n')
            pass
        # SOURCE LINE 62
        __M_writer(u'            ')
        __M_writer(escape(next.body()))
        __M_writer(u'\n        </div>\n        <div class="span3" id="sidebar">\n            <div style="position:fixed; width: inherit; max-width: 280px;">\n')
        # SOURCE LINE 66
        if c.iPrivs and c.editInitiative and c.initiative.objType != 'initiativeUnpublished':
            # SOURCE LINE 67
            __M_writer(u'                <ul class="nav nav-tabs nav-stacked nav-init no-top" style="width: 100%;">\n                    <li class="active"><a href="#basics">1. Basics</a></li>\n                    <li><a href="#summary">2. Summary</a></li>\n                    <li><a href="#detail">3. Detail</a></li>\n                    <li><a href="#photo">4. Photo</a></li>\n                    <li><a href="#coauthors">5. Coauthors</a></li>\n                    <!--\n                    <li><a href="#iStats" data-toggle="tab">Stats</a></li>\n                    <li><a href="#iUpdates" data-toggle="tab">Updates</a></li>\n                    <li><a href="#iPhotos" data-toggle="tab">Photos</a></li>\n                    -->\n                </ul>\n                <div class="well" style="background-color: whitesmoke;">\n                    <div class="row-fluid">\n')
            # SOURCE LINE 81
            if c.initiative['public'] == '0' and c.complete:
                # SOURCE LINE 82
                __M_writer(u'                            <form method="POST" name="publish" id="publish" action="/initiative/')
                __M_writer(escape(c.initiative['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.initiative['url']))
                __M_writer(u'/edit">\n                                <button type="submit" class="btn btn-large btn-success input-block-level" name="public" value="publish">Publish</button>\n                            </form>\n                            <p>You have added all of the required information. Click \'Publish\' to make your initiative publicly discoverable.</p>\n')
                # SOURCE LINE 86
            elif c.initiative['public'] == '0':
                # SOURCE LINE 87
                __M_writer(u'                            <button class="btn btn-large btn-warning input-block-level" disabled>Publish</button>\n                            <br>\n                            <p>You must complete all required information and upload a picture before you can publish.</p>\n')
                # SOURCE LINE 90
            else:
                # SOURCE LINE 91
                __M_writer(u'                            <div class="row-fluid">\n                                <form method="POST" name="publish" id="publish" action="/unpublish/initiative/')
                # SOURCE LINE 92
                __M_writer(escape(c.initiative['urlCode']))
                __M_writer(u'">\n                                    <button type="submit" class="btn btn-large btn-warning input-block-level" name="public" value="unpublish">Unpublish</button>\n                                </form><br>\n                            </div>\n                            <p>Unpublished initiatives don\'t show up in searches or on public listings.</p>\n')
                pass
            # SOURCE LINE 98
            __M_writer(u'                    </div>\n                </div>\n')
            # SOURCE LINE 100
        elif not c.editInitiative and c.initiative.objType == 'initiative':
            # SOURCE LINE 101
            __M_writer(u'                <div class="section-wrapper overview well initiative-well" style="overflow:visible;">\n')
            # SOURCE LINE 102
            if c.initiative.objType != 'revision':
                # SOURCE LINE 103
                __M_writer(u'                        <h4 class="section-header initiative smaller">Vote</h4>\n                        <div class="row-fluid">\n                            <div class="span6 offset3">\n                                ')
                # SOURCE LINE 106
                __M_writer(escape(lib_6.yesNoVote(c.initiative, 'detail')))
                __M_writer(u'\n                            </div><!-- span4 -->\n                            <div class="span3"></div>\n                        </div>\n                        ')
                # SOURCE LINE 110
                __M_writer(escape(lib_6.showPositions(c.initiative)))
                __M_writer(u'\n                        <h4 class="section-header initiative smaller section-header-inner">Share It</h4>\n                        <div class="row-fluid centered">\n                            <span>\n                                ')
                # SOURCE LINE 114

                subj = 'Vote on "' + c.initiative['title'] + '"'
                subj = subj.replace(' ','%20')
                body = lib_6.initiativeLink(c.initiative, embed=True, noHref=True, fullURL=True)
                                                
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['body','subj'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 118
                __M_writer(u'\n')
                # SOURCE LINE 119
                if c.initiative['public'] == '1':
                    # SOURCE LINE 120
                    __M_writer(u'                                    ')
                    __M_writer(escape(lib_6.facebookDialogShare2(shareOnWall=True, sendMessage=True)))
                    __M_writer(u'\n\n')
                    # SOURCE LINE 122
                    if not c.privs['provisional']:
                        # SOURCE LINE 123
                        __M_writer(u'                                        <a class="btn btn-danger" href="mailto:?subject=')
                        __M_writer(escape(subj))
                        __M_writer(u'&body=')
                        __M_writer(escape(body))
                        __M_writer(u'"><i class="icon-envelope right-space"></i> | Email</i></a>\n')
                        pass
                    # SOURCE LINE 125
                    __M_writer(u'\n                                    <!-- % if c.initiative[\'public\'] == \'1\':\n                                        <a href="/workshop/')
                    # SOURCE LINE 127
                    __M_writer(escape(c.initiative['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.initiative['url']))
                    __M_writer(u'/rss" target="_blank"><i class="icon-rss icon-2x"></i></a>\n                                    #%endif -->\n')
                    # SOURCE LINE 129
                else:
                    # SOURCE LINE 130
                    __M_writer(u'                                    <a class="btn dropdown-toggle btn-primary facebook unpublished disabled" rel="tooltip" data-placement="bottom" data-original-title="Initiative must be published before you can share it." href="#">\n                                        <i class="icon-facebook icon-light right-space"></i> | Share\n                                    </a>\n                                    <a class="btn btn-danger disabled email-invite" href="#" rel="tooltip" data-placement="bottom" data-original-title="Initiative must be published before you can share it."><i class="icon-envelope right-space"></i> | Email</i></a>\n')
                    pass
                # SOURCE LINE 135
                __M_writer(u'                            </span>\n                        \n                        </div>\n                        <div class="row-fluid">\n                            <div class="span10 offset2">\n                                <label class="checkbox grey">\n                                <input type="checkbox" class="shareVote" name="shareVote" value="shareVote"> Show how I voted when sharing\n                                </label>\n                            </div>\n                        </div>\n                        <!-- \n                        <h4 class="section-header smaller section-header-inner">Fund It</h4>\n                        <br>\n                        <div>$136,000 of ')
                # SOURCE LINE 148
                __M_writer(escape(c.initiative['cost']))
                __M_writer(u'</div>\n                        <div class="progress">\n                          <div class="bar bar-primary" style="width: 35%;"></div>\n                        </div>\n                        <small class="pull-right grey" style="margin-top: -20px;">43 funders</small><br>\n                        <div class="row-fluid centered">\n                            <button class="btn-large btn-success btn">Fund Initiative</button>\n                        </div>\n                        -->\n')
                pass
            # SOURCE LINE 158
            __M_writer(u'                </div><!-- section-wrapper -->\n                <!--\n                <ul class="nav nav-tabs nav-stacked nav-init" style="width: 100%;">\n                    <li class="active"><a href="#iText" data-toggle="tab">Text</a></li>\n                    <li><a href="#iResources" data-toggle="tab">Resources</a></li>\n                    <li><a href="#iStats" data-toggle="tab">Stats</a></li>\n                    <li><a href="#iUpdates" data-toggle="tab">Updates</a></li>\n                    <li><a href="#iPhotos" data-toggle="tab">Photos</a></li>\n\n                </ul>\n                -->\n')
            pass
        # SOURCE LINE 170
        __M_writer(u'            </div> <!-- position:fixed -->\n        </div><!-- span4 -->\n    </div><!-- row-fluid -->\n</div><!-- row-fluid -->\n\n')
        # SOURCE LINE 197
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x3079550')._populate(_import_ns, [u'comments'])
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 175
        __M_writer(u'\n')
        # SOURCE LINE 176
        if c.facebookShare:
            # SOURCE LINE 177
            if c.facebookShare.facebookAppId:
                # SOURCE LINE 178
                if c.facebookShare.facebookAppId:
                    # SOURCE LINE 179
                    __M_writer(u'                <meta property="fb:app_id" content="')
                    __M_writer(escape(c.facebookShare.facebookAppId))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 181
                if c.facebookShare.title:
                    # SOURCE LINE 182
                    __M_writer(u'                <meta property="og:title" content="')
                    __M_writer(escape(c.facebookShare.title))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 184
                __M_writer(u'            <meta property="og:site_name" content="Civinomics"/>\n            <meta property="og:locale" content="en_US" /> \n')
                # SOURCE LINE 186
                if c.facebookShare.url:
                    # SOURCE LINE 187
                    __M_writer(u'                <meta property="og:url" content="')
                    __M_writer(escape(c.facebookShare.url))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 189
                if c.facebookShare.description:
                    # SOURCE LINE 190
                    __M_writer(u'                <meta property="og:description" content="')
                    __M_writer(escape(c.facebookShare.description))
                    __M_writer(u'" />\n')
                    pass
                # SOURCE LINE 192
                if c.facebookShare.image:
                    # SOURCE LINE 193
                    __M_writer(u'                <meta property="og:image" content="')
                    __M_writer(escape(c.facebookShare.image))
                    __M_writer(u'"/>\n')
                    pass
                pass
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x3079550')._populate(_import_ns, [u'comments'])
        session = _import_ns.get('session', context.get('session', UNDEFINED))
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 199
        __M_writer(u'\n   <script src="')
        # SOURCE LINE 200
        __M_writer(escape(lib_6.fingerprintFile('/js/follow.js')))
        __M_writer(u'" type="text/javascript"></script>\n   <script type="text/javascript">\n      $(".followButton").tooltip();\n      $(".facebook.unpublished").tooltip();\n      $(".email-invite").tooltip();\n   </script>\n   <script src="/js/bootstrap/bootstrap-affix.js"></script>\n    <script type="text/javascript"> \n        $(\'#initiative-dashboard\').affix({offset: 0})\n    </script> \n    <script type="text/javascript" src="/js/vendor/jquery.backstretch.min.js"></script>\n\n    <script>$.backstretch(')
        # SOURCE LINE 212
        __M_writer(c.bgPhoto_url )
        __M_writer(u', {centeredX: true})</script>\n    <script type="text/javascript" src="/js/vendor/jquery.autosize.js"></script>\n    <script>\n      $(document).ready(function(){\n        $(\'textarea\').autosize();   \n      });\n    </script>\n    <script src="')
        # SOURCE LINE 219
        __M_writer(escape(lib_6.fingerprintFile('/js/yesNo.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script src="')
        # SOURCE LINE 220
        __M_writer(escape(lib_6.fingerprintFile('/js/upDown.js')))
        __M_writer(u'" type="text/javascript"></script>\n    <script type="text/javascript"> \n        $(\'#inner-sidebar\').affix({offset: 130})\n        <!-- $(\'body\').scrollspy({target: \'#sidebar\'}) -->\n        $(window).scrollspy({wrap: $(\'#wrap\')[0]});\n    </script> \n')
        # SOURCE LINE 226
        if 'user' in session:
            # SOURCE LINE 227
            __M_writer(u'        <script src="')
            __M_writer(escape(lib_6.fingerprintFile('/js/flag.js')))
            __M_writer(u'" type="text/javascript"></script>\n        <script src="')
            # SOURCE LINE 228
            __M_writer(escape(lib_6.fingerprintFile('/js/ng/edit_item.js')))
            __M_writer(u'" type="text/javascript"></script>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


