<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="basic_listing()">
    <td class="avatar-cell"><div ng-if="item.thumbnail" class="i-photo small-i-photo" style="background-image:url('{{item.thumbnail}}');"/></div></td>
    <td><a href="{{item.href}}">{{item.title}}</a> | {{item.objType}} | deleted by: {{item.unpublishedBy}}</td>
</%def>

<%def name="meeting_listing()">
    <div class="media well search-listing">
        <div class="row-fluid">
            <div class="span2"><img src="{{item.flag}}" width="60" height="60"></div><div class="span9">{{item.scopeLevel}} of {{item.scopeName}}</div>
        </div><!-- row-fluid -->
        <div class="row-fluid">
            <div class="span2">
                <strong>{{item.meetingDate}}</strong>
                <p><strong>{{item.meetingTime}}</strong></p>
            </div>
            <div class="span9">
                <a href="{{item.href}}">{{item.title}}</a>
                <p>Public Meeting of {{item.group}}</p>
                <p>{{item.location}}</p>
                <p><a href="{{item.href}}">View, vote and comment on agenda items.</a></p>
            </div>
        </div><!-- row-fluid -->
    </div><!-- media-well -->
</%def>

<%def name="agenda_item_listing()">
    <div style="margin-top: 30px;"></div>
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode; url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; canVote=item.canVote; canComment=item.canComment; revisions = item.revisions; revisionList = item.revisionList; canEdit = item.canEdit">
        <div class="row-fluid" ng-controller="yesNoVoteCtrl">
            <div class="well yesNoWell" ng-show="(canVote == 'checked')">
                ${yesNoVoteBlock()}
            </div>
            <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
            <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
        </div><!-- row-fluid -->
        <div class="row-fluid">
            <div class="btn-group">
                <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#edit-{{urlCode}}">Edit</button>
                <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">trash</a>
            </div>
            <div id="edit-{{urlCode}}" class="collapse">
                <form action="/agendaitem/{{urlCode}}/{{url}}/editHandler" method="POST">
                    <fieldset>
                        <label>Item Title</label>
                        <input type="text" name="agendaItemTitle" class="span6" value="{{item.title}}" class="span9">
                        <label>Item Text</label>
                        ${lib_6.formattingGuide()}<br>
                        <textarea rows="3" name="agendaItemText" class="span6" class="span9">{{item.text}}</textarea>
                        <label class="checkbox">
                        <input type="checkbox" name="agendaItemVote" ng-show="(canVote == '')">
                        <input type="checkbox" name="agendaItemVote" checked ng-show="(canVote == 'checked')">
                        People can vote on this
                        </label>
                        <label class="checkbox">
                        <input type="checkbox" name="agendaItemComment" ng-show="(canComment == '')">
                        <input type="checkbox" name="agendaItemComment" checked ng-show="(canComment == 'checked')">
                        People can comment on this
                        </label>
                        <button class="btn btn-success" type="submit" class="btn">Save Item</button>
                    </fieldset>
                </form>
            </div>
            <div id="unpublish-{{urlCode}}" class="collapse" >
                <div class="alert">
                    <strong>Are you sure you want to send this meeting agenda item to the trash?</strong>
                    <br />
                    <a href="/unpublish/agendaitem/{{urlCode}}" class="btn btn-danger">Yes</a>
                    <a class="btn accordion-toggle" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">No</a>
                    <span id = "unpublish_{{urlCode}}"></span>
                </div>
            </div>
            <div class="accordion" id="revisions">
                <div ng-repeat="rev in revisionList">
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#revisions" href="#rev-{{rev.urlCode}}">
                            Revision: {{rev.date}}
                            </a>
                        </div><!-- accordian-heading -->
                        <div id="rev-{{rev.urlCode}}" class="accordion-body collapse">
                            <div class="accordion-inner">
                                <h4>{{rev.title}}</h4>
                                <span ng-bind-html="rev.html"></span>
                            </div><!-- accordian-inner -->
                        </div><!-- accordian-body -->
                    </div><!-- accordian-group -->
                </div><!-- ng-repeat -->
            </div><!-- accordian -->
        </div>
        <div class="row-fluid" ng-show="(canComment == 'checked')">
            ${actions()}
        </div>
    </div>
</%def>

<%def name="initiative_listing()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl"> 
            <div class="row-fluid">
                <div class="span3">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
                        </a>
                    </div>
                </div>
                <div class="span9">
                    <div class="well yesNoWell" >
                        ${yesNoVoteBlock()}
                    </div>
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
                ${actions()}
            </div>
        </div>
    </div>
</%def>

<%def name="idea_listing()">
        <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
            <div class="media-body row-fluid" ng-controller="yesNoVoteCtrl">
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
                    <div class="span9">
                % else:
                    <div class="span12">
                % endif
                    <div class="well yesNoWell" >
                        ${yesNoVoteBlock()}
                    </div>
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    % if not c.w:
                        <p><small>${metaData()}</small></p>
                    % endif
                    <strong ng-if="item.status == 'adopted'" class="green"><i class="icon-star"></i> Adopted</strong>
                    <strong ng-if="item.status == 'disabled'" class="red"><i class="icon-flag"></i> Disabled</strong>
                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                </div>
            </div><!-- media-body -->
            <div class="row-fluid">
                ${actions()}
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
    <small><img class="thumbnail flag mini-flag border" src="{{item.flag}}"> 
        <span style="text-transform: capitalize;">{{item.objType}}</span> for <a class="green green-hover" href="{{item.scopeHref}}"><span ng-show="!(item.scopeLevel == 'Country' || item.scopeLevel == 'Postalcode' || item.scopeLevel == 'County')">{{item.scopeLevel}} of</span> {{item.scopeName}} <span ng-show="item.scopeLevel == 'County'"> {{item.scopeLevel}}</span></a>
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
    % if not c.searchQuery:
    <div class="actions" ng-init="type = item.objType; discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; submit = 'reply'; numComments = item.numComments;">
        <div ng-controller="commentsController">
            <div class="actions-links">
                <ul class="horizontal-list iconListing">
                    <li>
                        <a ng-show="item.numComments == '0'" class="no-highlight" ng-click="showAddComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                        <a ng-show="!(item.numComments == '0')" class="no-highlight" ng-click="getComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                    </li>
                    <li ng-show="!(type == 'agendaitem')"><i class="icon-eye-open"></i> Views ({{item.views}})</li>
                </ul>
            </div>
            ### Comments
            <div class="centered" ng-show="commentsLoading" ng-cloak>
                <i class="icon-spinner icon-spin icon-2x bottom-space-med"></i>
            </div>

            <table class="activity-comments" ng-class="{hidden : commentsHidden}">
                <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == 'yes', con : comment.commentRole == 'no', neutral : comment.commentRole == 'neutral'}">

                    <td class="comment-avatar-cell">
                        <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">
                    </td>
                    <td style="padding: 10px;">
                        <small><a class="no-highlight" ng-href="{{comment.authorHref}}"><strong>{{comment.authorName}}</strong></a><span class="date">{{comment.date}} ago</span></small>
                        <br>
                        <p ng-init="stringLimit=300"><span ng-bind-html="comment.html | limitTo:stringLimit"></span>${moreLessComment()}</p>
                        <div class="accordion" id="revisions">
                            <div ng-repeat="rev in comment.revisionList">
                                <div class="accordion-group">
                                    <div class="accordion-heading">
                                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#revisions" href="#rev-{{rev.urlCode}}">
                                        Revision: {{rev.date}}
                                        </a>
                                    </div><!-- accordian-heading -->
                                    <div id="rev-{{rev.urlCode}}" class="accordion-body collapse">
                                        <div class="accordion-inner">
                                            <p>Position: {{rev.role}}</p>
                                            Comment: <span ng-bind-html="rev.html"></span>
                                        </div><!-- accordian-inner -->
                                    </div><!-- accordian-body -->
                                </div><!-- accordian-group -->
                            </div><!-- ng-repeat -->
                        </div><!-- accordian -->
                        <div ng-show="(comment.canEdit == 'yes')">
                            <div class="btn-group">
                                <button type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-mini" data-toggle="collapse" data-target="#edit-{{comment.urlCode}}">Edit</button>
                            </div><!-- btn-group -->
                            <div id="edit-{{comment.urlCode}}" class="collapse">
                                <div ng-controller="commentEditController" ng-init="urlCode = comment.urlCode; commentEditText = comment.text; commentEditRole = comment.commentRole;">
                                    <form class="no-bottom" ng-submit="submitEditComment()">
                                        <textarea class="span10" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
                                        <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>
                                        <div ng-show="(comment.doCommentRole == 'yes')">
                                            &nbsp;
                                            <label class="radio inline">
                                                <input type="radio" name="commentRole-{{comment.urlCode}}" value="yes" ng-model="commentEditRole"> Pro
                                            </label>
                                            <label class="radio inline">
                                                <input type="radio" name="commentRole-{{comment.urlCode}}" value="neutral" ng-model="commentEditRole"> Neutral
                                            </label>
                                            <label class="radio inline">
                                                <input type="radio" name="commentRole-{{comment.urlCode}}" value="no" ng-model="commentEditRole"> Con
                                            </label>
                                        </div><!-- ng-show -->
                                    </form>
                                </div><!-- controller -->
                            </div><!-- collapse -->
                        </div><!-- ng-show -->
                    </td>
                    <td class="span1 voteWrapper">
                        <div class="row-fluid" ng-init="objType='comment'; rated=comment.rated; urlCode=comment.urlCode; totalVotes=comment.voteCount; yesVotes=comment.ups; noVotes=comment.downs; netVotes=comment.netVotes">
                            <div ng-controller="yesNoVoteCtrl">
                                ${upDownVoteBlock()}
                            </div>
                        </div>
                    </td>
                </tr>
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
                        <td style="padding: 10px;">
                            % if c.privs and not c.privs['provisional']:
                                <form class="no-bottom" ng-submit="submitComment()">
                                    <textarea class="span10" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>
                                    <div ng-show="type == 'initiative' || type == 'idea' || type == 'agendaitem'">
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
                                    <textarea class="span10" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    <a href="#activateAccountModal" data-toggle='modal' class="btn btn-success" style="vertical-align: top;">Submit</a>
                                </a>
                            % endif
                        </td>
                    % else:
                        <td class="comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar small-avatar"></td>
                        <td style="padding: 10px;">
                            <form class="no-bottom" ng-submit="submitComment()">
                                <a href="#signupLoginModal" data-toggle='modal'>
                                    <textarea class="span10" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    <button type="submit" class="btn btn-success" style="vertical-align: top;">Submit</button>
                                </a>
                                <div ng-show="type == 'initiative' || type == 'idea' || type == 'agendaitem' ">
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
        </div><!-- comments controller -->
    </div><!-- action -->
    % endif
</%def>