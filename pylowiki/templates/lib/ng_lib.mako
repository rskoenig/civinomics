
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
                </div>
            </div>
        </div>
    </td>
</%def>