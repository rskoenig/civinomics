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
                            <a href="/profile/{{idea.authorCode}}/{{idea.authorURL}}"><img class="avatar topbar-avatar" ng-src="http://www.gravatar.com/avatar/{{idea.authorHash}}?r=pg&d=identicon&s=200" alt="{{idea.authorName}}" title="{{idea.authorName}}"></a>Posted by <a class="green green-hover" href="/profile/{{idea.authorCode}}/{{idea.authorURL}}">{{idea.authorName}}</a> <span class="grey">{{idea.date}} ago</span>
                        </li>
                        <!-- <li><i class="icon-file-text"></i> Read full text</li> -->
                        <li><i class="icon-comment"></i> Comments ({{idea.numComments}})</li>
                        <li><i class="icon-eye-open"></i> Views ({{idea.views}})</li>
                    </ul>
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
                            Total Votes: <span class="totalVotes">{{totalVotes}}</span>
                        </div>
                    % else:
                        <a href="/login" class="yesVote">
                            <div class="vote-icon yes-icon"></div>
                        </a>
                        <br>
                        <br>
                        <a href="/login" class="noVote">
                            <div class="vote-icon no-icon"></div>
                        </a>
                        <br>
                        <div class="totalVotesWrapper">
                            Total Votes: <span class="totalVotes">{{totalVotes}}</span>
                        </div>
                    % endif
                </div>
            </div><!-- media-body -->
        </div><!-- search-listing -->
</%def>