# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398542484.1860509
_template_filename = '/home/maria/civinomics/pylowiki/templates/derived/6_search.bootstrap'
_template_uri = '/derived/6_search.bootstrap'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headScripts', 'extraScripts', 'extraScripts2']


# SOURCE LINE 5
 
import locale
try:
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
except: #windows
    locale.setlocale(locale.LC_ALL, 'eng_US')


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'ng_helpers', context._clean_inheritance_tokens(), templateuri=u'/lib/ng_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'ng_helpers')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

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
        session = context.get('session', UNDEFINED)
        ng_helpers = _mako_get_namespace(context, 'ng_helpers')
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        lib = _mako_get_namespace(context, 'lib')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        # SOURCE LINE 11
        __M_writer(u'\n')
        # SOURCE LINE 12
        lib.return_to() 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<div class="darkened-bg"></div> \n<div class="spacer"></div>\n<div class="row-fluid one-up" ng-controller="SearchCtrl">\n')
        # SOURCE LINE 16
        if c.searchType == 'region':
            # SOURCE LINE 17
            __M_writer(u'        <div class="span2 search-left-column">\n            <img class="thumbnail tight flag pull-left" src="')
            # SOURCE LINE 18
            __M_writer(escape(c.flag))
            __M_writer(u'">\n            <div class="tabbable tabs-left">\n                <ul class="nav nav-pills civ-search-tools tags" ng-hide="showingPeople.show" ng-model="query" ng-cloak>\n                    ')
            # SOURCE LINE 21
            __M_writer(escape(lib_6.public_tag_list_filter()))
            __M_writer(u'\n                </ul>\n            </div>\n        </div>\n')
            pass
        # SOURCE LINE 26
        __M_writer(u'\n    ')
        # SOURCE LINE 27
 
        if c.searchType == 'region':
            spanX = 'span7'
        else:
            spanX = 'span9'
            
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['spanX'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 32
        __M_writer(u'\n\n    <div class="')
        # SOURCE LINE 34
        __M_writer(escape(spanX))
        __M_writer(u' search-middle-column">\n        <div class="row-fluid">\n            <h2 class="lead geoName">\n')
        # SOURCE LINE 37
        if c.searchType == 'region':
            # SOURCE LINE 38
            __M_writer(u'                ')
            __M_writer(escape(c.searchQuery))
            __M_writer(u'\n')
            # SOURCE LINE 39
        elif c.searchType == 'tag':
            # SOURCE LINE 40
            __M_writer(u'                ')
            __M_writer(escape(c.searchTitle))
            __M_writer(u'\n')
            # SOURCE LINE 41
        else:
            # SOURCE LINE 42
            __M_writer(u'                <span class="lead geoName">Results for \'')
            __M_writer(escape(c.searchQuery))
            __M_writer(u"'</span>\n")
            pass
        # SOURCE LINE 44
        __M_writer(u'            </h2>\n        </div>\n        <div class="row-fluid">\n            <ul class="nav nav-pills civ-search-tools">\n                <li ng-class="showingInitiatives.class">\n                    <a href="#initiatives" data-toggle="tab" ng-click="searchInitiatives()">\n                        Initiatives (')
        # SOURCE LINE 50
        __M_writer(escape(c.numInitiatives))
        __M_writer(u')\n                    </a>\n                </li>\n                <li ng-class="showingWorkshops.class">\n                    <a href="#workshops" data-toggle="tab" ng-click="searchWorkshops()">\n                        Workshops (')
        # SOURCE LINE 55
        __M_writer(escape(c.numWorkshops))
        __M_writer(u')\n                    </a>\n                </li>\n')
        # SOURCE LINE 58
        if c.numUsers != 0 or c.searchType == "name":
            # SOURCE LINE 59
            __M_writer(u'                    <li ng-class="showingPeople.class">\n                        <a href="#users" data-toggle="tab" ng-click="searchPeople()">\n                            People (')
            # SOURCE LINE 61
            __M_writer(escape(c.numUsers))
            __M_writer(u')\n                        </a>\n                    </li>\n')
            pass
        # SOURCE LINE 65
        if c.numOrganizations != 0 or c.searchType == "name" or c.searchType == "orgURL":
            # SOURCE LINE 66
            __M_writer(u'                    <li ng-class="showingOrganizations.class">\n                        <a href="#organizations" data-toggle="tab" ng-click="searchOrganizations()">\n                            Organizations (')
            # SOURCE LINE 68
            __M_writer(escape(c.numOrganizations))
            __M_writer(u')\n                        </a>\n                    </li>\n')
            pass
        # SOURCE LINE 72
        __M_writer(u'                <li class="dropdown">\n                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">\n                        More <b class="caret"></b>\n                    </a>\n                    <ul class="dropdown-menu">\n                        <li ng-class="showingIdeas.class">\n                            <a href="#ideas" data-toggle="tab" ng-click="searchIdeas()">\n                                Ideas <span class="pull-right">(')
        # SOURCE LINE 79
        __M_writer(escape(c.numIdeas))
        __M_writer(u')</span>\n                            </a>\n                        </li>\n                        <li ng-class="showingResources.class">\n                            <a href="#resources" data-toggle="tab" ng-click="searchResources()">\n                                Resources <span class="pull-right">(')
        # SOURCE LINE 84
        __M_writer(escape(c.numResources))
        __M_writer(u')</span>\n                            </a>\n                        </li>\n                        <li ng-class="showingDiscussions.class">\n                            <a href="#discussions" data-toggle="tab" ng-click="searchDiscussions()">\n                                Discussions <span class="pull-right">(')
        # SOURCE LINE 89
        __M_writer(escape(c.numDiscussions))
        __M_writer(u') </span>\n                            </a>\n                        </li>\n                        <li class="search-right-column-link" ng-class="showingPhotos.class">\n                            <a href="#photos" data-toggle="tab" ng-click="searchPhotos()">\n                                Photos <span class="pull-right">(')
        # SOURCE LINE 94
        __M_writer(escape(c.numPhotos))
        __M_writer(u') </span>\n                            </a>\n                        </li>\n                    </ul>\n                </li>\n                <li>\n                    <a class="accordion-toggle" href="#sortOptions" data-toggle="collapse">\n                        Search tools\n                    </a>\n                </li>\n\n')
        # SOURCE LINE 106
        __M_writer(u'                <li class="pull-right" ng-show="showingWorkshops.create" ng-cloak>\n')
        # SOURCE LINE 107
        if c.searchType != 'region':
            # SOURCE LINE 108
            if not c.privs['provisional']:
                # SOURCE LINE 109
                __M_writer(u'                            <button class="btn btn-civ" href="/workshop/display/create/form" >\n                                <i class="icon-plus"></i> Start Workshop\n                            </button>\n')
                pass
            # SOURCE LINE 113
        else:
            # SOURCE LINE 114
            if not c.privs['provisional']:
                # SOURCE LINE 115
                __M_writer(u'                            <form id="CreateWorkshop" action = "/workshop/create/handler" method = "post" class="inline">\n                                <input type="hidden" name="geoString" value="')
                # SOURCE LINE 116
                __M_writer(escape(c.geoString))
                __M_writer(u'">\n                                <button class="btn btn-civ" type="submit" name="createPublic"><i class="icon-plus"></i> Start Workshop</button>\n                            </form>\n')
                pass
            pass
        # SOURCE LINE 121
        __M_writer(u'                </li>\n                <li class="pull-right" ng-show="showingInitiatives.create" ng-cloak>\n')
        # SOURCE LINE 123
        if 'user' in session:
            # SOURCE LINE 124
            if c.searchType != 'region':
                # SOURCE LINE 125
                if not c.privs['provisional']:
                    # SOURCE LINE 126
                    __M_writer(u'                                <button class="btn btn-civ" href="/profile/')
                    __M_writer(escape(c.authuser['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.authuser['url']))
                    __M_writer(u'/newInitiative">\n                                    <i class="icon-plus"></i> Start Initiative\n                                </button>\n')
                    pass
                # SOURCE LINE 130
            else:
                # SOURCE LINE 131
                if not c.privs['provisional']:
                    # SOURCE LINE 132
                    __M_writer(u'                                <form id="create_intitiatve" action = "/profile/')
                    __M_writer(escape(c.authuser['urlCode']))
                    __M_writer(u'/')
                    __M_writer(escape(c.authuser['url']))
                    __M_writer(u'/newInitiative" method = "post" class="inline">\n                                    <input type="hidden" name="initiativeRegionScope" value="')
                    # SOURCE LINE 133
                    __M_writer(escape(c.geoString))
                    __M_writer(u'">\n                                    <button class="btn btn-civ" type="submit"><i class="icon-plus"></i> Start Initiative</button>\n                                </form>\n')
                    pass
                pass
            # SOURCE LINE 138
        else:
            # SOURCE LINE 139
            __M_writer(u'                        <button class="btn btn-civ" style="margin-top: 7px;" href="#signupLoginModal" data-toggle="modal"><i class="icon-plus"></i> Start Initiative</button>\n')
            pass
        # SOURCE LINE 141
        __M_writer(u'                </li>\n            </ul>\n\n            <div id="sortOptions" class="row-fluid collapse">\n                <ul class="nav nav-pills civ-search-tools" ng-model="orderProp" ng-hide="showingWorkshops.show || showingPeople.show || showingOrganizations.show" ng-cloak>\n                    <li class="active" ng-class="{active : orderProp == \'-date\'}"><a href="#" ng-click="orderProp = \'-date\'">Recent</a></li>\n                    <!-- <li ng-class="{active : orderProp == \'title\'}"><a href="#" ng-click="orderProp = \'title\'">Alphabetical</a></li> -->\n                    <li ng-class="{active : orderProp == \'-numComments\'}"><a href="#" ng-click="orderProp = \'-numComments\'">Most Comments</a></li>\n                    <li ng-class="{active : orderProp == \'-voteCount\'}"><a href="#" ng-click="orderProp = \'-voteCount\'">Most Votes</a></li>\n                </ul>\n\n                <ul class="nav nav-pills civ-search-tools" ng-model="orderProp" ng-show="showingWorkshops.show" ng-cloak>\n                    <li class="active" ng-class="{active : orderProp == \'-date\'}"><a href="#" ng-click="orderProp = \'-date\'">Date Created</a></li>\n                    <li ng-class="{active : orderProp == \'-startTime\'}"><a href="#" ng-click="orderProp = \'-startTime\'">Start Time</a></li>\n                    <li ng-class="{active : orderProp == \'-bookmarks\'}"><a href="#" ng-click="orderProp = \'-bookmarks\'">Bookmarks</a></li>\n                    <li ng-class="{active : orderProp == \'-activity\'}"><a href="#" ng-click="orderProp = \'-activity\'">Posts</a></li>\n                </ul>\n\n                <ul class="nav nav-pills civ-search-tools" ng-model="orderProp" ng-show="showingPeople.show || showingOrganizations.show" ng-cloak>\n                    <li ng-class="{active : orderProp == \'-date\'}"><a href="#" ng-click="orderProp = \'-date\'">Join Date</a></li>\n                    <li ng-class="{active : orderProp == \'name\'}"><a href="#" ng-click="orderProp = \'name\'">Alphabetical</a></li>\n                </ul>\n            </div>\n        </div>\n        <div class="tabbable">\n            <div class="tab-content">\n                <div class="row-fluid" style="color: #ffffff; padding-bottom: 10px;" ng-cloak>\n                    <form class="form-search inline">\n                    </form>\n                </div>\n                <div class="loading-civ" ng-show="loading" ng-cloak>\n                    <i class="icon-spinner icon-spin icon-4x"></i>\n                </div>\n                <div ng-show="noQuery" ng-cloak>\n                    <div class="row-fluid">\n                        <div class="alert alert-info centered span6 offset3">\n                            Searching for nothing yields nothing.  How zen.\n                        </div>\n                    </div>\n                </div>\n                <div ng-show="noResult" ng-cloak>\n                    <div class="row-fluid">\n                        <div class="alert">\n')
        # SOURCE LINE 184
        if c.searchType == 'region':
            # SOURCE LINE 185
            __M_writer(u"                                We couldn't find any {{objType}} scoped for <strong>")
            __M_writer(escape(c.searchQuery))
            __M_writer(u'</strong>. Be the first to create one!\n')
            # SOURCE LINE 186
        else:
            # SOURCE LINE 187
            __M_writer(u"                                Sorry, we couldn't find any {{objType}} matching <strong>")
            __M_writer(escape(c.searchQuery))
            __M_writer(u'</strong>. Be the first to create one!\n')
            pass
        # SOURCE LINE 189
        __M_writer(u'                            \n                        </div>\n                    </div>\n                </div>\n                <div id="workshops" class="tab-pane" ng-class="showingWorkshops.class" ng-show="showingWorkshops.show" ng-cloak>\n                    <table class="table plain">\n                        <tr ng-repeat="w in workshopArray = (workshops | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize)" class="plain">\n\n                        <div class="alert" ng-show="workshopArray.length == 0">\n                                There are no workshops in <strong>{{query}}</strong> for this region. Be the first to start one!\n                            </div>\n\n                        <td>\n                            <div class="media well searchListing">\n                                <div class="span3">\n                                    <a href = \'/workshops/{{w.urlCode}}/{{w.url}}\'>\n                                        <div style="height:100px; background-image:url(\'{{w.imageURL}}\'); background-repeat:no-repeat; background-size:cover; background-position:center;"/></div>\n                                    </a>\n                                </div>\n                                <div class="span9 media-body">\n                                    <h4 class="media-heading"><a class="listed-item-title" href="/workshops/{{w.urlCode}}/{{w.url}}">{{w.title}}</a></h4>\n                                    <p class="grey"><small>{{w.description}}</small></p>\n                                    <ul class="horizontal-list iconListing">\n                                        <li><i class="icon-bookmark"></i> Bookmarks ({{w.bookmarks}})</li>\n                                        <li><i class="icon-edit"></i> Posts ({{w.activity}})</li>\n                                    </ul>\n                                    <p> <small>Tags:</small>\n                                        <span ng-repeat="tag in w.tags" class="label workshop-tag" ng-class="tag.colour">{{tag.title}}</span>\n                                    </p>\n                                </div>\n                            </div>\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="workshops.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= workshops.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="users" class="tab-pane" ng-class="showingPeople.class" ng-show="showingPeople.show">\n                    <table class="table plain">\n                        <tr ng-repeat = "p in people | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize" class="plain"><td>\n                            <div class="media well searchListing">\n                                <div class="span2">\n                                    <a class="pull-left" href="/profile/{{p.urlCode}}/{{p.url}}">\n                                        <img class="media-object avatar" ng-src="{{p.photo}}" alt="{{p.name}}" title="{{p.name}}">\n                                    </a>\n                                </div>\n                                <div class="span10">\n                                    <h4 class="media-heading"><a class="green green-hover" href="/profile/{{p.urlCode}}/{{p.url}}">{{p.name}}</a></h4>\n                                    <p class="grey">{{p.greetingMsg}}</p>\n                                    <small><p>from <a href="{{p.cityURL}}" class="orange oreange-hover">{{p.cityTitle}}</a>, <a href="{{p.stateURL}}" class="orange orange-hover">{{p.stateTitle}}</a><br>\n                                        joined {{p.date}}</p></small>\n                                </div>\n                            </div>\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="people.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= people.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="organizations" class="tab-pane" ng-class="showingOrganizations.class" ng-show="showingOrganizations.show">\n                    <table class="table plain">\n                        <tr ng-repeat = "o in organizations | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize" class="plain"><td>\n                            <div class="media well searchListing">\n                                <div class="span2">\n                                    <a class="pull-left" href="/profile/{{o.urlCode}}/{{o.url}}">\n                                        <img class="media-object avatar" ng-src="{{o.photo}}" alt="{{o.name}}" title="{{o.name}}">\n                                    </a>\n                                </div>\n                                <div class="span10">\n                                    <h4 class="media-heading"><a class="green green-hover" href="/profile/{{o.urlCode}}/{{o.url}}">{{o.name}}</a></h4>\n                                    <p class="grey">{{p.greetingMsg}}</p>\n                                    <small><p>from <a href="{{o.cityURL}}" class="orange oreange-hover">{{o.cityTitle}}</a>, <a href="{{o.stateURL}}" class="orange orange-hover">{{o.stateTitle}}</a><br>\n                                        joined {{o.date}}</p></small>\n                                </div>\n                            </div>\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="organizations.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= organizations.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="resources" class="tab-pane" ng-class="showingResources.class" ng-show="showingResources.show">\n                    <table class="table plain">\n                        <tr ng-repeat = "resource in resourceArray = ( resources | filter: query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize ) " class="plain">\n\n                        <div class="alert" ng-show="resourceArray.length == 0">\n                                There are no resources in <strong>{{query}}</strong> for this region. Be the first to add one!\n                            </div>\n\n                        <td>\n                            <div class="media well searchListing">\n                                <div class="span1">\n                                   <i class="icon-{{resource.type}} icon-3x"></i>\n                                </div>\n                                <div class="span11 media-body">\n                                    <h4 class="media-heading"><a class="listed-item-title" href="/{{resource.parentType}}/{{resource.parentCode}}/{{resource.parentURL}}/resource/{{resource.urlCode}}/{{resource.url}}">\n                                        {{resource.title}}\n                                    </a></h4>\n                                    <a class="break" href="/{{resource.parentType}}/{{resource.parentCode}}/{{resource.parentURL}}/resource/{{resource.urlCode}}/{{resource.url}}">{{resource.link}}</a>\n\n                                    <ul class="horizontal-list iconListing">\n                                        <li>\n                                            <i class="{{resource.parentIcon}}"></i> From {{resource.parentType}}: <a href="/{{resource.parentType}}/{{resource.parentCode}}/{{resource.parentURL}}">\n                                                {{resource.parentTitle}}\n                                            </a>\n                                        </li>\n                                        <li><i class="icon-chevron-sign-up"></i> Net votes ({{resource.voteCount}})</li>\n                                        <li><i class="icon-comment"></i> Comments ({{resource.numComments}})</li>\n                                    </ul>\n                                    <p> <small>Tags:</small>\n                                        <span ng-repeat="tag in resource.tags" class="label workshop-tag" ng-class="tag.colour">{{tag.title}}</span>\n                                    </p>\n                                </div>\n                            </div>\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="resources.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= resources.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="discussions" class="tab-pane" ng-class="showingDiscussions.class" ng-show="showingDiscussions.show">\n                    <table class="table plain">                             \n                        <tr ng-repeat = "discussion in discussionArray = (discussions | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize)" class="plain">\n\n                        <div class="alert" ng-show="discussionArray.length == 0">\n                                There are no discussions in <strong>{{query}}</strong> for this region. Be the first to add one!\n                            </div>\n\n                        <td>\n                            <div class="media well searchListing">\n                                <div class="span1">\n                                   <i class="icon-comments icon-3x"></i>\n                                </div>\n                                <div class="span11 media-body">\n                                    <h4 class="media-heading"><a class="listed-item-title" href="/workshop/{{discussion.workshopCode}}/{{discussion.workshopURL}}/discussion/{{discussion.urlCode}}/{{discussion.url}}">\n                                        {{discussion.title}}\n                                    </a></h4>\n                                    <ul class="horizontal-list iconListing">\n                                        <li>\n                                            <i class="icon-cog"></i> From workshop: <a href="/workshop/{{discussion.workshopCode}}/{{discussion.workshopURL}}">\n                                                {{discussion.workshopTitle}}\n                                            </a>\n                                        </li>\n                                        <li>\n                                            <i class="icon-comment"></i> Comments ({{discussion.numComments}})\n                                        </li>\n                                    </ul>\n                                    <p> <small>Tags:</small>\n                                        <span ng-repeat="tag in discussion.tags" class="label workshop-tag" ng-class="tag.colour">{{tag.title}}</span>\n                                    </p>\n                                    <p class="no-bottom">\n                                        <span class="left-space"><a href="/profile/{{discussion.authorCode}}/{{discussion.authorURL}}"><img class="avatar topbar-avatar" ng-src="http://www.gravatar.com/avatar/{{discussion.authorHash}}?r=pg&d=identicon&s=200" alt="{{discussion.authorName}}" title="{{discussion.authorName}}"></a><small> Posted by <a class="green green-hover" href="/profile/{{discussion.authorCode}}/{{discussion.authorURL}}">{{discussion.authorName}}</a></small></span>\n                                    </p>\n                                </div>\n                            </div>\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="discussions.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= discussions.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="ideas" class="tab-pane" ng-class="showingIdeas.class" ng-show="showingIdeas.show">\n                    <table class="table plain">\n                        <tr ng-repeat = "idea in ideaArray = (ideas | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize)" class="plain">\n\n                        <div class="alert" ng-show="ideaArray.length == 0">\n                                There are no ideas in <strong>{{query}}</strong> for this region. Be the first to add one!\n                            </div>\n\n                        <td>\n                            <div class="media well searchListing" ng-init="rated=idea.rated; urlCode=idea.urlCode;url=idea.url; totalVotes=idea.voteCount; yesVotes=idea.ups; noVotes=idea.downs; objType=\'idea\';">\n                                <div class="media-body" ng-controller="yesNoVoteCtrl">\n                                    <div class="span9">\n                                        <p class="ideaListingTitle"><a class="listed-item-title" href="/workshop/{{idea.workshopCode}}/{{idea.workshopURL}}/idea/{{idea.urlCode}}/{{idea.url}}">\n                                            {{idea.title}}\n                                        </a></p>\n                                        <ul class="horizontal-list iconListing">\n                                            <li><i class="icon-check-sign"></i> Total votes ({{totalVotes}})</li>\n                                            <li><i class="icon-comment"></i> Comments ({{idea.numComments}})</li>\n                                            <li>\n                                                <i class="icon-cog"></i> From workshop: <a href="/workshop/{{idea.workshopCode}}/{{idea.workshopURL}}">\n                                                    {{idea.workshopTitle}}\n                                                </a>\n                                            </li>\n                                        </ul>\n                                        <small>Tags:</small>\n                                            <span ng-repeat="tag in idea.tags" class="label workshop-tag" ng-class="tag.colour">{{tag.title}}</span>\n                                        <p>\n                                            <span class="left-space"><a href="/profile/{{idea.authorCode}}/{{idea.authorURL}}"><img class="avatar topbar-avatar" ng-src="http://www.gravatar.com/avatar/{{idea.authorHash}}?r=pg&d=identicon&s=200" alt="{{idea.authorName}}" title="{{idea.authorName}}"></a><small> Posted by <a class="green green-hover" href="/profile/{{idea.authorCode}}/{{idea.authorURL}}">{{idea.authorName}}</a></small></span>\n                                        </p>\n                                    </div>\n                                    <div class="span3 voteBlock ideaListing well" >\n')
        # SOURCE LINE 416
        if 'user' in session:
            # SOURCE LINE 417
            __M_writer(u'                                            <a ng-click="updateYesVote()" class="yesVote {{yesVoted}}">\n                                                <div class="vote-icon yes-icon detail"></div>\n                                                <div class="ynScoreWrapper"><span class="yesScore {{display}}">{{yesPercent | number:0 }}%</span></div>\n                                            </a>\n                                            <br>\n                                            <br>\n                                            <a ng-click="updateNoVote()" class="noVote {{noVoted}}">\n                                                <div class="vote-icon no-icon detail"></div>\n                                                <div class="ynScoreWrapper"><span class="noScore {{display}}">{{noPercent | number:0 }}%</span></div>\n                                            </a>\n                                            <br>\n                                            <div class="totalVotesWrapper">\n                                                <small class="grey pull-left">Votes:</small>\n                                                <strong class="pull-right">\n                                                    <span class="totalVotes">{{totalVotes}}</span>\n                                                </strong>\n                                            </div>\n')
            # SOURCE LINE 434
        else:
            # SOURCE LINE 435
            __M_writer(u'                                            <a href="#signupLoginModal" class="yesVote">\n                                                <div class="vote-icon yes-icon"></div>\n                                            </a>\n                                            <br>\n                                            <br>\n                                            <a href="#signupLoginModal" class="noVote">\n                                                <div class="vote-icon no-icon"></div>\n                                            </a>\n')
            pass
        # SOURCE LINE 444
        __M_writer(u'                                    </div>\n                                </div><!-- media-body -->\n                            </div><!-- search-listing -->\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="ideas.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= ideas.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="photos" class="tab-pane" ng-class="showingPhotos.class" ng-show="showingPhotos.show">\n                    <table class="table plain">\n                        <tr ng-repeat = "photo in photoArray = (photos | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize)" class="plain">\n\n                        <div class="alert" ng-show="photoArray.length == 0">\n                                There are no photos in <strong>{{query}}</strong> for this region. Be the first to add one!\n                            </div>\n\n                        <td>\n                            <div class="media well searchListing" ng-init="rated=photo.rated; urlCode=photo.urlCode;url=photo.url; totalVotes=photo.voteCount;netVotes=photo.netVotes;objType=\'photo\';">\n                                <div class="media-body" ng-controller="yesNoVoteCtrl">\n                                    <div class="span1 voteWrapper" >\n')
        # SOURCE LINE 472
        if 'user' in session:
            # SOURCE LINE 473
            __M_writer(u'                                            <a ng-click="updateYesVote()" class="upVote {{yesVoted}}">\n                                                <i class="icon-chevron-sign-up icon-2x {{yesVoted}}"></i>\n                                            </a>\n                                            <br>\n                                            <div class="centered chevron-score"> {{netVotes}}</div>\n                                            <a ng-click="updateNoVote()" class="downVote {{noVoted}}">\n                                                <i class="icon-chevron-sign-down icon-2x {{noVoted}}"></i>\n                                            </a>\n')
            # SOURCE LINE 481
        else:
            # SOURCE LINE 482
            __M_writer(u'                                            <a href="/login" class="upVote">\n                                                <i class="icon-chevron-sign-up icon-2x"></i>\n                                            </a>\n                                            <br>\n                                            <div class="centered chevron-score"> {{netVotes}}</div>\n                                            <a href="/login" class="downVote">\n                                                <i class="icon-chevron-sign-down icon-2x"></i>\n                                            </a>\n')
            pass
        # SOURCE LINE 491
        __M_writer(u'                                        <br>\n                                    </div>\n                                    <div class="pull-left">\n                                        <a href="{{photo.photoLink}}"><img src="{{photo.thumbnail}}"></a>\n                                    </div>\n                                    <div class="media-body">\n                                        <h4 class="media-heading">\n                                            <a class="listed-item-title" href="{{photo.photoLink}}">{{photo.title}}</a>\n                                        </h4>\n                                        <small>\n                                            Posted by: <a href="/profile/{{photo.authorCode}}/{{photo.authorURL}}">{{photo.authorName}}</a><br />\n                                            Location: {{photo.location}}<br />\n                                            Tags: <span ng-repeat="tag in photo.tags" class="label workshop-tag {{tag}}">{{tag}}</span>\n                                        </small>\n                                        <br />\n                                        <ul class="horizontal-list iconListing">\n                                            <li><i class="icon-comment"></i> Comments ({{photo.numComments}})</li>\n                                        </ul>\n                                    </div>\n                                </div>\n                            </div>\n                        </td></tr>\n                    </table>\n                    <div class="centered" ng-show="photos.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= photos.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n                <div id="initiatives" class="tab-pane" ng-class="showingInitiatives.class" ng-show="showingInitiatives.show">\n                    <table class="table plain">\n                        <tr ng-repeat = "item in initiativeArray = (initiatives | filter:query | orderBy:orderProp | startFrom:currentPage*pageSize | limitTo:pageSize)" class="plain">\n\n                            <div class="alert" ng-show="initiativeArray.length == 0">\n                                There are no initiatives in <strong>{{query}}</strong> for this region. Be the first to start one!\n                            </div>\n                            \n                            <td>\n                                ')
        # SOURCE LINE 534
        __M_writer(escape(ng_helpers.initiative_listing()))
        __M_writer(u'\n                            </td>\n\n                        </tr>\n                    </table>\n                    <div class="centered" ng-show="initiatives.length>pageSize">\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage == 0" ng-click="currentPage=currentPage-1">\n                            Prev\n                        </button>\n                        <span style="color: #ffffff;"> <strong>{{currentPage+1}}</strong> of <strong>{{numberOfPages()}}</strong> </span>\n                        <button class="btn" onclick="$(\'html,body\').scrollTop(0);" ng-disabled="currentPage >= initiatives.length/pageSize - 1" ng-click="currentPage=currentPage+1">\n                            Next\n                        </button>\n                        <div class="spacer"></div>\n                    </div>\n                </div>\n            </div><!-- tab-content -->\n        </div><!-- tabbable tabs-left civ-search -->\n    </div><!-- span7 -->\n')
        # SOURCE LINE 553
        if c.searchType == 'region' or c.searchType == 'tag':
            # SOURCE LINE 554
            __M_writer(u'        <div class="span2 search-right-column">\n')
            # SOURCE LINE 555
            if c.searchType == 'region' and c.geoInfo:
                # SOURCE LINE 556
                __M_writer(u'                <div class="well">\n                    <span>Stats</span>\n                    <form class="form-horizontal stats">\n                        <div class="control-group">\n                            <label class="control-label grey" for="inputEmail">Population:</label>\n                            <div class="controls">\n                                <span class="pull-right"><strong>')
                # SOURCE LINE 562
                __M_writer(escape(locale.format("%d", c.population, grouping=True)))
                __M_writer(u'</strong></span>\n                            </div>\n                        </div>\n                        <div class="control-group">\n                            <label class="control-label grey" for="inputEmail">Median Age:</label>\n                            <div class="controls">\n                                <span class="pull-right"><strong>')
                # SOURCE LINE 568
                __M_writer(escape(locale.format("%d", c.medianAge, grouping=True)))
                __M_writer(u'</strong></span>\n                            </div>\n                        </div>\n                        <div class="control-group">\n                            <label class="control-label grey" for="inputEmail">Persons per Household:</label>\n                            <div class="controls">\n                                <span class="pull-right"><strong>')
                # SOURCE LINE 574
                __M_writer(escape(locale.format("%d", c.personsHousehold, grouping=True)))
                __M_writer(u'</strong></span>\n                            </div>\n                        </div>\n')
                # SOURCE LINE 577
                if 'Postal Code' in c.searchQuery:
                    # SOURCE LINE 578
                    __M_writer(u'                            <hr class="stats">\n                            <div class="control-group">\n                                <label class="control-label grey" for="inputEmail">Income per Household:</label>\n                                <div class="controls">\n                                    <span class="pull-right"><strong>$')
                    # SOURCE LINE 582
                    __M_writer(escape(locale.format("%d", c.incomePerHousehold, grouping=True)))
                    __M_writer(u'</strong></span>\n                                </div>\n                            </div>\n                            <div class="control-group">\n                                <label class="control-label grey" for="inputEmail">Avg House Value:</label>\n                                <div class="controls">\n                                    <span class="pull-right"><strong>$')
                    # SOURCE LINE 588
                    __M_writer(escape(locale.format("%d", c.avgHouseValue, grouping=True)))
                    __M_writer(u'</strong></span>\n                                </div>\n                            </div>\n                            <div class="control-group">\n                                <label class="control-label grey" for="inputEmail">Business Annual Payroll:</label>\n                                <div class="controls">\n                                    <span class="pull-right"><strong>$')
                    # SOURCE LINE 594
                    __M_writer(escape(locale.format("%d", c.bizAnnualPayroll, grouping=True)))
                    __M_writer(u'</strong></span>\n                                </div>\n                            </div>\n')
                    pass
                # SOURCE LINE 598
                __M_writer(u'                    </form>\n                </div>\n')
                pass
            # SOURCE LINE 601
            __M_writer(u'            <div class="well">\n                <span>\n                    <a href="#photos" class="green green-hover" ng-click="searchPhotos()">\n                        Photos (')
            # SOURCE LINE 604
            __M_writer(escape(c.numPhotos))
            __M_writer(u')\n                    </a>\n')
            # SOURCE LINE 606
            if c.authuser:
                # SOURCE LINE 607
                __M_writer(u'                        <a href="/profile/')
                __M_writer(escape(c.authuser['urlCode']))
                __M_writer(u'/')
                __M_writer(escape(c.authuser['url']))
                __M_writer(u'/photos/show" class="btn btn-civ btn-small pull-right bottom-space"><i class="icon-plus"></i>\n                        </a>\n')
                # SOURCE LINE 609
            else:
                # SOURCE LINE 610
                __M_writer(u'                        <a href="/login" class="btn btn-civ btn-small pull-right bottom-space"><i class="icon-plus"></i>\n                        </a>\n')
                pass
            # SOURCE LINE 613
            __M_writer(u'                </span>\n')
            # SOURCE LINE 614
            if c.photos:
                # SOURCE LINE 615
                __M_writer(u'                    <img class="thumbnail tight" src="')
                __M_writer(escape(c.backgroundPhoto))
                __M_writer(u'">\n                    Top photo by ')
                # SOURCE LINE 616
                __M_writer(escape(lib_6.userLink(c.backgroundAuthor)))
                __M_writer(u'\n')
                # SOURCE LINE 617
            else:
                # SOURCE LINE 618
                __M_writer(u'                    <div class="alert photo-alert">\n                      <strong>No photos!</strong> Be the first to add one.\n                    </div>\n')
                pass
            # SOURCE LINE 622
            __M_writer(u'            </div>\n        </div> <!-- span3 search-right-column -->\n')
            pass
        # SOURCE LINE 625
        __M_writer(u'</div><!-- row-fluid -->\n\n')
        # SOURCE LINE 632
        __M_writer(u'\n\n')
        # SOURCE LINE 641
        __M_writer(u'\n\n')
        # SOURCE LINE 648
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headScripts(context):
    context.caller_stack._push_frame()
    try:
        lib_6 = _mako_get_namespace(context, 'lib_6')
        __M_writer = context.writer()
        # SOURCE LINE 627
        __M_writer(u'\n    <script src="//cdnjs.cloudflare.com/ajax/libs/angular-strap/0.7.1/angular-strap.min.js"></script>\n    <script type="text/javascript" src="')
        # SOURCE LINE 629
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/search.js')))
        __M_writer(u'"></script>\n    <script type="text/javascript" src="')
        # SOURCE LINE 630
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/yesno_vote.js')))
        __M_writer(u'"></script>\n    <script type="text/javascript" src="')
        # SOURCE LINE 631
        __M_writer(escape(lib_6.fingerprintFile('/js/ng/activity.js')))
        __M_writer(u'"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 634
        __M_writer(u'\n    <script type="text/javascript" src="/js/vendor/jquery.backstretch.min.js"></script>\n   ')
        # SOURCE LINE 636

        backgroundImage = '"' + c.backgroundPhoto + '"'
        
           
        
        # SOURCE LINE 639
        __M_writer(u'\n   <script>$.backstretch(')
        # SOURCE LINE 640
        __M_writer(backgroundImage )
        __M_writer(u', {centeredX: true})</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extraScripts2(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 643
        __M_writer(u'\n    <script src="/js/bootstrap/bootstrap-tooltip.js"></script>\n    <script type="text/javascript">\n        $(\'.upVote.nullvote\').tooltip();\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


