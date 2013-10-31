<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%! 
    import pylowiki.lib.db.user     as userLib 
    import pylowiki.lib.db.message  as messageLib
    import pylowiki.lib.db.workshop as workshopLib
%>

!
<%def name="mainNavbar()">
    <% tagCategories = workshopLib.getWorkshopTagCategories() %>
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
                                <input type="text" class="span2 search-query" placeholder="Search" id="search-input" name="searchQuery">
                                <button type="button" class="btn" data-toggle="collapse" data-target="#search">Options</button>
                            </div>
                        </form>
                    </li>
                </ul>
                <ul class="nav pull-right" id="profileAvatar">
                    <%
                        wSelected = mSelected = pSelected = aSelected = hSelected = homeSelected = ''
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
                        endif
                    %>
                    % if 'user' in session:
                        <li class="${homeSelected} small-hidden">
                            <a href="/">Home</a>
                        </li>
                        <li class="${homeSelected} small-show">
                            <a href="/"><i class="icon-home"></i></a>
                        </li>
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
                                    <li><a tabindex="-1" href="/admin/initiatives">Initiatives</a></li>
                                    <li><a tabindex="-1" href="/admin/flaggedInitiatives">Flagged Initiatives</a></li>
                                </ul>
                            </li>
                        % endif
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                Create <span class="caret"></span>
                            </a>
                            <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                <li><a href="/workshop/display/create/form"> New Workshop</a></li>
                            </ul>
                        </li>

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
                    <li class="small-show">
                        <a type="button" data-toggle="collapse" data-target="#search"><i class="icon-search"></i></a>
                    </li>
                </ul>
            </div> <!--/.container-->
        </div> <!--/.navbar-inner.civ-navbar -->
    </div> <!-- /.navbar -->
    <div id="search" class="collapse search_drawer">
        <% tagCategories = workshopLib.getWorkshopTagCategories() %>
        <div class="spacer"></div>
        <div class="row-fluid searches">
            <div class="span3 offset1">
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
            </div><!-- span3 -->
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
            </div><!-- span5 -->
        </div><!-- row-fluid -->
        <div class="spacer"></div>
    </div><!-- collapse -->
</%def>

<%def name="splashNavbar()">
    <div class="navbar splash-nav">
      <div class="navbar-inner civinomics-splash">
        <div class="container-fluid">
            <a class="brand" href="/"><div class="logo logo-lg" id="civinomicsLogo"></div></a>
            <ul class="nav pull-right">
                <li class="nav-item"><a href="/workshops" class="nav-item">Browse</a></li>
                <li class="nav-item"><a href="/corp/about" class="nav-item">About</a></li>
                <li class="nav-item"><a href="http://civinomics.wordpress.com/" target="_blank" class="nav-item">Blog</a></li>
                <li class="nav-item"><a href="/login" class="nav-item">Log In</a></li>
            </ul>
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

<%def name="condensedFooter()">
    <div class="footer-civ condensed">
        <div class="container-fluid" >
            <div class="row-fluid pretty">
                <div class="span5">
                    <div class="pull-right">
                        © 2013 Civinomics, Inc. 
                        <ul class="horizontal-list">
                            <li><a href="/corp/terms">Terms</a></li>
                            <li><a href="/corp/privacy">Privacy</a></li>
                            <li><a href="/corp/news">News</a></li>
                            <li><a href="/corp/contact">Contact</a></li>
                        </ul>
                    </div>
                </div>
                <div class="span2 centered">
                    <img src="/images/logo_white_simple.png">
                </div>
                <div class="span5">
                    <ul class="horizontal-list">
                        <li><a target="_blank" href="http://www.indiegogo.com/projects/civinomicon-help-us-create-a-paradigm-shift-in-civic-engagement">Fund Us</a></li>
                        <li><a href="/corp/careers">Careers</a></li>
                        <li><a href="/corp/team">Team</a></li>
                        <li><a href="http://www.civinomics.wordpress.com" target="_blank">Blog</a></li>
                        <li><a href="/corp/caseStudies">Case Studies</a></li>
                    </ul>
                </div>
            </div>
            <div class="row-fluid simple">
                <div class="span10">
                    <ul class="horizontal-list">
                        <li><a href="/corp/terms">Terms</a></li>
                        <li><a href="/corp/privacy">Privacy</a></li>
                        <li><a href="/corp/news">News</a></li>
                        <li><a href="/corp/contact">Contact</a></li>
                        <li><a target="_blank" href="http://www.indiegogo.com/projects/civinomicon-help-us-create-a-paradigm-shift-in-civic-engagement">Fund Us</a></li>
                        <li><a href="/corp/careers">Careers</a></li>
                        <li><a href="/corp/team">Team</a></li>
                        <li><a href="http://www.civinomics.wordpress.com" target="_blank">Blog</a></li>
                        <li><a href="/corp/caseStudies">Case Studies</a></li>
                        <li>© 2013 Civinomics, Inc. </li>
                    </ul>
                </div>
                <div class="span2 centered">
                    <img src="/images/logo_white_simple.png">
                </div>
            </div>
            <div class="row-fluid">
                <em class="photo-cred">Cover photo: Occupy Wallstreet, November 11th, 2011. Source: Wikimedia Commons</em>
            </div>
        </div>
    </div>
</%def>