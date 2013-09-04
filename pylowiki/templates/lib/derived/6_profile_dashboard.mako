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

<%def name="thingCount(user, things, title)">
    <% 
        thisTitle = title
        if title == 'conversations':
            thisTitle = 'discussions'
        elif title == 'bookmarks':
            thisTitle = 'watching'
        thingListingURL = "/profile/%s/%s/%s" %(user['urlCode'], user['url'], thisTitle)
    %>
    <h3 class="profile-count centered">
        <a class="black" href="${thingListingURL}">${len(things)}</a>
    </h3>
    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">${title}</a></p></div>
</%def>

<%def name="profileDashboard()">
    <div class="centered">
        ${lib_6.userImage(c.user, className="avatar avatar-large")}
    </div>
    <div class="section-wrapper">
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
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.resources, 'resources')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.ideas, 'ideas')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.discussions, 'conversations')}
                </div>
            </div> <!--/.row-fluid-->
            <hr>
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.followers, 'followers')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.following, 'following')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.watching, 'bookmarks')}
                </div>
            </div> <!--/.row-fluid-->
                        <hr>
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.photos, 'pictures')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.facilitatorWorkshops, 'facilitating')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.listeningWorkshops, 'listening')}
                </div>
            </div> <!--/.row-fluid-->
        </div><!--/.browse-->
    </div><!--/.section-wrapper-->
</%def>
