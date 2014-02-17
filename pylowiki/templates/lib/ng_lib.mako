
<%def name="initiative_listing()">
    <td class="initiative-listing">
        <div class="media well searchListing" ng-init="rated=initiative.rated; urlCode=initiative.urlCode;url=initiative.url; totalVotes=initiative.voteCount; yesVotes=initiative.ups; noVotes=initiative.downs; objType='initiative';">
            <div class="media-body" ng-controller="yesNoVoteCtrl">
                <div class="span9">
                    <div class="span3">
                        <a href = '{{initiative.initiativeLink}}'>
                            <div class="i-thumb" style="background-image:url('{{initiative.thumbnail}}');"/></div>
                        </a>
                    </div>
                    <div class="span9">
                        <h4 class="media-heading">
                            <a class="listed-item-title initiative-title" href="{{initiative.initiativeLink}}">{{initiative.title}}</a>
                        </h4>
                        <p>{{initiative.description}}</p>
                        <hr class="no-bottom no-top">
                        <h5 class="h45">
                            <small class="grey centered">Estimated Cost:</small>
                            <span class="pull-right">{{initiative.cost | currency}}</span>
                        </h5>
                        <small>
                            % if c.searchType and c.searchType != 'region':
                                <a class="no-highlight" href="{{initiative.geoHref}}"><img class="thumbnail small-flag border" src="{{initiative.flag}}"> {{initiative.scopeLevel}} of {{initiative.scopeName}}</a><br>
                            % endif
                            Authors: <a href="/profile/{{initiative.authorCode}}/{{initiative.authorURL}}">{{initiative.authorName}}</a> | Tags: <span  class="label workshop-tag {{initiative.tag}}">{{initiative.tag}}</span>
                        </small>
                    </div>
                </div>
                <div class="span3 voteBlock ideaListing well" >
                    ${yesNoVoteBlock()}
                </div>
            </div>
        </div>
    </td>
</%def>

<%def name="listIdeas()">
        <div ng-init="rated=idea.rated; urlCode=idea.urlCode;url=idea.url; totalVotes=idea.voteCount; yesVotes=idea.ups; noVotes=idea.downs; objType='idea';">
            <div class="media-body object-in-listing {{idea.status}} border-bottom" ng-controller="yesNoVoteCtrl">
                <div class="span9">
                    <p class="ideaListingTitle"><a class="listed-item-title" href="/workshop/{{idea.workshopCode}}/{{idea.workshopURL}}/idea/{{idea.urlCode}}/{{idea.url}}">
                        {{idea.title}}
                    </a></p>
                    <strong ng-show="idea.status == 'adopted'" class="green"><i class="icon-star"></i> Adopted</strong>
                    <strong ng-show="idea.status == 'disabled'" class="red"><i class="icon-flag"></i> Disabled</strong>
                    <p>{{idea.text}}</p>
                    <ul class="horizontal-list iconListing">
                        <li>
                            <a href="/profile/{{idea.authorCode}}/{{idea.authorURL}}"><img class="avatar topbar-avatar" ng-src="http://www.gravatar.com/avatar/{{idea.authorHash}}?r=pg&d=identicon&s=200" alt="{{idea.authorName}}" title="{{idea.authorName}}"></a>Posted by <a class="green green-hover" href="/profile/{{idea.authorCode}}/{{idea.authorURL}}">{{idea.authorName}}</a> <span class="grey">{{idea.fuzzyTime}} ago</span>
                        </li>
                        <!-- <li><i class="icon-file-text"></i> Read full text</li> -->
                        <li><i class="icon-comment"></i> Comments ({{idea.numComments}})</li>
                        <li><i class="icon-eye-open"></i> Views ({{idea.views}})</li>
                    </ul>
                </div>
                <div class="span3 voteBlock ideaListing well" >
                    ${yesNoVoteBlock()}
                </div><!-- voteBlock -->
            </div><!-- media-body -->
        </div><!-- search-listing -->
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

<%def name="listenerFacilitationInvite()">
    
    % if {{read}} == u'1':
        <div class="media">
            <img src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left message-workshop-image">
            <div class="media-body">
                <h5 class="media-heading">
                    {{messageTitle}}
                </h5>
                <p>
                    <a href="{{userLink}}">{{userName}}</a>
                    invites you to facilitate 
                    <a href="{{itemLink}}">{{itemTitle}}</a>
                </p>
                <p>
                    {{messageText}}
                </p>
                <p>
                    (You have already responded by 
                    {{responseAction}})
                </p>
                <p class="pull-right"><small>
                    {{messageDate}}
                    (PST)
                </small></p>
            </div>
        </div>
    % else:
        {{formStr}}
            <input type="hidden" name="workshopCode" value="{{itemCode}}">
            <input type="hidden" name="workshopURL" value="{{itemUrl}}">
            <input type="hidden" name="messageCode" value="{{messageCode}}">
            <div class="media">
                <img src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left message-workshop-image">
                <div class="media-body">
                    <h5 class="media-heading">
                        {{messageTitle}}
                    </h5>
                    <p>
                        <a href="{{userLink}}">{{userName}}</a>
                        invites you to 
                        {{action}} 
                        <a href="{{itemLink}}">{{itemTitle}}</a>
                    </p>
                    <p>
                        {{messageText}}
                    </p>
                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{action}} the workshop">Accept</button>
                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{action}} the workshop">Decline</button>
                    <p class="pull-right"><small>
                        {{messageDate}} 
                        (PST)
                    </small></p>
                </div>
            </div>
        </form>
    % endif

</%def>