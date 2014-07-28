<%!
    import pylowiki.lib.db.workshop     as workshopLib
    import pylowiki.lib.db.facilitator  as facilitatorLib
    import pylowiki.lib.db.listener     as listenerLib
    import pylowiki.lib.db.follow       as followLib
    import pylowiki.lib.db.user         as userLib
    import pylowiki.lib.db.pmember      as pmemberLib
    import pylowiki.lib.utils           as utils
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="profileCurator()">

    
</%def>

<%def name="profileDashboard()">
    <div class="centered">
        ${lib_6.userImage(c.user, className="avatar avatar-large")}
    </div>
    <div class="section-wrapper" ng-cloak>
        <div class="browse">

            %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                <div ng-init="dashboardFullName='${c.user['name']}'; greetingMsg='${c.user['greetingMsg']}'; fullName='${c.user['name']}'; websiteDesc='${c.user['websiteDesc']}'; postalCode='${c.user['postalCode']}'; updateGeoLinks();";>
                    <h3 class="section-header">{{fullName}}</h3>
                    <p><a href="{{cityURL}}">{{cityTitle}}</a>, <a href="{{stateURL}}">{{stateTitle}}</a>, <a href="{{countryURL}}">{{countryTitle}}</a>
                </div>
            %else:
                <h3 class="section-header">${c.user['name']}</h3>
                <p>${lib_6.userGeoLink(c.user)}</p>
            %endif
            
            <p>Joined ${c.user.date.strftime('%b %d, %Y')}</p>
            % if 'curateLevel' in c.user and c.user['curateLevel'] != '':
                <p>Community curator for ${c.user['curateLevelTitle']}</p>
            % endif
            %if c.isAdmin:
                <div class="well">
                % if 'curateLevel' in c.user and c.user['curateLevel'] != '':
                    <form method="POST" action="/profile/${c.user['urlCode']}/${c.user['url']}/nocurate">
                    Remove as a curator: <button type="submit" class="btn btn-danger">Submit</button>
                    </form>
                % else:
                    <form method="POST" action="/profile/${c.user['urlCode']}/${c.user['url']}/curate">
                    Make a curator for their &nbsp; &nbsp;
                    <select name="curateLevel">
                        <option value="8">City</option>
                        <option value="6" selected>County</option>
                        <option value="4">State</option>
                        <option value="2">Country</option>
                    </select> 
                    <p><button type="submit" class="btn btn-primary">Submit</button></p>
                    </form>
                % endif
                </div><!-- well -->
                <div class="spacer"></div>
            % endif
            % if c.user['greetingMsg'] != '':
                %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                    <div ng-init="dashboardGreetingMsg='${c.user['greetingMsg']}'">
                    <small class="muted expandable">{{greetingMsg}}</small>
                %else:
                    <small class="muted expandable">${c.user['greetingMsg']}</small>
                %endif
            % endif
            % if c.user['websiteLink'] != '':
                %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                    <div ng-init="dashboardWebsiteLink='${c.user['websiteLink']}'">
                    <p class = "expandable no-bottom"><a href="{{dashboardWebsiteLink}}" target="_blank">{{dashboardWebsiteLink}}</a></p>
                %else:
                    <p class = "expandable no-bottom"><a href="${c.user['websiteLink']}" target="_blank">${c.user['websiteLink']}</a></p>
                % endif
                % if c.user['websiteDesc'] != '':
                    %if ('user' in session and c.user.id == c.authuser.id) or c.isAdmin:
                        <div ng-init="dashboardWebsiteDesc='${c.user['websiteDesc']}'">
                            <small class="muted expandable">{{websiteDesc}}</small>
                        </div>
                    %else:
                        <small class="muted expandable">${c.user['websiteDesc']}</small>
                    %endif
                % endif
            % endif
            <hr>
            <div class="row">
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/resources" %(c.user['urlCode'], c.user['url'])
                        if 'resource_counter' in c.user:
                            numThings = c.user['resource_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">resources</a></p></div>
                </div><!-- col-xs-4 -->
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/ideas" %(c.user['urlCode'], c.user['url'])
                        if 'idea_counter' in c.user:
                            numThings = c.user['idea_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">ideas</a></p></div>
                </div>
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/discussions" %(c.user['urlCode'], c.user['url'])
                        if 'discussion_counter' in c.user:
                            numThings = c.user['discussion_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">conversations</a></p></div>
                </div>
            </div> <!--/.row-->
            <hr>
            <div class="row">
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/followers" %(c.user['urlCode'], c.user['url'])
                        if 'follower_counter' in c.user:
                            numThings = c.user['follower_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">followers</a></p></div>
                </div>
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/following" %(c.user['urlCode'], c.user['url'])
                        if 'follow_counter' in c.user:
                            numThings = c.user['follow_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">following</a></p></div>
                </div>
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/watching" %(c.user['urlCode'], c.user['url'])
                        if 'bookmark_counter' in c.user:
                            numThings = c.user['bookmark_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">bookmarks</a></p></div>
                </div>
            </div> <!--/.row-->
                        <hr>
            <div class="row">
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/pictures" %(c.user['urlCode'], c.user['url'])
                        if 'photo_counter' in c.user:
                            numThings = c.user['photo_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">pictures</a></p></div>
                </div>
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/facilitating" %(c.user['urlCode'], c.user['url'])
                        if 'facilitator_counter' in c.user:
                            numThings = c.user['facilitator_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">facilitating</a></p></div>
                </div>
                <div class="col-xs-4">
                    <% 
                        thingListingURL = "/profile/%s/%s/listening" %(c.user['urlCode'], c.user['url'])
                        if 'listener_counter' in c.user:
                            numThings = c.user['listener_counter']
                        else:
                            numThings = '0'
                    %>
                    <h3 class="profile-count centered">
                    <a class="black" href="${thingListingURL}">${numThings}</a>
                    </h3>
                    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">listening</a></p></div>
                </div>
            </div> <!--/.row-->
        </div><!--/.browse-->
    </div><!--/.section-wrapper-->
</%def>
