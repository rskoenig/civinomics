<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%! 
    import pylowiki.lib.db.user     as userLib 
    import pylowiki.lib.db.message  as messageLib
%>

<%def name="mainNavbar()">
    <div class="navbar civ-navbar">
        <div class="navbar-inner"
            % if "corp" in session._environ['PATH_INFO']:
                id="corpNavbar"
            % endif
        >
            <div class="container">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </a>
                <a class="brand civ-brand" href="/">
                    % if "corp" in session._environ['PATH_INFO']:
                        <img src="/images/logo_white.png" class="small-logo" id="civinomicsLogo">
                    % else:
                        <img src="/images/logo.png" class="small-logo" id="civinomicsLogo">
                    % endif
                </a>
                <ul class="nav">
                    <li>
                        <form class="form-search" action="/search">
                            <div class="input-append">
                                <input type="text" class="span2 search-query" placeholder="workshops or people" id="search-input" name="searchQuery" value="${c.searchQuery}">
                            </div>
                            <span class="search-icon-container">
                                <img src="/images/glyphicons_pro/glyphicons/png/glyphicons_027_search.png" class="search-icon" data-toggle="tooltip" title="search">
                            </span>
                        </form>
                    </li>
                </ul>
                <div class="nav-collapse collapse">
                    <ul class="nav pull-right" id="profileAvatar">
                        % if 'user' in session:
                            <li>
                                ${lib_6.userImage(c.authuser, className="avatar topbar-avatar", linkClass="topbar-avatar-link")}
                                <%
                                    profileTitle = 'profile'
                                    numMessages = messageLib.getMessages(c.authuser, read = '0', count = True)
                                    if numMessages:
                                        if numMessages > 0:
                                            profileTitle += ' (%s)' % numMessages
                                %>
                                <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">${profileTitle}</a>
                            </li>
                            % if 'user' in session:
                                <%
                                    country = c.authuser_geo['countryTitle']
                                    countryURL = c.authuser_geo['countryURL']
                                    state = c.authuser_geo['stateTitle']
                                    stateURL = c.authuser_geo['stateURL']
                                    county = c.authuser_geo['countyTitle']
                                    countyURL = c.authuser_geo['countyURL']
                                    city = c.authuser_geo['cityTitle']
                                    cityURL = c.authuser_geo['cityURL']
                                    postalCode = c.authuser_geo['postalCodeURL']
                                %>
                                <li class="dropdown">
                                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">workshops<b class="caret"></b></a>
                                    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                        <li><a tabindex="-1" href="/workshop/display/create/form">start a new workshop!</a></li>
                                        <li><a tabindex="-1" href="/workshops">show all workshops</a></li>
                                        <li><a tabindex="-1" href="/workshops/geo/earth/${countryURL}/">- ${country}</a></li>
                                        <li><a tabindex="-1" href="/workshops/geo/earth/${countryURL}/${stateURL}/">- State of ${state}</a></li>
                                        <li><a tabindex="-1" href="/workshops/geo/earth/${countryURL}/${stateURL}/${countyURL}/">- County of ${county}</a></li>
                                        <li><a tabindex="-1" href="/workshops/geo/earth/${countryURL}/${stateURL}/${countyURL}/${cityURL}/">- City of ${city}</a></li>
                                        <li><a tabindex="-1" href="/workshops/geo/earth/${countryURL}/${stateURL}/${countyURL}/${cityURL}/${postalCode}">- Postal Code of ${postalCode}</a></li>
                                    </ul>
                                </li>
                            % else:
                                <li><a href="/workshops">workshops</a></li>
                            % endif
                            % if userLib.isAdmin(c.authuser.id):
                                <li class="dropdown">
                                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">objects<b class="caret"></b></a>
                                    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                        <li><a tabindex="-1" href="/admin/users">Users</a></li>
                                        <li><a tabindex="-1" href="/admin/workshops">Workshops</a></li>
                                        <li><a tabindex="-1" href="/admin/ideas">Ideas</a></li>
                                        <li><a tabindex="-1" href="/admin/resources">Resources</a></li>
                                        <li><a tabindex="-1" href="/admin/discussions">Discussions</a></li>
                                        <li><a tabindex="-1" href="/admin/comments">Comments</a></li>
                                    </ul>
                                </li>
                            % endif
                        % endif
                        <li><a href="/help">help</a></li>
                        % if 'user' in session:
                            <li><a href="/login/logout">logout</a></li>
                        % else:
                            <li><a href="/login">login</a></li>
                            <li><a href="/signup">signup</a></li>
                        % endif
                    </ul>
                </div><!--/.nav-collapse -->
            </div> <!--/.container-->
        </div> <!--/.navbar-inner.civ-navbar -->
    </div> <!-- /.navbar -->
    <hr class="civ-topbar-hr" 
        % if "corp" in session._environ['PATH_INFO']:
            id="corpTopbar"
        % endif/
    >
</%def>

<%def name="splashNavbar()">
    <div class="navbar navbar-fixed-top" style="border-bottom:1px solid #DDDDDD;">
      <div class="navbar-inner" style="background-image: none; background-color: #FFFFFF;">
        <div class="container-fluid">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/"> <img src="/images/logo.png"> </a>
          <div class="nav-collapse collapse">
            <ul class="nav pull-left">
               <li class="nav-item"></li> 
            </ul>
            <ul class="nav pull-right">
              <li class="nav-item"><a href="/signup" class="nav-item">Sign Up</a></li>
              <li class="nav-item"><a href="/login" class="nav-item">Log In</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
</%def>

<%def name="corpNavbar()">
    <div class="navbar navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container-fluid">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </a>
                <div class="span2 offset" style="padding-top: 2px; padding-bottom: 5px;">
                    <a href="/"><img src="/images/logo_white.png"></a>
                </div>
                <div class="nav-collapse">
                </div><!--/.nav-collapse -->
            </div>
        </div>
    </div>
</%def>

<%def name="shortFooter()">
    <div id="baseTemplate_footer">
        <div id="footerContainer" class="container">
            <div class="row footer well">
                <div class="span8">
                    <ul class="horizontal-list">
                        <li><a class="green green-hover" href="/corp/about">About</a></li> 
                        <li><a class="green green-hover" href="/corp/polling">Polling</a></li>
                        <li><a class="green green-hover" href="/corp/contact">Contact</a></li>
                        <li><a class="green green-hover" href="/corp/terms">Terms</a></li>
                        <li><a class="green green-hover" href="/help">Help</a></li>
                        <li><a class="green green-hover" href="#" id="footerFeedbackButton">Feedback</a></li>
                    </ul>
                </div>
                <div class="span pull-right">
                  © 2013 Civinomics
                </div>
            </div><!-- row footer well -->
        </div><!-- footerContainer -->
    </div><!-- baseTemplate_footer -->
</%def>

<%def name="copyright()">
    <div id="baseTemplate_footer">
        <div id="footerContainer" class="container">
            <div class="row footer well">
                <div class="span pull-right">
                  © 2013 Civinomics
                </div>
            </div><!-- row footer well -->
        </div><!-- footerContainer -->
    </div><!-- baseTemplate_footer -->
</%def>

<%def name="tallFooter()">
    <div class="footer-separator"></div>

    <div class="footer-civ">
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span10 offset1">
                    <div class="span2">
                        <ul class="unstyled footer-list">
                            <li>
                                <h4>
                                    ORGANIZATION
                                </h4>
                            </li>
                            <li><a href="/corp/about"> About</a></li>
                            <li><a href="/corp/team">Team</a></li>
                            <li><a href="/corp/careers">Careers</a></li>
                            <li><a href="/corp/terms">Terms</a></li>
                            <li><a href="/corp/privacy">Privacy</a></li>
                            <li><a href="http://www.civinomics.wordpress.com" target="_blank">Blog</a></li>
                            <li><a href="/corp/news">News</a></li>
                            <li><a href="/corp/contact">Contact</a></li>
                        </ul>
                    </div>
                    
                    <div class="span3">
                        <ul class="unstyled footer-list">
                            <li>
                                <h4>
                                    SERVICES
                                </h4>
                            </li>
                            <li><a href="/corp/polling">Polling</a></li>
                            <li><a href="#">Online</a><span class="label label-warning">Coming Soon</span></li>
                            <li><a href="/corp/caseStudies">Case Studies</a></li>
                        </ul>
                    </div>

                    <div class="span3" style="padding-top:20px;">
                        <ul class="unstyled" style="color:#818180;">
                        <li><div class="fb-like" data-href="http://www.facebook.com/civinomics" data-send="true" data-width="395" data-show-faces="true"></div> 
                        </li>
                        <li><a href="https://twitter.com/civinomics" class="twitter-follow-button" data-show-count="true" data-size="large">Follow @civinomics</a></li>
                        <li><g:plusone annotation="inline"></g:plusone></li>
                        </ul>
                    </div>

                </div>
            </div>
            <div class="row-fluid">
                <div class="span10 offset1" style="color:#e4e4e4;">
                    <p class="pull-right">
                        © 2012 Civinomics Inc. All rights reserved.
                    </p>
                </div>
            </div>
        </div>
    </div>
</%def>
