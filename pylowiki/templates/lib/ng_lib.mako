<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="basic_listing()">
    <td class="avatar-cell"><div ng-if="item.thumbnail" class="i-photo small-i-photo" style="background-image:url('{{item.thumbnail}}');"/></div></td>
    <td><a href="{{item.href}}">{{item.title}}</a> | {{item.objType}} | deleted by: {{item.unpublishedBy}}</td>
</%def>

<%def name="initiative_listing()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl"> 
            <div class="row-fluid">
                <div class="span2">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
                        </a>
                    </div>
                </div>
                <div class="span10">
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p><small>${metaData()}</small></p>
                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                    <h4>
                        <small class="grey centered">Estimated Cost:</small>
                        <span class="pull-right">{{item.cost | currency}}</span>
                    </h4>
                </div>
            </div>
            <div class="row-fluid">
                ${yesNoVoteFooter()}
                ${actions()}
            </div>
        </div>
    </div>
</%def>

<%def name="initiative_listing_condensed()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl"> 
            <div class="row-fluid">
                <div class="span2">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo full-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                        </a>
                    </div>
                </div>
                <div class="span10">
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p style="line-height: 16px;"><small>${metaData()}</small></p>
                    <small style="grey" ng-init="stringLimit=200"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</small>
                    <h4>
                        <small class="grey centered">Estimated Cost:</small>
                        <span class="pull-right">{{item.cost | currency}}</span>
                    </h4>
                </div>
            </div>
            <div class="row-fluid">
                ${yesNoVoteFooter()}
                ${actions()}
            </div>
        </div>
    </div>
</%def>

<%def name="idea_listing()">
        <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
            <div class="media-body row" ng-controller="yesNoVoteCtrl">
                % if not c.w:
                    <div class="col-sm-3">
                        <div class="listed-photo">
                            <a href = '{{item.parentHref}}'>
                                <div class="i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
                            </a>
                        </div>
                    </div>
                % endif
                % if not c.w:
                    <div class="col-sm-9">
                % else:
                    <div class="col-sm-12">
                % endif
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    % if not c.w:
                        <p><small>${metaData()}</small></p>
                    % endif
                    <strong ng-if="item.status == 'adopted'" class="green"><i class="icon-star"></i> Adopted</strong>
                    <strong ng-if="item.status == 'disabled'" class="red"><i class="icon-flag"></i> Disabled</strong>
                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                    ${authorPosting()}
                </div>
            </div><!-- media-body -->
            <div class="row">
                <div class="col-xs-12">
                ${yesNoVoteFooter()}
                ${actions()}
                </div>
            </div>
        </div><!-- search-listing -->
</%def>

<%def name="resource_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div class="row-fluid" ng-controller="yesNoVoteCtrl">
            % if not c.w:
                <div class="span3">
                    <div class="listed-photo">
                        <a href = '{{item.parentHref}}'>
                            <div class="i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
                        </a>
                    </div>
                </div>
            % endif
            % if not c.w:
                <div class="span8">
            % else:
                <div class="span11 media-body">
            % endif
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                % if not c.w:
                    <p><small>${metaData()}</small></p>
                % endif
                <p><a class="break" href="{{item.link}}" target="_blank">{{item.link}}</a><p>
            </div>
            <div class="span1 voteWrapper">
                ${upDownVoteBlock()}
            </div>
        </div>
        <div class="row-fluid">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="discussion_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType='discussion'">
        <div class="row-fluid" ng-controller="yesNoVoteCtrl">
            % if not c.w:
                <div class="span3">
                    <div class="listed-photo">
                        <a href = '{{item.parentHref}}'>
                            <div class="i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
                        </a>
                    </div>
                </div>
            % endif
            % if not c.w:
                <div class="span8">
            % else:
                <div class="span11 media-body">
            % endif
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                % if not c.w:
                    <p><small>${metaData()}</small></p>
                % endif
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
            <div class="span1 voteWrapper">
                ${upDownVoteBlock()}
            </div>
        </div>
        <div class="row-fluid">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="photo_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div class="row-fluid" ng-controller="yesNoVoteCtrl">
            <div class="span11 media-body">
                <div class="listed-photo">
                    <a href = '{{item.href}}'>
                        <div class="main-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                    </a>
                </div>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                <p><small>${metaData()}</small></p>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
            <div class="span1 voteWrapper">
                ${upDownVoteBlock()}
            </div>
        </div>
        <div class="row-fluid">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="yesNoVoteBlock()">
    % if 'user' in session:
        <a ng-click="updateYesVote()" class="yesVote {{yesVoted}}">
            <div class="vote-icon yes-icon detail"></div>
            <div class="ynScoreWrapper"><span class="yesScore {{display}}">{{yesPercent | number:0 }}%</span></div>
        </a>
        <br>
        <br>
        <a ng-click="updateNoVote()" class="noVote {{noVoted}}">
            <div class="vote-icon no-icon detail"></div>
            <div class="ynScoreWrapper"><span class="noScore {{display}}">{{noPercent | number:0 }}%</span></div>
        </a>
        <br>
        <div class="totalVotesWrapper">
            <span class="grey pull-left">Votes:</span>
            <strong class="pull-right">
                <span class="totalVotes">{{totalVotes}}</span>
            </strong>
        </div>
    % else:
        <a href="#signupLoginModal" role="button" data-toggle="modal" class="yesVote">
            <div class="vote-icon yes-icon"></div>
        </a>
        <br>
        <br>
        <a href="#signupLoginModal" role="button" data-toggle="modal" class="noVote">
            <div class="vote-icon no-icon"></div>
        </a>
        <br>
        <div class="totalVotesWrapper">
            <small class="grey pull-left">Votes:</small>
            <strong class="pull-right">
                <span class="totalVotes">{{totalVotes}}</span>
            </strong>
        </div>
    % endif
</%def>

<%def name="yesNoVoteFooter()">
    <div class="actions centered" style="padding:10px; padding-bottom: 10px;">
        <a  href="#" target="_blank" class="btn btn-lg btn-success" style="width:100px;">YES</a>
        <a  href="#" target="_blank" class="btn btn-lg btn-danger" style="width:100px;">NO</a>
    </div>
</%def>

<%def name="upDownVoteBlock()">   
    % if 'user' in session:
        <a ng-click="updateYesVote()" class="upVote {{yesVoted}}">
            <i class="icon-chevron-sign-up icon-2x {{yesVoted}}"></i>
        </a>
        <br>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a ng-click="updateNoVote()" class="downVote {{noVoted}}">
            <i class="icon-chevron-sign-down icon-2x {{noVoted}}"></i>
        </a>
    % else:
        <a href="#signupLoginModal" data-toggle="modal" class="upVote">
            <i class="icon-chevron-sign-up icon-2x"></i>
        </a>
        <br>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a href="#signupLoginModal" data-toggle="modal" class="downVote">
            <i class="icon-chevron-sign-down icon-2x"></i>
        </a>
    % endif
    <br>
</%def>

<%def name="moreLess()">
    <a class="green green-hover" ng-show="item.text.length > 300 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{item.urlCode}}" class="green green-hover"  ng-show="item.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="moreLessComment()">
    <a class="green green-hover" ng-show="comment.text.length > 300 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{comment.urlCode}}" class="green green-hover"  ng-show="comment.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="metaData()">
    <small><img class="thumbnail flag mini-flag border no-bottom" src="{{item.flag}}"> 
        <span style="text-transform: capitalize;"><a class="green green-hover" href="{{item.scopeHref}}"><span ng-show="!(item.scopeLevel == 'Country' || item.scopeLevel == 'Postalcode' || item.scopeLevel == 'County')">{{item.scopeLevel}} of</span> {{item.scopeName}} <span ng-show="item.scopeLevel == 'County'"> {{item.scopeLevel}}</span></a>
        <span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span>
    </small>
</%def>

<%def name="authorPosting()">
    <img class="avatar small-avatar inline" ng-src="{{item.authorPhoto}}" alt="{{item.authorName}}" title="{{item.authorName}}">
    <small>
        <a href="{{item.authorHref}}" class="green green-hover">{{item.authorName}}</a> 
        <span class="date">{{item.fuzzyTime}} ago</span>
        % if not (c.w or c.initiative):
            <span ng-if="item.parentObjType && !(item.parentObjType == '')">
                in <a ng-href="{{item.parentHref}}" class="green green-hover">{{item.parentTitle}}</a>
            </span>
        % endif
    </small>
</%def>

<%def name="actions()">
    <div class="actions" ng-init="type = item.objType; discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; submit = 'reply'; numComments = item.numComments;">
        <div ng-controller="commentsController">
            ### Comments
            <div class="centered" ng-show="commentsLoading" ng-cloak>
                <i class="icon-spinner icon-spin icon-2x bottom-space-med"></i>
            </div>


            <table class="activity-comments">
                <tr ng-show="newCommentLoading" ng-cloak>
                    <td></td>
                    <td>
                        <div class="centered">
                            <i class="icon-spinner icon-spin icon-2x"></i>
                        </div>
                    </td>
                </tr>
                <tr ng-hide="newCommentLoading">
                    % if c.authuser:
                        <td class="comment-avatar-cell">${lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")}</td>
                        <td style="padding: 10px 0px;">
                            % if c.privs and not c.privs['provisional']:
                                <form class="no-bottom" ng-submit="submitComment()">
                                    <div class="form-group col-xs-10">
                                        <textarea class="form-control" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    </div>
                                    <div class="form-group">
                                        <button type="submit" class="btn btn-primary">Submit</button>
                                    </div>
                                    <div ng-show="type == 'initiative' || type == 'idea'">
                                        <label class="radio inline">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="yes"> Pro
                                        </label>
                                        <label class="radio inline">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="neutral"> Neutral
                                        </label>
                                        <label class="radio inline">
                                            <input type="radio" name="commentRole" ng-model="commentRole" value="no"> Con
                                        </label>
                                    </div>
                                </form>
                            % else:
                                <a href="#activateAccountModal" data-toggle='modal'>
                                    <textarea class="form-control col-xs-10" rows="1" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    <a href="#activateAccountModal" data-toggle='modal' class="btn btn-success" style="vertical-align: top;">Submit</a>
                                </a>
                            % endif
                        </td>
                    % else:
                        <td class="comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar topbar-avatar"></td>
                        <td style="padding: 10px;">
                            <form class="no-bottom" ng-submit="submitComment()">
                                <div class="form-group col-xs-10">
                                    <a href="#signupLoginModal" data-toggle='modal'>
                                        <textarea rows="1" class="form-control" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                        <button type="submit" class="btn btn-primary" style="vertical-align: top;">Submit</button>
                                    </a>
                                </div>
                                <div ng-show="type == 'initiative' || type == 'idea'">
                                    <a href="#signupLoginModal" data-toggle='modal' class="no-highlight no-hover">
                                        <label class="radio inline">
                                            <input type="radio"> Pro
                                        </label>
                                        <label class="radio inline">
                                            <input type="radio"> Neutral
                                        </label>
                                        <label class="radio inline">
                                            <input type="radio"> Con
                                        </label>
                                    </a>
                                </div>
                            </form>
                        </td>
                    % endif
                </tr> 
                
                <tr class="actions-links">
                    <td colspan="2" style="padding: 10px;">
                        <ul class="horizontal-list iconListing">
                            <li>
                                <a ng-show="item.numComments == '0'" class="no-highlight" ng-click="showAddComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                                <a ng-show="!(item.numComments == '0')" class="no-highlight" ng-click="getComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                            </li>
                            <li><i class="icon-eye-open"></i> Views ({{item.views}})</li>
                        </ul>
                    </td>
                </tr>
                
                <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == 'yes', con : comment.commentRole == 'no', neutral : comment.commentRole == 'neutral', hidden : commentsHidden}">

                    <td class="comment-avatar-cell">
                        <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">
                    </td>
                    <td style="padding: 10px;">
                        <small><a class="no-highlight" ng-href="{{comment.authorHref}}"><strong>{{comment.authorName}}</strong></a><span class="date">{{comment.date}} ago</span></small>
                        <br>
                        <p ng-init="stringLimit=300"><span ng-bind-html="comment.html | limitTo:stringLimit"></span>${moreLessComment()}</p>                   
                  </td>
                </tr>
                
            </table>

        </div>
    </div>
</%def>