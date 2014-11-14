<%namespace name="workshopHelpers" file="/lib/derived/6_workshop_home.mako" />
<%namespace name="ng_helpers" file="/lib/ng_lib.mako"/>


<%def name="homeSlide(item)">
	<div class="span wrap-voting-group-slide" style="background-image:url('${item['photo']}'); background-size: cover; background-position: center center;">
	  <a href="${item['link']}">
	    <span class="link-span dark-gradient"></span><!-- used to make entire div a link -->
	    <div class="row-fluid tile-title lead">Featured Workshop</div>
	    <div class="row-fluid featured">
	    	<table class="featured-title">
	            <tr>
	              <td>
	                <span>${item['title']}</span><br>
	     			${workshopHelpers.displayWorkshopFlag(item['item'], 'small')}<span class="featured-scope-title lead">${item['scopeTitle']}</span>
	              </td>
	            </tr>
	         </table>
	    </div>
	  </a>
	</div>
</%def>

<%def name="feedFilters()">
	<ul ng-if="geoScope === ''" class="nav nav-pills">
        <li ng-class="{'active' : activityType == '/all'}"><a ng-click="getAllActivity()"> Activity </a></li>
        <li ng-class="{'active' : activityType == 'initiatives'}"><a ng-click="browseInitiatives()"> Initiatives </a></li>
        % if c.authuser:
          <li ng-class="{'active' : activityType == 'following'}"><a ng-click="getFollowingActivity()"> Following Activity</a></li>
          <li ng-class="{'active' : activityType == '/meetings'}"><a ng-click="getMeetingActivity()"> Upcoming Meetings </a></li>
        % endif
    </ul>
</%def>

<%def name="followingInitiatives()">
	<div ng-controller="followCtrl">

      	<div infinite-scroll='getFollowSlice()' infinite-scroll-disabled='followLoading' infinite-scroll-distance='5'>
	        % if c.authuser:

                <div class="well" ng-show="followInitiatives.length >= 1" ng-cloak>
                	<h4 class="well-header grey">Following</h4>
                	<div ng-repeat="item in followInitiatives">
                    	<div ng-init="url=item.url; code=item.urlCode">
                         	<div ng-controller="follow_unfollowCtrl">
                           
                            <table class="activity-item follow" ng-show="following" ng-hide="trashed" ng-cloak>
                              	<tr>
	                                <td rowspan="2" class="avatar-cell">
	                                  <a href = '{{item.href}}'>
	                                      <div class="i-photo small-i-photo" style="background-image:url('{{item.thumbnail}}');"/></div> 
	                                  </a>
	                                </td>
	                                <td colspan="2" class="title-cell">
	                                  <a class="no-highlight" href = '{{item.href}}'><h5 class="initiative-title listed-item-title">{{item.title}}</h5></a>
	                                  <div class="btn-group pull-right follow-actions">
	                                    <a class="btn clear dropdown-toggle" data-toggle="dropdown" href="#">
	                                      <i class="grey icon-gear"></i>
	                                    </a>
	                                    <ul class="dropdown-menu">
	                                      <li  ng-if="!(item.authorID == '${c.authuser.id}')"><a ng-click="changeFollow()">Unfollow</a></li>
	                                      <li ng-if="item.authorID == '${c.authuser.id}'"><a href = '{{item.href}}/edit'>Edit</a></li>
	                                      <li ng-if="item.authorID == '${c.authuser.id}'"><a ng-click="trashThing()">Delete</a></li>
	                                    </ul>
	                                  </div>
	                                </td>
								</tr>
								<tr>
	                                <td class="vote-progress">
		                            	<small class="grey">{{item.voteCount}} votes</small>
										<div>
										  <div class="progress vote-progress">
										    <div class="progress-bar" role="progress-bar" style="width: {{100 * item.voteCount / item.goal | number:0}}%;"></div>
										  </div>
										  <small ng-if="item.goal == 100" class="grey pull-right clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes needed for this idea to become an initiative.">{{item.goal - item.voteCount | number}} NEEDED</small>
										  <small ng-if="!(item.goal == 100)" class="grey pull-right clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{item.goal - item.voteCount | number}} NEEDED</small>
										</div>
	                                </td>
	                                <td class="text-right">
	                                  <small>
	                                  <span class="green">{{100 * item.ups / item.voteCount | number:0}}% YES</span> | <span class="red">{{100 * item.downs / item.voteCount | number:0}}% NO</span>
	                                  </small>
	                                </td>
								</tr>
                            </table>
						</div><!-- follow_unfollowCtrl -->
					</div><!-- ng-init -->
				</div><!-- ng-repeat -->
				<div class="centered following-spinner" ng-show="followSliceLoading" ng-cloak>
					<i class="icon-spinner icon-spin icon-4x"></i>
                </div>
            </div><!-- well -->

            <div class="centered following-spinner" ng-show="followLoading" ng-cloak>
              <i class="icon-spinner icon-spin icon-4x"></i>
            </div>

            <div ng-show="noFollowingResult && !followLoading" class="alert alert-info" ng-cloak>
                You have not followed or authored any initiatives yet.
            </div>

            <div class="large-spacer"></div>

	        % endif
		</div><!-- infinite-scroll -->
    </div><!-- follow-controller -->
</%def>

<%def name="geoFlagInfo()">
	<div ng-if="geoScope != ''" ng-cloak style="position: relative;">
		<div style="background-image:url('{{geoPhoto}}'); height: 100px; z-index: 50; border-radius: 4px 4px 0px 0px;  border: 1px solid #e3e3e3; background-position:50% 30%;">
		</div>
		<img src="{{geoFlagUrl}}" class="info-side-img"/>
		<div class="well" style="z-index: 53;height: 100px;margin-top: -50px;text-align: right; border-radius: 0px 0px 4px 4px;">
			<div class="top-info-side" style="margin-top: -50px;">
				<p>{{geoScopeName}}</p>
			</div>
			<div>
				<p>
				Population: {{geoPopulation | number}}<br/>
				<p ng-if="False" ng-cloak>Members: 123456789</p>
				</p>
				<div class="nav nav-pills" ng-if="geoScope != ''" ng-cloak>
				<a href="{{geoHref}}" class="active">View full profile</a>
				</div>
			</div>
		</div>
	</div>
</%def>

<%def name="elections()">
	% if c.authuser:
		<div  ng-init="postalCode=${c.authuser['postalCode']};">
		  <div ng-controller="electionsHomeController">
		    <div ng-show="elections.length >= 1" ng-cloak class="media well search-listing">
		    	<h4 class="well-header grey">Upcoming Elections</h4>
					<table ng-show="!restored" class="activity-item follow" style="margin-bottom: 0;" ng-cloak>
						<tr ng-repeat="item in elections">
							<td>${ng_helpers.election_home_listing()}</td>
						</tr>
					</table>
		    </div><!-- ng-show -->
		  </div><!-- electionsHomeController -->
		</div>
	% endif
</%def>

<%def name="leaderboardHome()">
    <div class="well" ng-controller="leaderboardController" ng-init="leaderboard.type = 'initiatives'" ng-cloak>
    <h4 class="well-header grey">Leaderboard</h4>
    <p>initiatives members </p>
        <table class="table table-condensed">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Votes</th>
                </tr>
            </thead>
            <tbody>
                <tr ng-repeat="item in leaderboard.list">
                    <td>{{item['title']}}</td>
                    <td>{{item['voteCount']}}</td>
                </tr>
            </tbody>
        </table>
        <p><a href="#" ng-if="!firstSector" ng-click="getSector('less')">previous 10</a> <a href="#" ng-click="getSector('more')">next 10</a>     <a href="#">show all</a></p>
    </div>
</%def>
