<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%namespace file="/lib/mako_lib.mako" import="fields_alert"/>
<%! 
    import pylowiki.lib.db.user     as userLib 
    import pylowiki.lib.db.message  as messageLib
    import pylowiki.lib.db.tag      as tagLib
    from types import StringTypes
%>

!
<%def name="mainNavbar()">
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                % if 'user' in session:
                    <a href="/home"><img class="nav-logo" src="/images/civ_logo_simple.png"></a>
                % else:
                    <a href="/splash"><img class="nav-logo" src="/images/civ_logo_simple.png"></a>
                % endif
            </div>

            <div class="collapse navbar-collapse">

                <form class="navbar-form navbar-left" action="/search">
                  <div class="form-group">
                    <input type="text" class="form-control" name="searchQuery" placeholder="Search">
                  </div>
                  <button type="submit" class="btn btn-default">Submit</button>
                </form>
                
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="/home">Home</a></li>
                    % if c.authuser:
                        % if c.authuser['activated'] == '1':
                            <li class="dropdown">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Create <b class="caret"></b></a>
                                <ul class="dropdown-menu">
                                    % if 'user' in session:
                                        <li>
                                            <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/newInitiative"><i class="icon-file-text"></i> New Initiative</a>
                                        </li>
                                    % endif
                                    <li><a href="/workshop/display/create/form"><i class="icon-gear"></i> New Workshop</a></li>
                                    % if int(c.authuser['accessLevel']) > 200:
                                        <li><a href="/meeting/${c.authuser['urlCode']}/${c.authuser['url']}/meetingNew"><i class="icon-calendar"></i> New Meeting</a></li>
                                    % endif
                                </ul>
                            </li>
                        % endif
                        % if userLib.isAdmin(c.authuser.id):
                            <li class="dropdown">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Curate<b class="caret"></b></a>
                                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                    <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/csv">Upload</a></li>
                                    % if 'meeting_counter' in c.authuser and c.authuser['meeting_counter'] != '0':
                                        <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/meetings">My Meetings</a></li>
                                    % endif
                                    % if 'election_counter' in c.authuser and c.authuser['election_counter'] != '0':
                                        <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/elections">My Elections</a></li>
                                    % endif
                                    % if 'ballot_counter' in c.authuser and c.authuser['ballot_counter'] != '0':
                                        <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/ballots">My Ballots</a></li>
                                    % endif
                                    <li><a tabindex="-1" href="/admin/users">All Users</a></li>
                                    <li><a tabindex="-1" href="/admin/usersNotActivated">Unactivated Users</a></li>
                                    <li><a tabindex="-1" href="/admin/workshops">Workshops</a></li>
                                    <li><a tabindex="-1" href="/admin/ideas">Ideas</a></li>
                                    <li><a tabindex="-1" href="/admin/resources">Resources</a></li>
                                    <li><a tabindex="-1" href="/admin/discussions">Discussions</a></li>
                                    <li><a tabindex="-1" href="/admin/comments">Comments</a></li>
                                    <li><a tabindex="-1" href="/admin/photos">Photos</a></li>
                                    <li><a tabindex="-1" href="/admin/flaggedPhotos">Flagged Photos</a></li>
                                    <li><a tabindex="-1" href="/admin/initiatives">Initiatives</a></li>
                                    <li><a tabindex="-1" href="/admin/flaggedInitiatives">Flagged Initiatives</a></li>
                                </ul>
                            </li>
                        % endif
                        <li>
                            <%
                                messageCount = ''
                                numMessages = messageLib.getMessages_count(c.authuser, read = '0', count = True)
                                if numMessages:
                                    if numMessages > 0:
                                        messageCount += '<span class="badge badge-warning left-space"> %s</span>' % numMessages
                            %>
                            <a href="/messages/${c.authuser['urlCode']}/${c.authuser['url']}"><i class="glyphicon glyphicon-envelope"></i></i>${messageCount | n}</a>
                        </li>
                        <li class="dropdown">
                            <a href="#"  style="padding-bottom:0px;" class="dropdown-toggle" data-toggle="dropdown">${lib_6.userImage(c.authuser, className="avatar topbar-avatar", noLink=True)} Me <b class="caret"></b></a>
                            <ul class="dropdown-menu">
                                <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">My Profile</a>
                                % if c.authuser['activated'] == '1':
                                    <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/edit#tab4">Reset Password</a>
                                % endif
                                <li><a href="/help">Help</a></li>
                                <li class="divider"></li>
                                <li><a tabindex="-1" href="/login/logout">Logout</a></li>
                            </ul>
                        </li>
                    % else:
                        <li><a href="/login">Login</a></li>
                        <li><a href="/signup">Signup</a></li>
                    % endif

                </ul>
            </div><!-- /.navbar-collapse -->
        </div><!-- container fluid -->
    </nav>
</%def>


<%def name="oldNavbar()">
    <% tagCategories = tagLib.getTagCategories() %>
    <div class="navbar civ-navbar navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container">
                <a class="brand civ-brand" href="/">
                    <div class="logo" id="civinomicsLogo"></div>
                </a>
                <ul class="nav">
                    <li class="small-hidden">
                        <form class="form-search" action="/search">
                            <div class="input-append">
                                <input type="text" class="span2 search-query" name="searchQuery" placeholder="Search">
                                <button type="submit" class="btn btn-search-first"><i class="icon-search"></i></button>
                                <button type="button" class="btn" data-toggle="collapse" data-target="#search">Advanced</button>
                            </div>
                        </form>
                    </li>
                </ul>
                <ul class="nav pull-right" id="profileAvatar">
                    <%
                        wSelected = mSelected = pSelected = aSelected = hSelected = homeSelected = aSelected = bSelected = ''
                        if "/workshops" in session._environ['PATH_INFO'] and not 'geo' in session._environ['PATH_INFO']:
                            wSelected = "active"
                        elif "/messages" in session._environ['PATH_INFO']:
                            mSelected = "active"
                        elif "/profile" in session._environ['PATH_INFO']:
                            pSelected = "active"
                        elif "/admin" in session._environ['PATH_INFO']:
                            aSelected = "active"
                        elif "/help" in session._environ['PATH_INFO']:
                            hSelected = "active"
                        elif "/home" in session._environ['PATH_INFO']:
                            homeSelected = "active"
                        elif "/browse/initiatives" in session._environ['PATH_INFO']:
                            bSelected = "active"
                        elif "/corp/about" in session._environ['PATH_INFO']:
                            aSelected = "active"
                        endif
                    %>
                    % if 'user' in session:
                        <li class="${homeSelected}">
                            <a href="/">Home</a>
                        </li>
                        <!--<li class="${bSelected}"><a href="/browse/initiatives">Browse</a></li>-->
                        % if userLib.isAdmin(c.authuser.id):
                            <li class="dropdown ${aSelected}">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Curate<b class="caret"></b></a>
                                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                    <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/csv">Upload</a></li>
                                    % if 'meeting_counter' in c.authuser and c.authuser['meeting_counter'] != '0':
                                        <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/meetings">My Meetings</a></li>
                                    % endif
                                    % if 'election_counter' in c.authuser and c.authuser['election_counter'] != '0':
                                        <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/elections">My Elections</a></li>
                                    % endif
                                    % if 'ballot_counter' in c.authuser and c.authuser['ballot_counter'] != '0':
                                        <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/ballots">My Ballots</a></li>
                                    % endif
                                    <li><a tabindex="-1" href="/admin/users">All Users</a></li>
                                    <li><a tabindex="-1" href="/admin/usersNotActivated">Unactivated Users</a></li>
                                    <li><a tabindex="-1" href="/admin/workshops">Workshops</a></li>
                                    <li><a tabindex="-1" href="/admin/ideas">Ideas</a></li>
                                    <li><a tabindex="-1" href="/admin/resources">Resources</a></li>
                                    <li><a tabindex="-1" href="/admin/discussions">Discussions</a></li>
                                    <li><a tabindex="-1" href="/admin/comments">Comments</a></li>
                                    <li><a tabindex="-1" href="/admin/photos">Photos</a></li>
                                    <li><a tabindex="-1" href="/admin/flaggedPhotos">Flagged Photos</a></li>
                                    <li><a tabindex="-1" href="/admin/initiatives">Initiatives</a></li>
                                    <li><a tabindex="-1" href="/admin/flaggedInitiatives">Flagged Initiatives</a></li>
                                    <li><a tabindex="-1" href="/admin/meetings">All Meetings</a></li>
                                    <li><a tabindex="-1" href="/admin/elections">All Elections</a></li>
                                    <li><a tabindex="-1" href="/admin/ballots">All Ballots</a></li>
                                </ul>
                            </li>
                        % endif
                        % if c.authuser['activated'] == '1':
                            <li class="dropdown">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                    Create <span class="caret"></span>
                                </a>
                                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                    <li>
                                        <a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/newInitiative"><i class="icon-file-text"></i> New Initiative</a>
                                    </li>
                                    <li><a href="/workshop/display/create/form"><i class="icon-gear"></i> New Workshop</a></li>
                                    % if int(c.authuser['accessLevel']) > 200:
                                        <li><a href="/meeting/${c.authuser['urlCode']}/${c.authuser['url']}/meetingNew"><i class="icon-calendar"></i> New Meeting</a></li>
                                        <li><a href="/election/${c.authuser['urlCode']}/${c.authuser['url']}/electionNew"><i class="icon-ok"></i> New Election</a></li>
                                    % endif
                                </ul>
                            </li>

                            <li class="${mSelected}">
                                <%
                                    messageCount = ''
                                    numMessages = messageLib.getMessages_count(c.authuser, read = '0', count = True)
                                    if numMessages:
                                        if numMessages > 0:
                                            messageCount += '<span class="badge badge-warning left-space"> %s</span>' % numMessages
                                %>
                                <a href="/messages/${c.authuser['urlCode']}/${c.authuser['url']}"><i class="icon-envelope icon-white"></i>${messageCount | n}</a>
                            </li>
                        % endif
                        <li class="dropdown ${pSelected}">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                ${lib_6.userImage(c.authuser, className="avatar topbar-avatar", noLink=True)} Me<b class="caret"></b></a>
                            <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" id="profileDropdown">
                                <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">My Profile</a>
                                % if c.authuser['activated'] == '1':
                                    <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/edit#tab4">Reset Password</a>
                                % endif
                                <li><a href="/help">Help</a></li>
                                <li><a tabindex="-1" href="/login/logout">Logout</a></li>
                            </ul>
                        </li>
                    % else:
                        <li class="${bSelected}"><a href="/browse/initiatives">Browse</a></li>
                        <li class="${hSelected}"><a href="/help">Help</a></li>
                        <li><a href="/login">Login</a></li>
                        <li><a href="/signup">Signup</a></li>
                    % endif
                    <li class="small-show">
                        <a type="button" data-toggle="collapse" data-target="#search"><i class="icon-search"></i></a>
                    </li>
                </ul>
            </div> <!--/.container-->
        </div> <!--/.navbar-inner.civ-navbar -->
    </div> <!-- /.navbar -->
    ${search_drawer()}
</%def>

<%def name="splashNavbar()">
    <div class="navbar splash-nav" ng-init="showTitle = 'sTitle'">
      <div class="navbar-inner civinomics-splash">
        <div class="container-fluid">
            <a class="brand" href="/"><div class="logo logo-lg" id="civinomicsLogo"></div></a>
            <ul class="nav">
                <li class="small-hidden">
                    <form class="form-search" action="/search">
                        <input type="text" class="span2 search-query splash" placeholder="Search" name="searchQuery">
                    </form>
                </li>
            </ul>
            <ul class="nav pull-right">
                <li class="nav-item"><a href="/corp/about" class="nav-item">About</a></li>
                <li class="nav-item"><a href="/corp/surveys" class="nav-item">Surveys</a></li>
                <li class="nav-item"><a href="/browse/initiatives" class="nav-item">Browse</a></li>
                <li class="nav-item"><a href="http://civinomics.wordpress.com" target="_blank" class="nav-item">Blog</a></li>
                <!-- <li class="nav-item"><a href="/corp/about" class="nav-item">Create</a></li> -->
                <li class="nav-item">
                    <a href="/login" class="btn nav-login">Log in</a>                            
                </li>
            </ul>
        </div>
      </div>
    </div>
    ${search_drawer()}
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
    </div><!-- kludge for case of missing close div tag -->
    <div id="baseTemplate_footer">
        <div id="footerContainer" class="container">
            <div class="row footer rounded well">
                <div class="col-sm-8 no-left">
                    <ul class="horizontal-list">
                        <li><a class="green green-hover" href="/corp/about">About</a></li> 
                        <li><a class="green green-hover" href="http://civinomics.wordpress.com" target="_blank">Blog</a></li>
                        <li><a class="green green-hover" href="/corp/polling">Polling</a></li>
                        <li><a class="green green-hover" href="/corp/contact">Contact</a></li>
                        <li><a class="green green-hover" href="/corp/terms">Terms</a></li>
                        <li><a class="green green-hover" href="/help">Help</a></li>
                        <li><a class="green green-hover" href="#" id="footerFeedbackButton">Feedback</a></li>
                    </ul>
                </div><!-- col-sm-8 -->
                <div class="span pull-right">
                  © 2014 Civinomics
                </div><!-- span pull-right -->
            </div><!-- row footer well -->
        </div><!-- footerContainer -->
    </div><!-- baseTemplate_footer -->
</%def>

<%def name="copyright()">
    <div id="baseTemplate_footer">
        <div id="footerContainer" class="container">
            <div class="row footer rounded well">
                <div class="span pull-right">
                  © 2014 Civinomics
                </div>
            </div><!-- row footer well -->
        </div><!-- footerContainer -->
    </div><!-- baseTemplate_footer -->
</%def>

<%def name="condensedFooter()">
    <div class="footer">
        <div class="container-fluid" >
            <div class="row ">
                <div class="col-sm-5 text-center">
                    <ul class="horizontal-list">
                        <li><a href="/corp/team">Team</a></li>
                        <li><a href="/corp/careers">Careers</a></li>
                        <li><a href="/corp/news">News</a></li>
                        <li><a href="http://www.civinomics.wordpress.com" target="_blank">Blog</a></li>
                        <li><a href="http://civinomics.storenvy.com" target="_blank">Gear Store</a></li>
                        <li><a href="/corp/caseStudies">Case Studies</a></li>
                        
                    </ul>
                </div>
                <div class="col-sm-2 centered">
                    <img src="/images/logo_white_simple.png">
                </div>
                <div class="col-sm-5">
                    <ul class="horizontal-list">
                        <li><a href="/corp/contact">Contact</a></li>
                        <li><a href="/corp/terms">Terms</a></li>
                        <li><a href="/corp/privacy">Privacy</a></li>
                        <li>© 2014 Civinomics, Inc. </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="search_drawer()">
    <div id="search" class="collapse search_drawer">
        <% tagCategories = tagLib.getTagCategories() %>
        <div class="spacer"></div>
        <div class="row-fluid searches">
            <div class="span3 offset1 small-show">
                <form class="form-search" action="/search">
                    <input type="text" class="search-query" placeholder="Search by Word" id="search-input" name="searchQuery">
                </form>
            </div>
            <div class="span4">
                <script type="text/javascript">
                    function searchTags() {
                        var sIndex = document.getElementById('categoryTag').selectedIndex;
                        var sValue = document.getElementById('categoryTag').options[sIndex].value;
                        if(sValue) {
                            var queryURL = sValue;
                            window.location = queryURL;
                        }
                    }
                </script>
                <form action="/searchTags" class="form-search search-type" method="POST">
                    <i class="icon-tag icon-light"></i>
                    <select name="categoryTag" id="categoryTag" onChange="searchTags();">
                    <option value="0">Search by Category</option>
                    % for tag in tagCategories:
                        <% tagValue = tag.replace(" ", "_") %>
                        <option value="/searchTags/${tagValue}/">${tag.title()}</option>
                    % endfor
                    </select>
                </form>
            </div><!-- span4 -->
            <div class="span4">
                <form  action="/searchGeo"  class="form-search search-type" method="POST">
                    <div class="row-fluid"><span id="searchCountrySelect">
                        <i class="icon-globe icon-light"></i>
                        <select name="geoSearchCountry" id="geoSearchCountry" class="geoSearchCountry" onChange="geoSearchCountryChange(); return 1;">
                        <option value="0" selected>Search by Region</option>
                        <option value="United States">United States</option>
                        </span><!-- searchCountrySelect -->
                        </select>
                        <span id="searchCountryButton"></span>
                    </div><!-- row-fluid -->
                    <div class="row-fluid">
                        <span id="searchStateSelect"></span>
                        <span id="searchStateButton"></span>
                    </div>
                    <div class="row-fluid">
                        <span id="searchCountySelect"></span>
                        <span id="searchCountyButton"></span>
                    </div>
                    <div class="row-fluid">
                        <span id="searchCitySelect"></span>
                        <span id="searchCityButton"></span>
                    </div>
                    <div class="row-fluid">
                        <span id="searchPostalSelect"></span>
                        <span id="searchPostalButton">
                    </div>
                </form>
            </div><!-- span4 -->
        </div><!-- row-fluid -->
        <div class="spacer"></div>
    </div><!-- collapse -->
</%def>


<%def name="tabbableSignupLogin(*args)">
    % if c.conf['read_only.value'] == 'true':
      <h1> Sorry, Civinomics is in read only mode right now </h1>
    % else:
        % if 'title' in args:
            <h2 ng-show="showTitle == 'sTitle'" class="no-top centered" ng-cloak>Sign up</h2>
            <h2 ng-show="showTitle == 'lTitle'" class="no-top centered" ng-cloak>Log in</h2>
            <h2 ng-show="showTitle == 'pTitle'" class="no-top centered" ng-cloak>Forgot Password</h2>
        % endif
        ${fields_alert()}
        % if c.splashMsg:
            <div class="col-xs-12">
                <% message = c.splashMsg %>
                <div class="alert alert-${message['type']}">
                    <button data-dismiss="alert" class="close">x</button>
                    <strong>${message['title']}</strong> ${message['content']}
                </div> 
            </div>
        % endif
      ${socialLogins()}
      <div ng-show="showTitle == 'sTitle'" ng-cloak>
        ${signupForm()}
      </div>
      <div ng-show="showTitle == 'lTitle'" ng-cloak>
        ${loginForm()}
      </div>
      <div ng-show="showTitle == 'pTitle'" ng-cloak>
        ${forgotPassword()}
      </div>
    % endif
</%def>

<%def name="socialLogins()">
    <div class="row social-login centered">
        <div id="fbLoginButton2">
            <a href="#" class="fbLogin"><img src="/images/f-login.png"></a>
        </div>
        <div id="twtLoginButton1">
            <a href="/twitterLoginBegin"><img src="/images/t-login.png"></a>
        </div>
    </div>
    <div class="social-sign-in-separator sc-font-light sc-text-light">
        <span>or</span>
    </div>
</%def>

<%def name="signupForm()">
        <form id="sign_in" action="/signup/handler" class="form-horizontal" ng-controller="signupController" name="signupForm" method="POST" role="form">
            <input type="hidden"  name="country" value="United States">
            <input type="hidden" name="memberType" value="professional">

            <div ng-class=" {'form-group': true, 'error': signupForm.name.$error.pattern} ">
                <label class="col-sm-3 control-label" for="name"> Full name: </label>
                <div class="col-sm-8">
                    <input type="text" class="form-control" name="name" id="name" ng-model="fullName" ng-pattern="fullNameRegex" required>
                    <span class="error help-block" ng-show="signupForm.name.$error.pattern" ng-cloak>Use only letters, numbers, spaces, and _ (underscore)</span>
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-3 control-label" for="email"> Email: </label>
                <div class="col-sm-8">
                    <input class="form-control" type="email" name="email" id="email" ng-model="email" required>
                    <span class="error help-block" ng-show="signupForm.email.$error.email" ng-cloak>Not a valid email!</span>
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-3 control-label" for="passphrase"> Password: </label>
                <div class="col-sm-8">
                    <input class="form-control" type="password" name="password" id="passphrase" ng-model= "passphrase1" required>
                </div>
            </div>
            <div ng-class=" {'form-group': true, 'error': signupForm.postalCode.$error.pattern} " ng-cloak>
                <label class="col-sm-3 control-label" for="postalCode"> Zip Code: </label>
                <div class="col-sm-4">
                    <input class="form-control" type="text" name="postalCode" id="postalCode" ng-model="postalCode" ng-pattern="postalCodeRegex" ng-minlength="5" ng-maxlength="5" onBlur="geoCheckPostalCode()" required>
                    <span class="error help-block" ng-show="signupForm.postalCode.$error.pattern" ng-cloak>Invalid zip code!</span>
                    <div id="postalCodeResult"></div>
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-3 control-label" for="terms">&nbsp;</label>
                <div class="col-sm-8">
                    <span id="terms">&nbsp;</span>
                </div>
            </div>
            <div class="form-group text-center">
                <div class="col-sm-6 col-sm-offset-3">
                    <button type="submit" name="submit" class="btn btn-success btn-block btn-lg">Sign up</button>
                </div>
            </div>
        </form>
        <script src="/js/signup.js" type="text/javascript"></script>
        <p class="centered"> Already have an account? <a href="#login" ng-click="switchLoginTitle()" class="green green-hover" data-toggle="tab">Log in</a></p>
</%def>

<%def name="loginForm()">
    <form id="sign_in" action="/loginHandler" class="form-horizontal" method="post">
        <div class="form-group">
            <label class="col-sm-3 control-label" for="email"> Email: </label>
            <div class="col-sm-8">
                <input class="form-control" type="email" name="email" id="email" required>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3  control-label" for="passphrase"> Password: </label>
            <div class="col-sm-8">
                <input class="form-control" type="password" name="password" id="password"><br>
                <a href="#forgot" ng-click="switchPasswordTitle()" data-toggle="tab" class="green green-hover"> Forgot password?</a>
            </div>
        </div>
        <div class="form-group">
            <div class="col-sm-6 col-sm-offset-3">
                <button type="submit" class="btn btn-success btn-lg btn-block"> Log in </button>
            </div>
        </div>
    </form>
    <p class="centered">Don't have an account? <a href="#signup" ng-click="switchSignupTitle()" class="green green-hover" data-toggle="tab">Sign up</a></p>
</%def>

<%def name="forgotPassword()">
    <div class="row-fluid">
        <div class="span8 offset2">
            <p class="centered">Enter your email and click 'Reset Password.' Then check your inbox for your new password.</p>
        </div>
    <form id="forgot_password" action="/forgotPasswordHandler" class="form form-horizontal" method="post">
        <div class="control-group">
            <label class="control-label" for="email"> Email: </label>
            <div class="controls">
                <input type="email" name="email" id="email"><br>
                <a href="#login" ng-click="switchLoginTitle()" data-toggle="tab" class="green green-hover"> Back to log in</a>
            </div>
        </div>
        <div class="control-group">
            <div class="controls">
                <button type="submit" class="btn btn-success"> Reset Password </button>
            </div>
        </div>
    </form>
</%def>

<%def name="signupLoginModal()">
    <!-- Signup Login Modal -->
    <% 
      ####
      #### After Login URL
      ####
      alURL= session._environ['PATH_INFO']
      if 'QUERY_STRING' in session._environ :
        alURL = alURL + '?' + session._environ['QUERY_STRING'] 
      # handles exception with geo pages where angular appends itself to URL
      if '{{' in alURL:
        try:
            alURL = session._environ['HTTP_REFERER']
        except:
            alURL = '/browse/initiatives'
      if 'zip/lookup' in alURL or '/signup' in alURL:
        alURL = '/home'
      session['afterLoginURL'] = alURL
    %>
    <div class="modal fade" id="signupLoginModal" tabindex="-1" role="dialog" aria-labelledby="signupLoginModal" aria-hidden="true" ng-controller="signupController" ng-init="showTitle = 'sTitle'">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h3 ng-show="showTitle == 'sTitle'" class="modal-title login top centered" ng-cloak>Sign up</h3>
                    <h3 ng-show="showTitle == 'lTitle'" class="modal-title login top centered" ng-cloak>Log in</h3>
                    <h3 ng-show="showTitle == 'pTitle'" class="modal-title login top centered" ng-cloak>Forgot Password</h3>
                </div>
                <div class="modal-body">
                    ${tabbableSignupLogin()}
                </div>
                <div class="modal-footer">
                    <div class="row centered tcs">
                      <div class="col-sm-10 col-sm-offset-1">
                        <p class="sc-font-light tcs">By joining, or logging in via Facebook or Twitter, you agree to Civinomics' <a href="/corp/terms" target="_blank" class="green">terms of use</a> and <a href="/corp/privacy" target="_blank" class="green">privacy policy</a></p>
                      </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</%def>


<%def name="activateAccountModal()">
    <div class="modal fade" id="activateAccountModal" tabindex="-1" role="dialog" aria-labelledby="activateAccountModal" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="no-top">Activate Your Account <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button></h3>
                </div>
                <div class="modal-body">
                    <p>You can't add comments, ideas, discussions or resources until you've activated your account.</p>

                    <p>To activate your account, click the link in your activation email from <strong>registration@civinomics.com</strong>. Don't see the email? Check your Spam or Junk folder.</p>
                    <div class="top-space green" id="resendMessage"></div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-default" data-dismiss="modal" aria-hidden="true">Close</button>
                    <button class="btn btn-success resendActivateEmailButton" data-URL-list="user_${c.authuser['urlCode']}_${c.authuser['url']}">Resend Activation Email</button>
                </div>
            </div>
        </div>
    </div>
    <script src="${lib_6.fingerprintFile('/js/activate.js')}" type="text/javascript"></script>
</%def>

