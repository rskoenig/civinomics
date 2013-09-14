<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%! 
    import pylowiki.lib.db.user     as userLib 
    import pylowiki.lib.db.message  as messageLib
    import pylowiki.lib.db.workshop as workshopLib
%>

!
<%def name="mainNavbar()">
    <% tagCategories = workshopLib.getWorkshopTagCategories() %>
    <div class="navbar civ-navbar navbar-fixed-top" style="margin-bottom: 60px;">
        <div class="navbar-inner">
            <div class="container">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </a>
                <a class="brand civ-brand" href="/">
                    <img src="/images/logo_white.png" class="small-logo" id="civinomicsLogo">
                </a>
                <ul class="nav">
                    <li>
                        <button type="button" class="btn btn-warning" data-toggle="collapse" data-target="#search">
                        Search <i class="icon-white icon-search"></i>
                        </button>
                    </li>
                </ul>
                <div class="nav-collapse collapse">
                    <ul class="nav pull-right" id="profileAvatar">
                        <%
                            wSelected = mSelected = pSelected = aSelected = hSelected = ''
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
                            endif
                        %>
                        % if 'user' in session:
                            <li class="${mSelected}">
                                <%
                                    messageCount = ''
                                    numMessages = messageLib.getMessages(c.authuser, read = '0', count = True)
                                    if numMessages:
                                        if numMessages > 0:
                                            messageCount += '<span class="badge badge-warning left-space"> %s</span>' % numMessages
                                %>
                                <a href="/messages/${c.authuser['urlCode']}/${c.authuser['url']}"><i class="icon-envelope icon-white"></i>${messageCount | n}</a>
                            </li>
                            ${lib_6.geoDropdown('navBar')}
                        % endif
                            <li class="${wSelected}">
                                <a href="/workshops">Workshops</a>
                            </li>
                        % if 'user' in session:
                            % if userLib.isAdmin(c.authuser.id):
                                <li class="dropdown ${aSelected}">
                                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">Objects<b class="caret"></b></a>
                                    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                        <li><a tabindex="-1" href="/admin/users">Users</a></li>
                                        <li><a tabindex="-1" href="/admin/workshops">Workshops</a></li>
                                        <li><a tabindex="-1" href="/admin/ideas">Ideas</a></li>
                                        <li><a tabindex="-1" href="/admin/resources">Resources</a></li>
                                        <li><a tabindex="-1" href="/admin/discussions">Discussions</a></li>
                                        <li><a tabindex="-1" href="/admin/comments">Comments</a></li>
                                        <li><a tabindex="-1" href="/admin/photos">Photos</a></li>
                                        <li><a tabindex="-1" href="/admin/flaggedPhotos">Flagged Photos</a></li>
                                    </ul>
                                </li>
                            % endif
                            <li class="dropdown ${pSelected}">
                                <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                    ${lib_6.userImage(c.authuser, className="avatar topbar-avatar", noLink=True)} Me<b class="caret"></b></a>
                                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                    <li><a tabindex="-1" href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">My Profile</a>
                                    <li><a href="/help">Help</a></li>
                                    <li><a tabindex="-1" href="/login/logout">Logout</a></li>
                                </ul>
                            </li>
                        % else:
                            <li class="${hSelected}"><a href="/help">Help</a></li>
                            <li><a href="/login">Login</a></li>
                            <li><a href="/signup">Signup</a></li>
                        % endif
                    </ul>
                </div><!--/.nav-collapse -->
            </div> <!--/.container-->
        </div> <!--/.navbar-inner.civ-navbar -->
    </div> <!-- /.navbar -->
    <div id="search" class="collapse search-white">
        <% tagCategories = workshopLib.getWorkshopTagCategories() %>
        <div class="spacer"></div>
        <div class="spacer"></div>
        <div class="row-fluid">
            <div class="span3 offset1">
                <form class="form-search" action="/search">
                    <div class="input-append">
                        <input type="text" class="span2 search-query" placeholder="Search by word" id="search-input" name="searchQuery">
                    </div>
                </form>
            </div><!-- span3 -->
            <div class="span3">
                <script type="text/javascript">
                    function searchTags() {
                        var sIndex = document.getElementById('categoryTag').selectedIndex;
                        var sValue = document.getElementById('categoryTag').options[sIndex].value;
                        if(sValue) {
                            window.location.pathname = sValue;
                        }
                    }
                </script>
                <form action="/searchTags" class="form-search" method="POST">
                    <select name="categoryTag" id="categoryTag" onChange="searchTags();">
                    <option value="0">Search by category</option>
                    % for tag in tagCategories:
                        <% tagValue = tag.replace(" ", "_") %>
                        <option value="/searchTags/${tagValue}/">${tag.title()}</option>
                    % endfor
                    </select>
                </form>
            </div><!-- span3 -->
            <div class="span5">
                <form  action="/searchGeo"  class="form-search" method="POST">
                    <div class="row-fluid"><span id="searchCountrySelect">
                        <select name="geoSearchCountry" id="geoSearchCountry" class="geoSearchCountry" onChange="geoSearchCountryChange(); return 1;">
                        <option value="0" selected>Search by country</option>
                        <option value="United States">United States</option>
                        </span><!-- searchCountrySelect -->
                        </select>
                    </div><!-- row-fluid -->
                    <div class="row-fluid"><span id="searchCountryButton"></span><span id="searchStateSelect">
                    </span></div>
                    <div class="row-fluid"><span id="searchStateButton"></span><span id="searchCountySelect">
                    </span></div>
                    <div class="row-fluid"><span id="searchCountyButton"></span><span id="searchCitySelect">
                    </span></div>
                    <div class="row-fluid"><span id="searchCityButton"></span><span id="searchPostalSelect">
                    </span></div>
                    <div class="row-fluid"><span id="searchPostalButton">
                    </span></div>
                </form>
            </div><!-- span5 -->
        </div><!-- row-fluid -->
        <div class="spacer"></div>
    </div><!-- collapse -->
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
              <li class="nav-item"><a href="/signup" class="nav-item green green-hover">Sign Up</a></li>
              <li class="nav-item"><a href="/login" class="nav-item green green-hover">Log In</a></li>
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
    </div><!-- kludge for case of missing close div tag -->
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
                </div><!-- span8 -->
                <div class="span pull-right">
                  © 2013 Civinomics
                </div><!-- span pull-right -->
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