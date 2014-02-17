
<%def name="initiative_listing()">
    <div class="media well search-listing initiative-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
        <div class="listing-body" ng-controller="yesNoVoteCtrl"> 
            <div class="row-fluid">
                <div class="span12">
                    <div class="listed-photo">
                        <a href = '{{item.href}}'>
                            <div class="i-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                        </a>
                    </div>
                    <div class="well yesNoWell" >
                        ${yesNoVoteBlock()}
                    </div>
                    <h4 class="listed-item-title initiative-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                    <p><small>${metaData()}</small></p>
                    <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                    <hr class="no-bottom no-top">
                    <h4>
                        <small class="grey centered">Estimated Cost:</small>
                        <span class="pull-right">{{item.cost | currency}}</span>
                    </h4>
                    <div>
                        ${stats()}
                    </div>
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="idea_listing()">
        <div class="media well search-listing {{item.status}}" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; objType=item.objType;">
            <div class="media-body" ng-controller="yesNoVoteCtrl">
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
                <div>
                    ${stats()}
                </div>
            </div><!-- media-body -->
        </div><!-- search-listing -->
</%def>

<%def name="resource_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl">
            <div class="span11 media-body">
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                <p><small>${metaData()}</small></p>
                <p><a class="break" href="{{item.link}}" target="_blank">{{item.link}}</a><p>
                <div>
                    ${stats()}
                </div>
            </div>
            <div class="span1 voteWrapper">
                ${upDownVoteBlock()}
            </div>
        </div>
    </div>
</%def>

<%def name="discussion_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType='discussion'">
        <div ng-controller="yesNoVoteCtrl">
            <div class="span11 media-body">
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                <p><small>${metaData()}</small></p>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                <div>
                    ${stats()}
                </div>
            </div>
            <div class="span1 voteWrapper">
                ${upDownVoteBlock()}
            </div>
        </div>
    </div>
</%def>

<%def name="photo_listing()">
    <div class="media well search-listing" ng-init="rated=item.rated; urlCode=item.urlCode;url=item.url; totalVotes=item.voteCount; yesVotes=item.ups; noVotes=item.downs; netVotes=item.netVotes; objType=item.objType;">
        <div ng-controller="yesNoVoteCtrl">
            <div class="span11 media-body">
                <div class="listed-photo">
                    <a href = '{{item.href}}'>
                        <div class="main-photo" style="background-image:url('{{item.mainPhoto}}');"/></div> 
                    </a>
                </div>
                <h4 class="listed-item-title"><a ng-href="{{item.href}}">{{item.title}}</a></h4>
                <p><small>${metaData()}</small></p>
                <p ng-init="stringLimit=300"><span ng-bind-html="item.html | limitTo:stringLimit"></span>${moreLess()}</p>
                <div>
                    ${stats()}
                </div>
            </div>
            <div class="span1 voteWrapper">
                ${upDownVoteBlock()}
            </div>
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
        <a href="/login" class="upVote">
            <i class="icon-chevron-sign-up icon-2x"></i>
        </a>
        <br>
        <div class="centered chevron-score"> {{netVotes}}</div>
        <a href="/login" class="downVote">
            <i class="icon-chevron-sign-down icon-2x"></i>
        </a>
    % endif
    <br>
</%def>

<%def name="moreLess()">
    <a href="#a" ng-show="item.text.length > 300 && stringLimit == 300" ng-click="stringLimit = 10000">more</a><a href="#{{item.urlCode}}" ng-show="item.text.length > 300 && stringLimit == 10000" ng-click="stringLimit = 300">less</a>
</%def>

<%def name="metaData()">
    <small><img class="thumbnail flag mini-flag border" src="{{item.flag}}"> 
        <span style="text-transform: capitalize;">{{item.objType}}</span> for <a class="green green-hover" href="{{scope.href}}"><span ng-show="!(item.scopeLevel == 'Country' || item.scopeLevel == 'Postalcode' || item.scopeLevel == 'County')">{{item.scopeLevel}} of</span> {{item.scopeName}} <span ng-show="item.scopeLevel == 'County'"> {{item.scopeLevel}}</span></a>
        <span ng-repeat="tag in item.tags" class="label workshop-tag {{tag}}">{{tag}}</span>
        <span ng-if="item.parentObjType && !(item.parentObjType == '')">
            in <a ng-href="{{item.parentHref}}" class="green green-hover">{{item.parentTitle}}</a>
        </span>
    </small>
</%def>

<%def name="stats()">
    <div ng-init="discussionCode = item.discussion; parentCode = 0; thingCode = item.urlCode; commentRole = 'yes'; submit = 'reply' ">
        <div ng-controller="commentsController">
            <ul class="horizontal-list iconListing">
                <li>
                    <span ng-show="item.numComments == '0'" class="no-highlight"><i class="icon-comments"></i> Comments ({{item.numComments}})</span>
                    <a ng-show="!(item.numComments == '0')" class="no-highlight" href="#a" ng-click="getComments()"><i class="icon-comments"></i> Comments ({{item.numComments}})</a>
                </li>
                <li><i class="icon-eye-open"></i> Views ({{item.views}})</li>
            </ul>
            ### Comments
            <div class="centered" ng-show="commentsLoading" ng-cloak>
                <i class="icon-spinner icon-spin icon-2x"></i>
            </div>

            <table class="activity-comments" ng-class="{hidden : commentsHidden}" style = "background-color: whitesmoke;">
                <tr ng-repeat="comment in comments" ng-class="{pro : comment.commentRole == 'yes', con : comment.commentRole == 'no', neutral : comment.commentRole == 'neutral'}">

                    <td style="vertical-align: top; width: 35px;">
                        <img class="media-object avatar small-avatar" ng-src="{{comment.authorPhoto}}" alt="{{comment.authorName}}" title="{{comment.authorName}}">
                    </td>
                    <td style="padding: 10px;">
                        <small><a class="no-highlight" ng-href="{{comment.authorHref}}"><strong>{{comment.authorName}}</strong></a><span class="date">{{comment.date}} ago</span></small>
                        <br>
                        {{comment.data}}                    
                  </td>
                </tr>
            </table>
        </div>
    </div>
</%def>