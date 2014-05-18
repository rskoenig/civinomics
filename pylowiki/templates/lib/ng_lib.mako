<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="basic_listing()">
    <td class="avatar-cell"><div ng-if="item.thumbnail" class="i-photo small-i-photo" style="background-image:url('{{item.thumbnail}}');"/></div></td>
    <td><a href="{{item.href}}">{{item.title}}</a> | {{item.objType}} | deleted by: {{item.unpublishedBy}}</td>
</%def>

<%def name="initiative_listing()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
        <div ng-controller="yesNoVoteCtrl"> 
            ${authorPosting()}
            <div class="row" style="margin-top:19px;">
                <div class="col-sm-3">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
                        </a>
                    </div>
                </div>
                <div class="col-sm-9 no-left">
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p><small>${metaData()}</small></p>
                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                    <p><strong>
                        <span ng-if="item.cost >= 0" class="grey centered">Net Cost:</span>
                        <span ng-if="item.cost < 0" class="grey centered">Net Savings:</span>
                        <span class="pull-right">{{(item.cost | currency).replace(".00", "")}}</span>
                    </strong></p>
                </div>
            </div>
            <div class="row">
                ${yesNoVoteFooter()}
                ${actions()}
            </div>
        </div>
    </div>
</%def>

<%def name="initiative_listing_condensed()">
    <div class="media well search-listing initiative-listing" style="height: 415px;" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl"> 
            <div class="row">
                <div class="col-sm-12">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo full-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                        </a>
                    </div>
                </div>
                <div class="col-sm-12" style="height: 155px;">
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p style="line-height: 16px;"><small>${metaData()}</small></p>
                    <!--
                    <p ng-init="stringLimit=300"><small><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</small></p>
                    -->
                    <h4>
                        <small class="grey centered">Estimated Cost:</small>
                        <span class="pull-right">{{item.cost | currency}}</span>
                    </h4>
                </div>
            </div>
            <div class="row">
                ${yesNoVoteFooter(noStats = True)}
            </div>
        </div>
    </div>
</%def>

<%def name="idea_listing()">
        <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
            ${authorPosting()}
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
        <div class="row" ng-controller="yesNoVoteCtrl">
            <div class="col-xs-11">
                <p>${authorPosting()}</p>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}" target="_blank">{{item.title}} <small>({{item.link}})</small></a> ${metaData()}</h4>
            </div>
            <div class="col-xs-1">
                ${upDownVoteBlock()}
            </div>
        </div>
        <div class="row">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="discussion_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType='discussion'">
        ${authorPosting()}
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
        ${authorPosting()}
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
        <div class="form-group">
            <a ng-click="updateYesVote()" class="btn btn-lg btn-block btn-success btn-vote {{voted}}">YES</a>
            <a ng-click="updateNoVote()" class="btn btn-lg btn-block btn-danger btn-vote {{voted}}">NO</a>
            <br>
            <div ng-cloak>
                <small class="grey">{{totalVotes}} votes <span ng-show="voted">| <span class="green">{{yesPercent | number:0}}% YES</span> | <span class="red">{{noPercent | number:0}}% NO</span></span></small> 
                <div class="progress" style="height: 12px; margin-bottom: 5px;">
                    <div class="progress-bar" role="progress-bar" style="width: {{100 * totalVotes / goal | number:0}}%;"></div>
                </div>
                <small ng-if="item.goal == 100" class="grey pull-right clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes needed for this initiative to advance.">{{goal - totalVotes | number:0}} NEEDED</small>
                <small ng-if="!(item.goal == 100)" class="grey pull-right clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{goal - totalVotes | number}} NEEDED</small>
            </div>
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
                <span class="totalVotes">{{totalVotes}} <span ng-if="goal">of {{goal - totalVotes | number}} NEEDED</span></span>
            </strong>
        </div>
    % endif
</%def>

<%def name="yesNoVoteFooter(**kwargs)">
    <div class="actions centered" style="padding:10px; padding-bottom: 10px;">
        % if 'user' in session:
            <div class="row centered">
                <div class="col-sm-12">
                    <a ng-click="updateYesVote()" class="btn btn-lg btn-success btn-vote {{voted}}">YES</a>
                    <a ng-click="updateNoVote()" class="btn btn-lg btn-danger btn-vote {{voted}}">NO</a>
                </div>
            </div>
            % if not 'noStats' in kwargs:
                <div class="row text-center" style="margin: 0 19px;">
                        <!--
                        <div class="progress col-sm-8">
                          <div class="progress-bar progress-bar-success" style="width: {{100 * yesVotes / 3 | number:0}}%">
                            <span class="sr-only">{{100 * yesVotes / 3 | number:0}}% Complete (success)</span>
                          </div>
                          <div class="progress-bar progress-bar-danger" style="width: {{100 * noVotes / 3 | number:0}}%">
                            <span class="sr-only">{{100 * noVotes / 3 | number:0}}% Complete (danger)</span>
                          </div>
                        -->
                        <div class="col-sm-12">
                            <small class="grey">
                                {{totalVotes}} votes, <span class="grey " tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{item.goal - item.voteCount | number}} NEEDED </span>
                                <span ng-show="voted">| <span class="green">{{yesPercent | number:0}}% YES</span> | <span class="red">{{noPercent | number:0}}% NO</span></span>
                            </small>
                        </div>
                    </div>
                </div>
            % endif
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
    <small>
        <span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span>
        <img class="thumbnail flag mini-flag border no-bottom" src="{{item.flag}}"> 
        <a style="text-transform: capitalize;" href="{{item.scopeHref}}"><span ng-show="!(item.scopeLevel == 'Country' || item.scopeLevel == 'Postalcode' || item.scopeLevel == 'County')">{{item.scopeLevel}} of</span> {{item.scopeName}} <span ng-show="item.scopeLevel == 'County'"> {{item.scopeLevel}}</span></a>
    </small>
</%def>

<%def name="authorPosting()">
    <img class="avatar small-avatar inline" ng-src="{{item.authorPhoto}}" alt="{{item.authorName}}" title="{{item.authorName}}">
    <small>
        <a href="{{item.authorHref}}" class="green green-hover">{{item.authorName}}</a> 
        <span class="date">{{item.fuzzyTime}} ago</span>
    </small>
</%def>

<%def name="actions()">
    <div class="actions" ng-init="type = item.objType; discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; submit = 'reply'; numComments = item.numComments;">
        <div ng-controller="commentsController">
            ### Comments
            
            <table class="activity-comments">

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

                <tr class="centered" ng-show="commentsLoading" ng-cloak>
                    <td></td>
                    <td><i class="icon-spinner icon-spin icon-2x bottom-space-med"></i></td>
                </tr>

                <tr ng-show="newCommentLoading" ng-cloak>
                    <td></td>
                    <td>
                        <div class="centered">
                            <i class="icon-spinner icon-spin icon-2x"></i>
                        </div>
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

                <tr ng-hide="newCommentLoading || commentsHidden">
                    % if c.authuser:
                        <td class="col-xs-1 comment-avatar-cell">${lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")}</td>
                        <td class="col-xs-11" style="padding: 10px 0px;">
                            % if c.privs and not c.privs['provisional']:
                                <form class="no-bottom form-inline" ng-submit="submitComment()">
                                    <div class="form-group col-sm-10 text-right" style="margin-left: 0; padding-left:0;">
                                        <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>

                                        <small class="left-space" ng-show="type == 'initiative' || type == 'idea'">
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="yes"> Pro 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="neutral"> Neutral 
                                            </span>
                                            <span class="radio inline no-top right-space">
                                                <input type="radio" name="commentRole" ng-model="commentRole" value="no"> Con 
                                            </span>
                                        </small>
                                        
                                    </div>
                                    <div class="form-group">
                                        <button type="submit" class="btn btn-primary">Submit</button>
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
                
            </table>

        </div>
    </div>
</%def>