# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1398542482.4292741
_template_filename = u'/home/maria/civinomics/pylowiki/templates/lib/ng_lib.mako'
_template_uri = u'/lib/ng_lib.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['yesNoVoteBlock', 'upDownVoteBlock', 'photo_listing', 'actions', 'moreLessComment', 'idea_listing', 'resource_listing', 'moreLess', 'initiative_listing', 'metaData', 'discussion_listing']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 1
    ns = runtime.TemplateNamespace(u'lib_6', context._clean_inheritance_tokens(), templateuri=u'/lib/6_lib.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, u'lib_6')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        # SOURCE LINE 32
        __M_writer(u'\n\n')
        # SOURCE LINE 59
        __M_writer(u'\n\n')
        # SOURCE LINE 77
        __M_writer(u'\n\n')
        # SOURCE LINE 95
        __M_writer(u'\n\n')
        # SOURCE LINE 118
        __M_writer(u'\n\n')
        # SOURCE LINE 161
        __M_writer(u'\n\n')
        # SOURCE LINE 184
        __M_writer(u'\n\n')
        # SOURCE LINE 188
        __M_writer(u'\n\n')
        # SOURCE LINE 192
        __M_writer(u'\n\n')
        # SOURCE LINE 202
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_yesNoVoteBlock(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 120
        __M_writer(u'\n')
        # SOURCE LINE 121
        if 'user' in session and c.authuser['memberType'] == 'organization':
            # SOURCE LINE 122
            __M_writer(u'        <p><a ng-href="{{item.href}}">State a Position</a></p>\n        Votes: <span class="totalVotes">{{totalVotes}}</span></br>\n        No:  {{noPercent | number:0 }}%</br>\n        Yes: {{yesPercent | number:0 }}%</br>\n')
            # SOURCE LINE 126
        elif 'user' in session:
            # SOURCE LINE 127
            __M_writer(u'        <a ng-click="updateYesVote()" class="yesVote {{yesVoted}}">\n            <div class="vote-icon yes-icon detail"></div>\n            <div class="ynScoreWrapper"><span class="yesScore {{display}}">{{yesPercent | number:0 }}%</span></div>\n        </a>\n        <br>\n        <br>\n        <a ng-click="updateNoVote()" class="noVote {{noVoted}}">\n            <div class="vote-icon no-icon detail"></div>\n            <div class="ynScoreWrapper"><span class="noScore {{display}}">{{noPercent | number:0 }}%</span></div>\n        </a>\n        <br>\n        <div class="totalVotesWrapper">\n            <span class="grey pull-left">Votes:</span>\n            <strong class="pull-right">\n                <span class="totalVotes">{{totalVotes}}</span>\n            </strong>\n        </div>\n')
            # SOURCE LINE 144
        elif 'user' not in session:
            # SOURCE LINE 145
            __M_writer(u'        <a href="#signupLoginModal" role="button" data-toggle="modal" class="yesVote">\n            <div class="vote-icon yes-icon"></div>\n        </a>\n        <br>\n        <br>\n        <a href="#signupLoginModal" role="button" data-toggle="modal" class="noVote">\n            <div class="vote-icon no-icon"></div>\n        </a>\n        <br>\n        <div class="totalVotesWrapper">\n            <small class="grey pull-left">Votes:</small>\n            <strong class="pull-right">\n                <span class="totalVotes">{{totalVotes}}</span>\n            </strong>\n        </div>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_upDownVoteBlock(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 163
        __M_writer(u'   \n')
        # SOURCE LINE 164
        if 'user' in session:
            # SOURCE LINE 165
            __M_writer(u'        <a ng-click="updateYesVote()" class="upVote {{yesVoted}}">\n            <i class="icon-chevron-sign-up icon-2x {{yesVoted}}"></i>\n        </a>\n        <br>\n        <div class="centered chevron-score"> {{netVotes}}</div>\n        <a ng-click="updateNoVote()" class="downVote {{noVoted}}">\n            <i class="icon-chevron-sign-down icon-2x {{noVoted}}"></i>\n        </a>\n')
            # SOURCE LINE 173
        else:
            # SOURCE LINE 174
            __M_writer(u'        <a href="#signupLoginModal" data-toggle="modal" class="upVote">\n            <i class="icon-chevron-sign-up icon-2x"></i>\n        </a>\n        <br>\n        <div class="centered chevron-score"> {{netVotes}}</div>\n        <a href="#signupLoginModal" data-toggle="modal" class="downVote">\n            <i class="icon-chevron-sign-down icon-2x"></i>\n        </a>\n')
            pass
        # SOURCE LINE 183
        __M_writer(u'    <br>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_photo_listing(context):
    context.caller_stack._push_frame()
    try:
        def upDownVoteBlock():
            return render_upDownVoteBlock(context)
        def moreLess():
            return render_moreLess(context)
        def actions():
            return render_actions(context)
        def metaData():
            return render_metaData(context)
        __M_writer = context.writer()
        # SOURCE LINE 97
        __M_writer(u'\n    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">\n        <div class="row-fluid" ng-controller="yesNoVoteCtrl">\n            <div class="span11 media-body">\n                <div class="listed-photo">\n                    <a href = \'{{item.href}}\'>\n                        <div class="main-photo" style="background-image:url(\'{{item.mainPhoto}}\');"/></div> \n                    </a>\n                </div>\n                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>\n                <p><small>')
        # SOURCE LINE 107
        __M_writer(escape(metaData()))
        __M_writer(u'</small></p>\n                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>')
        # SOURCE LINE 108
        __M_writer(escape(moreLess()))
        __M_writer(u'</p>\n            </div>\n            <div class="span1 voteWrapper">\n                ')
        # SOURCE LINE 111
        __M_writer(escape(upDownVoteBlock()))
        __M_writer(u'\n            </div>\n        </div>\n        <div class="row-fluid">\n            ')
        # SOURCE LINE 115
        __M_writer(escape(actions()))
        __M_writer(u'\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_actions(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        lib_6 = _mako_get_namespace(context, 'lib_6')
        def moreLessComment():
            return render_moreLessComment(context)
        __M_writer = context.writer()
        # SOURCE LINE 204
        __M_writer(u'\n    <div ng-init="type = item.objType; discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; submit = \'reply\'; numComments = item.numComments;">\n        <div ng-controller="commentsController">\n            <ul class="horizontal-list iconListing">\n                <li>\n                    <a ng-show="item.numComments == \'0\'" class="no-highlight" ng-click="showAddComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>\n                    <a ng-show="!(item.numComments == \'0\')" class="no-highlight" ng-click="getComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>\n                </li>\n                <li><i class="icon-eye-open"></i> Views ({{item.views}})</li>\n            </ul>\n')
        # SOURCE LINE 215
        __M_writer(u'            <div class="centered" ng-show="commentsLoading" ng-cloak>\n                <i class="icon-spinner icon-spin icon-2x"></i>\n            </div>\n\n            <table class="activity-comments" ng-class="{hidden : commentsHidden}" style = "background-color: whitesmoke;">\n                <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == \'yes\', con : comment.commentRole == \'no\', neutral : comment.commentRole == \'neutral\'}">\n\n                    <td class="comment-avatar-cell">\n                        <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">\n                    </td>\n                    <td style="padding: 10px;">\n                        <small><a class="no-highlight" ng-href="{{comment.authorHref}}"><strong>{{comment.authorName}}</strong></a><span class="date">{{comment.date}} ago</span></small>\n                        <br>\n                        <p ng-init="stringLimit=300"><span ng-bind-html="comment.html | limitTo:stringLimit"></span>')
        # SOURCE LINE 228
        __M_writer(escape(moreLessComment()))
        __M_writer(u'</p>                   \n                  </td>\n                </tr>\n                \n                <tr ng-show="newCommentLoading" ng-cloak>\n                    <td></td>\n                    <td>\n                        <div class="centered">\n                            <i class="icon-spinner icon-spin icon-2x"></i>\n                        </div>\n                    </td>\n                </tr>\n                <tr>\n')
        # SOURCE LINE 241
        if c.authuser:
            # SOURCE LINE 242
            __M_writer(u'                        <td class="comment-avatar-cell">')
            __M_writer(escape(lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")))
            __M_writer(u'</td>\n                        <td style="padding: 10px;">\n')
            # SOURCE LINE 244
            if c.privs and not c.privs['provisional']:
                # SOURCE LINE 245
                __M_writer(u'                                <form class="no-bottom" ng-submit="submitComment()">\n                                    <textarea class="span10" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>\n                                    <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>\n                                    <div ng-show="type == \'initiative\' || type == \'idea\'">\n                                        <label class="radio inline">\n                                            <input type="radio" name="commentRole" ng-model="commentRole" value="yes"> Pro\n                                        </label>\n                                        <label class="radio inline">\n                                            <input type="radio" name="commentRole" ng-model="commentRole" value="neutral"> Neutral\n                                        </label>\n                                        <label class="radio inline">\n                                            <input type="radio" name="commentRole" ng-model="commentRole" value="no"> Con\n                                        </label>\n                                    </div>\n                                </form>\n')
                # SOURCE LINE 260
            else:
                # SOURCE LINE 261
                __M_writer(u'                                <a href="#activateAccountModal" data-toggle=\'modal\'>\n                                    <textarea class="span10" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>\n                                    <a href="#activateAccountModal" data-toggle=\'modal\' class="btn btn-success" style="vertical-align: top;">Submit</a>\n                                </a>\n')
                pass
            # SOURCE LINE 266
            __M_writer(u'                        </td>\n')
            # SOURCE LINE 267
        else:
            # SOURCE LINE 268
            __M_writer(u'                        <td class="comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar small-avatar"></td>\n                        <td style="padding: 10px;">\n                            <form class="no-bottom" ng-submit="submitComment()">\n                                <a href="#signupLoginModal" data-toggle=\'modal\'>\n                                    <textarea class="span10" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>\n                                    <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>\n                                </a>\n                                <div ng-show="type == \'initiative\' || type == \'idea\'">\n                                    <a href="#signupLoginModal" data-toggle=\'modal\' class="no-highlight no-hover">\n                                        <label class="radio inline">\n                                            <input type="radio"> Pro\n                                        </label>\n                                        <label class="radio inline">\n                                            <input type="radio"> Neutral\n                                        </label>\n                                        <label class="radio inline">\n                                            <input type="radio"> Con\n                                        </label>\n                                    </a>\n                                </div>\n                            </form>\n                        </td>\n')
            pass
        # SOURCE LINE 291
        __M_writer(u'                </tr> \n            </table>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_moreLessComment(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 190
        __M_writer(u'\n    <a class="green green-hover" ng-show="comment.text.length > 300 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{comment.urlCode}}" class="green green-hover"  ng-show="comment.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_idea_listing(context):
    context.caller_stack._push_frame()
    try:
        def yesNoVoteBlock():
            return render_yesNoVoteBlock(context)
        c = context.get('c', UNDEFINED)
        def moreLess():
            return render_moreLess(context)
        def actions():
            return render_actions(context)
        def metaData():
            return render_metaData(context)
        __M_writer = context.writer()
        # SOURCE LINE 34
        __M_writer(u'\n        <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">\n            <div class="media-body row-fluid" ng-controller="yesNoVoteCtrl">\n                <div class="well yesNoWell" >\n                    ')
        # SOURCE LINE 38
        __M_writer(escape(yesNoVoteBlock()))
        __M_writer(u'\n                </div>\n                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>\n')
        # SOURCE LINE 41
        if not c.w:
            # SOURCE LINE 42
            __M_writer(u'                    <p><small>')
            __M_writer(escape(metaData()))
            __M_writer(u'</small></p>\n')
            pass
        # SOURCE LINE 44
        __M_writer(u'                <strong ng-if="item.status == \'adopted\'" class="green"><i class="icon-star"></i> Adopted</strong>\n                <strong ng-if="item.status == \'disabled\'" class="red"><i class="icon-flag"></i> Disabled</strong>\n                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>')
        # SOURCE LINE 46
        __M_writer(escape(moreLess()))
        __M_writer(u'</p>\n            </div><!-- media-body -->\n            <div class="row-fluid">\n')
        # SOURCE LINE 49
        if c.w:
            # SOURCE LINE 50
            __M_writer(u'                    <img class="avatar small-avatar inline" ng-src="{{item.authorPhoto}}" alt="{{item.authorName}}" title="{{item.authorName}}">\n                    <small>\n                      <a href="{{item.authorHref}}" class="green green-hover">{{item.authorName}}</a> \n                      <span class="date">{{item.fuzzyTime}} ago</span>\n                    </small>\n')
            pass
        # SOURCE LINE 56
        __M_writer(u'                ')
        __M_writer(escape(actions()))
        __M_writer(u'\n            </div>\n        </div><!-- search-listing -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_resource_listing(context):
    context.caller_stack._push_frame()
    try:
        def upDownVoteBlock():
            return render_upDownVoteBlock(context)
        def actions():
            return render_actions(context)
        def metaData():
            return render_metaData(context)
        __M_writer = context.writer()
        # SOURCE LINE 61
        __M_writer(u'\n    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">\n        <div class="row-fluid" ng-controller="yesNoVoteCtrl">\n            <div class="span11 media-body">\n                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>\n                <p><small>')
        # SOURCE LINE 66
        __M_writer(escape(metaData()))
        __M_writer(u'</small></p>\n                <p><a class="break" href="{{item.link}}" target="_blank">{{item.link}}</a><p>\n            </div>\n            <div class="span1 voteWrapper">\n                ')
        # SOURCE LINE 70
        __M_writer(escape(upDownVoteBlock()))
        __M_writer(u'\n            </div>\n        </div>\n        <div class="row-fluid">\n            ')
        # SOURCE LINE 74
        __M_writer(escape(actions()))
        __M_writer(u'\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_moreLess(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 186
        __M_writer(u'\n    <a class="green green-hover" ng-show="item.text.length > 300 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{item.urlCode}}" class="green green-hover"  ng-show="item.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_initiative_listing(context):
    context.caller_stack._push_frame()
    try:
        def yesNoVoteBlock():
            return render_yesNoVoteBlock(context)
        def moreLess():
            return render_moreLess(context)
        def actions():
            return render_actions(context)
        def metaData():
            return render_metaData(context)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">\n        <div ng-controller="yesNoVoteCtrl"> \n            <div class="row-fluid">\n                <div class="span3">\n                    <div class="listed-photo">\n                        <a href = \'{{item.href}}\'>\n                            <div class="i-photo" style="background-image:url(\'{{item.thumbnail}}\');"/></div> \n                        </a>\n                    </div>\n                </div>\n                <div class="span9">\n                    <div class="well yesNoWell" >\n                        ')
        # SOURCE LINE 16
        __M_writer(escape(yesNoVoteBlock()))
        __M_writer(u'\n                    </div>\n                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>\n                    <p><small>')
        # SOURCE LINE 19
        __M_writer(escape(metaData()))
        __M_writer(u'</small></p>\n                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>')
        # SOURCE LINE 20
        __M_writer(escape(moreLess()))
        __M_writer(u'</p>\n                    <h4>\n                        <small class="grey centered">Estimated Cost:</small>\n                        <span class="pull-right">{{item.cost | currency}}</span>\n                    </h4>\n                </div>\n            </div>\n            <div class="row-fluid">\n                ')
        # SOURCE LINE 28
        __M_writer(escape(actions()))
        __M_writer(u'\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_metaData(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 194
        __M_writer(u'\n    <small><img class="thumbnail flag mini-flag border" src="{{item.flag}}"> \n        <span style="text-transform: capitalize;">{{item.objType}}</span> for <a class="green green-hover" href="{{item.scopeHref}}"><span ng-show="!(item.scopeLevel == \'Country\' || item.scopeLevel == \'Postalcode\' || item.scopeLevel == \'County\')">{{item.scopeLevel}} of</span> {{item.scopeName}} <span ng-show="item.scopeLevel == \'County\'"> {{item.scopeLevel}}</span></a>\n        <span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span>\n        <span ng-if="item.parentObjType && !(item.parentObjType == \'\')">\n            in <a ng-href="{{item.parentHref}}" class="green green-hover">{{item.parentTitle}}</a>\n        </span>\n    </small>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_discussion_listing(context):
    context.caller_stack._push_frame()
    try:
        def upDownVoteBlock():
            return render_upDownVoteBlock(context)
        def moreLess():
            return render_moreLess(context)
        def actions():
            return render_actions(context)
        def metaData():
            return render_metaData(context)
        __M_writer = context.writer()
        # SOURCE LINE 79
        __M_writer(u'\n    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=\'discussion\'">\n        <div class="row-fluid" ng-controller="yesNoVoteCtrl">\n            <div class="span11 media-body">\n                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>\n                <p><small>')
        # SOURCE LINE 84
        __M_writer(escape(metaData()))
        __M_writer(u'</small></p>\n                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>')
        # SOURCE LINE 85
        __M_writer(escape(moreLess()))
        __M_writer(u'</p>\n            </div>\n            <div class="span1 voteWrapper">\n                ')
        # SOURCE LINE 88
        __M_writer(escape(upDownVoteBlock()))
        __M_writer(u'\n            </div>\n        </div>\n        <div class="row-fluid">\n            ')
        # SOURCE LINE 92
        __M_writer(escape(actions()))
        __M_writer(u'\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


