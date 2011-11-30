## -*- coding: utf-8 -*-
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>${c.title} - ${c.conf['custom.titlebar']}</title>

    <link rel="stylesheet" type="text/css" href="/js/markitup/skins/simple/style.css" />
    <link rel="stylesheet" type="text/css" href="/js/markitup/sets/rst/style.css" />

    <link rel=stylesheet HREF="/css/grid.css" TYPE="text/css">
    <link rel=stylesheet HREF="/css/style.css" TYPE="text/css">
    <!--<link rel=stylesheet HREF="/css/style-custom.css" TYPE="text/css">-->
    <link rel=stylesheet HREF="/css/pygments/pygments-tango.css" TYPE="text/css">

    ${self.load_theme()}
    <script type="text/javascript" src="/js/jquery.js"></script>   
    <script type="text/javascript" src="/js/javascript.js"></script>

    <script type="text/javascript" src="/js/markitup/jquery.markitup.js"></script>
    <script type="text/javascript" src="/js/markitup/sets/rst/set.js"></script> 

    <script language="javascript">
        $(document).ready(function()	{
            $('.markitup').markItUp(mySettings);
        });
    </script>
    
    ${self.google_analytics()}

</head>
<body>
    <div id="header"><a href="/">${c.conf['custom.titlebar']}</a></div>
    <div class="container_16">

        <div id="wikibar" class="grid_16">
        ${self.wikibar()}
        </div>

        <div class="clear"></div>

        <div id="content" class="grid_16">
        ${self.flasher()}
        ${next.body()}
        </div> <!-- End div: grid_16 -->

        <div class="clear"></div>

    </div> <!-- End div: container_16 -->

<br><br> 
        <div  id="footer">
        ${self.footer()}
        </div>

</body>
</html>

<%def name="wikibar()">
    <% onTab = request.url.split('/')[3] %>
        % if "user" in session:
        <%namespace file="/lib/mako_lib.mako" import="gravatar, avatar" />
        <div id="wikibar-left" class="grid_10">
            
            <a href="/" ${"class=on" if onTab == "" else ""}>home</a> 
            <a href="/edit/${c.url}" ${"class=on" if onTab == "edit" else ""} >edit</a> 
            <a href="/attach" ${"class=on" if onTab == "attach" else ""} >attach</a> 
            <a href="/revision/${c.url}" ${"class=on" if onTab == "revision" else ""}>revisions</a>
            <a href="/create" ${"class=on" if onTab == "create" else ""}>create</a>
            <a href="/delete/${c.url}" ${"class=on" if onTab == "delete" else ""}>delete</a>
            <a href="/restore" ${"class=on" if onTab == "restore" else ""}>restore</a>
            <a href="/account" ${"class=on" if onTab == "account" else ""}>accounts</a> 
            <a href="/sitemap" ${"class=on" if onTab == "sitemap" else ""}>sitemap</a>
            <a href="/eventlog" ${"class=on" if onTab == "eventlog" else ""}>eventlog</a> 
        </div>
        <div id="wikibar-right" class="grid_6">

             ##<a href="/account/${c.authuser.name}">${gravatar(c.authuser.email, 14)} ${c.authuser.name}</a>
             <a href="/account/${c.authuser.name}">${avatar(c.authuser.pictureHash, 14)} ${c.authuser.name}</a>

             ${c.authuser.pointsObj.points} pts
             <a href="/login/logout">(logout)</a> &nbsp; &nbsp;

            ${h.form(h.url(controller='search', action='handler'), method='put')}
                <input type="text" class="text tiny" id="needle"  name="needle" placeholder="full text search"/>  
                <input type="submit" class="tiny" value="Search" name="submit" id="submit" />
            ${h.end_form()}
        </div>
    % else:
        <div id="wikibar-left" class="grid_10">
            <a href="/" ${"class=on" if onTab == "" else ""}>home</a>
            %if c.conf['public.sitemap'] == 'true': 
                <a href="/sitemap" ${"class=on" if onTab == "sitemap" else ""}>sitemap</a>
            %endif
        </div>
        <div id="wikibar-right" class="grid_6">
            <a href="/login">Login</a>
            % if c.conf['public.reg'] == 'true':
                or <a href="/register">register</a>
            % endif
           
            % if c.conf['public.search'] == 'true':
               &nbsp; &nbsp;
               ${h.form(h.url(controller='search', action='handler'), method='put')}
                  <input type="text" class="text tiny" id="needle"  name="needle" placeholder="full text search" />  
                  <input type="submit" class="tiny" value="Search" name="submit" id="submit" />
                ${h.end_form()}
            % endif
        </div>
    % endif
</%def>

<%def name="footer()">
            ##<a href="http://pylowiki.com">Pylowiki</a>,
            ##<a href="http://pylonshq.com">Pylons</a>, and 
            ##<a href="http://python.org">Python</a> Powered.
            <a href="/contact">Contact Us</a>
</%def>

<%def name="flasher()">
    <% messages = h.flash.pop_messages() %>
    % if messages:
        % for m in messages:
            <p id="flash" class="${m.category}" title="Dismiss this message.">
                    ${m}
            </p>
            <script>
                $("p#flash").fadeIn(800).delay(6000).fadeOut(800);                
                $("p#flash").click(function() {
                    $(this).clearQueue();
                    $(this).fadeOut(800);
                });
            </script>
        % endfor
    % endif
</%def>

<%def name="google_analytics()">
    % if c.conf['google.analytics']:
      <script type="text/javascript">

          var _gaq = _gaq || [];
          _gaq.push(['_setAccount', "${c.conf['google.analytics']}"]);
          _gaq.push(['_trackPageview']);

          (function() {
          var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
          ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
          var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();

      </script>
    % endif
</%def>

<%def name="load_theme()">
    % if c.conf['load.theme']:
    <link rel=stylesheet HREF="/themes/${c.conf['load.theme']}/style.css" TYPE="text/css">
    % endif
</%def>










