<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="basic_listing()">
    <td class="avatar-cell"><div ng-if="item.thumbnail" class="i-photo small-i-photo" style="background-image:url('{{item.thumbnail}}');"/></div></td>
    <td><a href="{{item.href}}">{{item.title}}</a> | {{item.objType}} | deleted by: {{item.unpublishedBy}}</td>
</%def>

<%def name="meeting_listing()">
    <div class="media well search-listing">
        <div class="row">
            <div class="col-xs-2"><img class="thumbnail med-flag" src="{{item.flag}}"></div><div class="col-xs-9">{{item.scopeLevel}} of {{item.scopeName}}</div>
        </div><!-- row -->
        <div class="row">
            <div class="col-xs-2">
                <strong>{{item.meetingDate}}</strong>
                <p><strong>{{item.meetingTime}}</strong></p>
            </div>
            <div class="col-xs-9">
                <a href="{{item.href}}">{{item.title}}</a>
                <p>Public Meeting of {{item.group}}</p>
                <p>{{item.location}}</p>
                <p ng-show="(item.agendaItemCount != '0')"><a href="{{item.href}}">View, vote and comment on agenda items.</a></p>
                <p ng-show="(item.agendaItemCount == '0' && item.agendaPostDate != '')">Agenda posted: {{item.agendaPostDate}}</p>
            </div>
        </div><!-- row -->
    </div><!-- media-well -->
</%def>

<%def name="agenda_item_listing()">
    <div style="margin-top: 30px;"></div>
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode; url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; canVote=item.canVote; canComment=item.canComment; revisions = item.revisions; revisionList = item.revisionList; canEdit = item.canEdit">
        <div class="row">
            <div class="col-xs-12">
                <h4 class="listed-item-title">{{item.title}}</h4>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
            </div>
        </div><!-- row -->
        <div class="row">
            <div class="col-xs-12">
                <div class="btn-group">
                    <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-default btn-xs" data-toggle="collapse" data-target="#edit-{{urlCode}}">Edit</button>
                    <button type="button" ng-show="(canEdit == 'yes')" class="btn btn-default btn-xs" data-toggle="collapse" data-target="#unpublish-{{urlCode}}">trash</a>
                </div>
                <div id="edit-{{urlCode}}" class="collapse">
                    <form action="/agendaitem/{{urlCode}}/{{url}}/editHandler" method="POST">
                        <fieldset>
                            <label>Item Title</label>
                            <input type="text" name="agendaItemTitle" class="col-xs-6" value="{{item.title}}" class="col-xs-9" required>
                            <label>Item Text</label>
                            ${lib_6.formattingGuide()}<br>
                            <textarea rows="3" name="agendaItemText" class="col-xs-9 form-control" required>{{item.text}}</textarea>
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
        </div>
        <div ng-controller="yesNoVoteCtrl" class="row" ng-show="(canVote == 'checked')">
                ${yesNoVoteFooter()}
            </div>
        <div class="row" ng-show="(canComment == 'checked')">
            ${actions()}
        </div>
    </div>
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
    <div class="media well search-listing initiative-listing" style="height: 415px;" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
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
    <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType; goal=item.goal">
        <div ng-controller="yesNoVoteCtrl">
            ${authorPosting()}
            <div class="row" style="margin-top:19px;">
                <div class="col-sm-12">
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    % if not c.w:
                        <p><small>${metaData()}</small></p>
                    % endif
                    <strong ng-if="item.status == 'adopted'" class="green"><i class="icon-star"></i> Adopted</strong>
                    <strong ng-if="item.status == 'disabled'" class="red"><i class="icon-flag"></i> Disabled</strong>
                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                </div>
            </div>
            <div class="row">
                ${yesNoVoteFooter()}
                ${actions()}
            </div>
    </div><!-- media well -->
</%def>

<%def name="resource_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl">
            <div class="row">
                <div class="col-xs-11">
                    <p>${authorPosting()}</p>
                    <h4 class="listed-item-title"><a ng-href="{{item.href}}" target="_blank">{{item.title}} <small>({{item.link}})</small></a></h4>
                    % if not c.w:
                        <p><small>${metaData()}</small></p>
                    % endif
                </div>
                <div class="col-xs-1">
                    ${upDownVoteBlock()}
                </div>
            </div>
            <div class="row">
                ${actions()}
            </div>
        </div>
    </div>
</%def>

<%def name="discussion_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType='discussion'">
        <div class="row" ng-controller="yesNoVoteCtrl">
            <div class="col-xs-11 media-body">
                <p>${authorPosting()}</p>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}" target="_blank">{{item.title}} <small></small></a></h4>
                % if not c.w:
                    <p><small>${metaData()}</small></p>
                % endif
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
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

<%def name="photo_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        ${authorPosting()}
        <div class="row" ng-controller="yesNoVoteCtrl">
            <div class="col-xs-11 media-body">
                <div class="listed-photo">
                    <a href = '{{item.href}}'>
                        <div class="main-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                    </a>
                </div>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                <p><small>${metaData()}</small></p>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
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

<%def name="yesNoVoteBlock()">
    <div class="form-group">
        % if 'user' in session:
        
            <a ng-click="updateYesVote()" class="btn btn-lg btn-block btn-success btn-vote {{voted}}">YES</a>
            <a ng-click="updateNoVote()" class="btn btn-lg btn-block btn-danger btn-vote {{voted}}">NO</a>

        % else:
            <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-block btn-success btn-vote {{voted}}">YES</a>
            <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-block btn-danger btn-vote {{voted}}">NO</a>
        % endif
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
        % else:
            <div class="row centered">
                <div class="col-sm-12">
                    <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-success btn-vote {{voted}}">YES</a>
                    <a href="#signupLoginModal" role="button" data-toggle="modal" class="btn btn-lg btn-danger btn-vote {{voted}}">NO</a>
                </div>
            </div>
        % endif
        % if not 'noStats' in kwargs:
            <div class="row text-center" style="margin: 0 19px;">
                <!-- multi-colored progress bar test
                <div class="progress col-sm-8">
                    <div class="progress-bar progress-bar-success" style="width: {{100 * yesVotes / 3 | number:0}}%">
                        <span class="sr-only">{{100 * yesVotes / 3 | number:0}}% Complete (success)</span>
                    </div>
                    <div class="progress-bar progress-bar-danger" style="width: {{100 * noVotes / 3 | number:0}}%">
                        <span class="sr-only">{{100 * noVotes / 3 | number:0}}% Complete (danger)</span>
                    </div>
                </div>
                -->
                <div class="col-sm-12">
                    <small class="grey">
                        {{totalVotes}} votes<span ng-if="item.goal">, <span class="grey " tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{item.goal - item.voteCount | number}} NEEDED</span> </span>
                        <span ng-show="voted">| <span class="green">{{yesPercent | number:0}}% YES</span> | <span class="red">{{noPercent | number:0}}% NO</span></span>
                    </small>
                </div>
            </div>
        % endif
    </div>
</%def>

<%def name="upDownVoteBlock()"> 
    <div class="text-center" >
    % if 'user' in session:
        <a ng-click="updateYesVote()" class="upVote {{voted}}">
            <i class="icon-chevron-sign-up icon-2x {{voted}}"></i>
        </a>
        <br>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a ng-click="updateNoVote()" class="downVote {{voted}}">
            <i class="icon-chevron-sign-down icon-2x {{voted}}"></i>
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
    </div>
    <br>
</%def>

<%def name="moreLess()">
    <a class="green green-hover" ng-show="item.text.length > 200 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{item.urlCode}}" class="green green-hover"  ng-show="item.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="moreLessComment()">
    <a class="green green-hover" ng-show="comment.text.length > 200 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{comment.urlCode}}" class="green green-hover"  ng-show="comment.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="metaData()">
    <small>
        <span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span>
        <img class="thumbnail flag mini-flag border no-bottom" src="{{item.flag}}"> 
        <a style="text-transform: capitalize;" ng-href="{{item.scopeHref}}">{{item.scopeName}}</span></a>
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
    % if not c.searchQuery:
        <div class="actions" ng-init="type = item.objType; discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; submit = 'reply'; numComments = item.numComments;">
            <div ng-controller="commentsController">
                <div class="row">
                    <div class="col-xs-12 icon-listing-row">
                        <ul class="horizontal-list iconListing">
                            <li>
                                <a ng-show="item.numComments == '0'" class="no-highlight" ng-click="showAddComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                                <a ng-show="!(item.numComments == '0')" class="no-highlight" ng-click="getComments()"><i class="icon-comments"></i> Comments ({{numComments}})</a>
                            </li>
                            <li><i class="icon-eye-open"></i> Views ({{item.views}})</li>
                        </ul>
                    </div>
                </div>
                ### Comments
                <table class="activity-comments">


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

                    <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == 'yes', con : comment.commentRole == 'no', neutral : comment.commentRole == 'neutral', hidden : commentsHidden}" class="comment-row">

                        <td class="comment-avatar-cell">
                            <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">
                        </td>
                        <td class="comment-main-cell">
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
                                <div class="btn-group btn-group-xs">
                                    <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#edit-{{comment.urlCode}}">Edit</button>
                                    <!-- <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#unpublish-{{comment.urlCode}}">Trash</button> -->
                                </div><!-- btn-group -->
                                <div id="edit-{{comment.urlCode}}" class="collapse">
                                    <div ng-controller="commentEditController" ng-init="urlCode = comment.urlCode; commentEditText = comment.text; commentEditRole = comment.commentRole;">
                                        <form class="no-bottom" ng-submit="submitEditComment()">
                                            <textarea class="col-xs-10 form-control" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
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
                        <td class="col-xs-1 comment-vote">
                            <div class="row" ng-init="objType='comment'; rated=comment.rated; urlCode=comment.urlCode; totalVotes=comment.voteCount; yesVotes=comment.ups; noVotes=comment.downs; netVotes=comment.netVotes">
                                <div ng-controller="yesNoVoteCtrl">
                                    ${upDownVoteBlock()}
                                </div>
                            </div>
                        </td>
                    </tr>

                    <tr ng-hide="newCommentLoading || commentsHidden">
                        % if c.authuser:
                            <td class="comment-avatar-cell">${lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")}</td>
                            <td class="col-xs-10" style="padding: 10px 0px;">
                                <form class="no-bottom form-inline" ng-submit="submitComment()">
                                    <div class="form-group col-sm-10 text-right" style="margin-left: 0; padding-left:0;">
                                        % if c.privs and not c.privs['provisional']:
                                            <textarea class="form-control new-comment"  rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                        % else:
                                            <a href="#activateAccountModal" data-toggle='modal'>
                                            <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea></a>
                                        % endif

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
                                        % if c.privs and not c.privs['provisional']:
                                            <button type="submit" class="btn btn-primary">Submit</button>
                                        % else:
                                            <a href="#activateAccountModal" data-toggle='modal' class="btn btn-primary">Submit</a>
                                        % endif
                                    </div>
                                </form>
                            </td>
                        % else:
                        <!-- if not c.authuser -->
                            <td class="col-xs-1 comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar topbar-avatar"></td>
                            <td class="col-xs-11" style="padding: 10px;">
                                <a href="#signupLoginModal" data-toggle='modal' class="no-highlight no-hover">
                                    <form class="no-bottom" ng-submit="submitEditComment()">
                                            <div class="form-group">
                                                <textarea class="col-xs-10 form-control" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
                                            </div>
                                            <div class="form-group">
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
                                            </div>
                                        </form>
                            </td>
                        % endif
                        <td></td>
                    </tr>
                    
                </table>
            </div>
        </div>
    % endif
</%def>

<%def name="actions2()">
    
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
                                <div class="btn-group btn-group-xs">
                                    <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#edit-{{comment.urlCode}}">Edit</button>
                                    <!-- <button class="btn btn-default" type="button" ng-show="(comment.canEdit == 'yes')" class="btn btn-xs" data-toggle="collapse" data-target="#unpublish-{{comment.urlCode}}">Trash</button> -->
                                </div><!-- btn-group -->
                                <div id="edit-{{comment.urlCode}}" class="collapse">
                                    <div ng-controller="commentEditController" ng-init="urlCode = comment.urlCode; commentEditText = comment.text; commentEditRole = comment.commentRole;">
                                        <form class="no-bottom" ng-submit="submitEditComment()">
                                            <div class="form-group">
                                                <textarea class="col-xs-10 form-control" ng-model="commentEditText" name="data">{{comment.text}}</textarea>
                                            </div>
                                            <div class="form-group">
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
                                            </div>
                                        </form>
                                    </div><!-- controller -->
                                </div><!-- collapse -->
                            </div><!-- ng-show -->
                        </td>
                        <td class="col-xs-1 comment-vote">
                            <div class="row" ng-init="objType='comment'; rated=comment.rated; urlCode=comment.urlCode; totalVotes=comment.voteCount; yesVotes=comment.ups; noVotes=comment.downs; netVotes=comment.netVotes">
                                <div ng-controller="yesNoVoteCtrl">
                                    ${upDownVoteBlock()}
                                </div>
                            </div>
                        </td>
                </tr>

                <tr ng-hide="newCommentLoading || commentsHidden">
                    % if c.authuser:
                        <td class="col-xs-1 comment-avatar-cell">${lib_6.userImage(c.authuser, className="media-object avatar small-avatar", linkClass="topbar-avatar-link")}</td>
                        <td class="col-xs-11" style="padding: 10px 0px;">
                            <form class="no-bottom form-inline" ng-submit="submitComment()">
                                <div class="form-group col-sm-10 text-right" style="margin-left: 0; padding-left:0;">
                                    % if c.privs and not c.privs['provisional']:
                                        <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
                                    % else:
                                        <a href="#activateAccountModal" data-toggle='modal'>
                                        <textarea class="form-control" style="width: 100%;" rows="1" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea></a>
                                    % endif

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
                                    % if c.privs and not c.privs['provisional']:
                                        <button type="submit" class="btn btn-primary">Submit</button>
                                    % else:
                                        <a href="#activateAccountModal" data-toggle='modal' class="btn btn-primary">Submit</a>
                                    % endif
                                </div>
                            </form>
                        </td>
                    % else:
                        <td class="col-xs-1 comment-avatar-cell"><img src="/images/hamilton.png" class="media-object avatar topbar-avatar"></td>
                        <td class="col-xs-11" style="padding: 10px;">
                            <a href="#signupLoginModal" data-toggle='modal' class="no-highlight no-hover">
                                <form class="no-bottom form-inline">
                                    <div class="form-group col-sm-10">
                                        <textarea rows="1" class="form-control" style="width:100%" ng-submit="submitComment()" name="commentText" ng-model="commentText" placeholder="Add a comment..."></textarea>
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
                        </td>
                    % endif
                </tr>
                
            </table>
</%def>