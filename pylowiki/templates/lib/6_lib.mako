<%!
   from pylowiki.lib.db.geoInfo import getGeoInfo

   import locale
   try:
      locale.setlocale(locale.LC_ALL, 'en_US.utf8')
   except: #windows
      locale.setlocale(locale.LC_ALL, 'eng_US')

   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.idea          as ideaLib
   import pylowiki.lib.db.resource      as resourceLib
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.rating        as ratingLib
   import pylowiki.lib.db.mainImage     as mainImageLib
   import pylowiki.lib.db.tag           as tagLib
   import pylowiki.lib.db.workshop      as workshopLib
   import pylowiki.lib.db.photo         as photoLib
   import pylowiki.lib.db.follow        as followLib
   import pylowiki.lib.db.initiative    as initiativeLib
   import pylowiki.lib.utils            as utilsLib
   from pylons import session
   
   import misaka as m
   from hashlib import md5
   import logging, os
   log = logging.getLogger(__name__)
%>
<%namespace name="homeHelpers" file="/lib/derived/6_workshop_home.mako"/>
<%namespace name="ihelpers" file="/lib/derived/6_initiative_home.mako"/>
<%namespace name="ng_helpers" file="/lib/ng_lib.mako"/>

<%def name="facebookDialogShare2(**kwargs)">
    <%
        shareOk = False
        shareOn = False
        if c.facebookShare:
            if c.facebookShare.facebookAppId:
                shareOn = True
                # link: direct url to item being shared
                # picture: url of the parent workshop's background image
                facebookAppId = int(c.facebookShare.facebookAppId)
                #log.info("app id %s and %s"%(c.facebookShare.facebookAppId, facebookAppId))
                channelUrl = c.facebookShare.channelUrl
                thingCode = c.facebookShare.thingCode

                link = c.facebookShare.url
                image = c.facebookShare.image
                #log.info("link %s and image %s"%(link, image))
                userCode = ''

                parentCode = c.facebookShare.parentCode

                # in order to prevent the javascript for these buttons from being included multiple
                # times, these kwargs are now used to activate either or both of the buttons
                if 'shareOnWall' in kwargs:
                    if kwargs['shareOnWall'] is True:
                        shareOnWall = True
                    else:
                        shareOnWall = False
                else:
                    shareOnWall = False

                if 'sendMessage' in kwargs:
                    if kwargs['sendMessage'] is True:
                        sendMessage = True
                    else:
                        sendMessage = False
                else:
                    sendMessage = False
                

                title = c.facebookShare.title
                descriptionLines = c.facebookShare.description.splitlines()
                desc = ""
                for line in descriptionLines:
                    desc += line
                description = desc

                # this is an elaborate way to get the item or workshop's description loaded as the caption
                caption = c.facebookShare.caption
                if c.thing:
                    if 'text' in c.thing.keys():
                        caption = c.thing['text']
                    else:
                        caption = ''
                
                shareOk = c.facebookShare.shareOk

    %>

    % if shareOk and shareOn:
        <div id="fb-root"></div>
        <script src="/js/extauth.js" type="text/javascript"></script>
        <script>
            // activate facebook javascript sdk
            var fbAuthId = '';
            
            window.fbAsyncInit = function() {
                FB.init({
                    appId      : "${facebookAppId}", // App ID
                    channelUrl : "${channelUrl}", // Channel File
                    status     : true, // check login status
                    cookie     : false, // enable cookies to allow the server to access the session
                    xfbml      : true  // parse XFBML
                });
                FB.Event.subscribe('auth.authResponseChange', function(response) {
                // Here we specify what we do with the response anytime this event occurs.
                console.log('above response tree');
                if (response.status === 'connected') {
                    console.log('calling fb connected');
                    fbAuthId = response.authResponse.userID;
                } else if (response.status === 'not_authorized') {
                    console.log('not authd');                
                    //FB.login();
                } else {
                    console.log('else');
                    //FB.login();
                }
                });
            };
            
            // Load the SDK asynchronously
            (function(d){
                var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
                if (d.getElementById(id)) {return;}
                js = d.createElement('script'); js.id = id; js.async = true;
                js.src = "//connect.facebook.net/en_US/all.js";
                ref.parentNode.insertBefore(js, ref);
            }(document));

            function shareOnWall() {
                // grab checked value of checkbox IF it's on the page. add to description.
                //var shareChecked = $("#shareVote").is(':checked');
                
                var shareChecked = false;
                var shareText = '';
                var inputElements = document.getElementsByTagName('input');
                for(var i=0; inputElements[i]; ++i){
                    //console.log("input class: "+inputElements[i].className)
                    if(inputElements[i].className=="shareVote" && inputElements[i].checked) {
                        //console.log("it's checked ")
                        shareChecked = true;
                        break;
                    }
                }
                
                if (shareChecked) {
                    //console.log("share checked")
                    // get the value of the voted button
                    var linkElements = document.getElementsByTagName('a');
                    for(var j=0; linkElements[j]; ++j){
                        //console.log(linkElements[j].className)
                        if(linkElements[j].className=="voted yesVote" || linkElements[j].className=="yesVote voted"){
                            //console.log("HURRAH!")
                            shareText = 'I am in favor of this.';
                            break;
                        } else if(linkElements[j].className=="noVote voted" || linkElements[j].className=="voted noVote") {
                            //console.log("NAH AH!")
                            shareText = 'I am not in favor of this.';
                            break;
                        } else {
                            shareText = 'I have not voted on this yet.';
                        }
                    }
                }
                
                FB.ui(
                    {
                      method: 'feed',
                      name: "${title}",
                      link: "${link}",
                      picture: "${image}",
                      caption: shareText,
                      description: "${description}"
                    },
                    function(response) 
                    {
                        
                        if (response && response.post_id) {
                          // if there's a post_id, create share object
                          var thingCode = "${thingCode}";
                          var link = "${link}"
                          var userCode = fbAuthId;
                          var parentCode = "${parentCode}"
                          
                          //console.log('tc: '+thingCode);
                          //console.log('wc: '+parentCode);

                          result = postShared(response, thingCode, link, response.post_id, userCode, parentCode, 'facebook-wall');
                        }
                    }
                );
            };

            function messageFriends() {
                // there is no callback for messages sent
                // we can simply record that the message dialog was brought up
                // grab checked value of checkbox IF it's on the page. add to description.
                
                var thingCode = "${thingCode}";
                var link = "${link}";
                var userCode = fbAuthId;
                var parentCode = "${parentCode}";
                
                //console.log('tc mf: '+thingCode);
                //console.log('wc mf: '+parentCode);
                          
                result = postShared("no response", thingCode, link, '0', userCode, parentCode, 'facebook-message');
                console.log("3");
                FB.ui(
                    {
                      method: 'send',
                      name: "${title}",
                      link: "${link}",
                      picture: "${image}"
                    }
                );

            };
        
        </script>
        % if 'circle' in kwargs:
            <a href="#" target='_top' onClick="shareOnWall()">
                <span class="icon-stack">
                    <i class="icon-circle icon-stack-base facebook"></i>
                    <i class="icon-facebook icon-light"></i>
                </span>
            </a>
        %else:
            <div class="btn-group facebook">
              % if 'btn' in kwargs:
                <a class="btn dropdown-toggle btn-default" data-toggle="dropdown" href="#">
                  <strong><i class="glyphicon glyphicon-share-alt"></i> Share </strong>
                </a>
              % else:
                <a class="btn dropdown-toggle clear" data-toggle="dropdown" href="#">
                  <i class="icon-facebook-sign icon-2x"></i>
                </a>
              % endif
              <ul class="dropdown-menu share-icons" style="margin-left: -50px;">
                <li>
                  % if shareOnWall:
                    <a href="#" target='_top' onClick="shareOnWall()"><i class="icon-facebook-sign icon"></i> Post to Timeline</a>
                  % endif
                </li>
                <li>
                  % if sendMessage:
                      <a href="#" target='_top' onClick="messageFriends()"><i class="icon-user"></i> Share with Friends</a>
                  % endif
                </li>
              </ul>
            </div>
        % endif
        
        
    % endif
</%def>

<%def name="facebookDialogShare(link, picture, **kwargs)">
    <%
        # link: direct url to item being shared
        # picture: url of the parent workshop's background image
        thingCode = c.thingCode
        if not thingCode:
          thingCode = 'noCode'

        userCode = ''
        if c.w:
            if 'urlCode' in c.w.keys():
                workshopCode = c.w['urlCode']
            else:
                workshopCode = 'noCode'
        else:
            workshopCode = 'noCode'
        # in order to prevent the javascript for these buttons from being included multiple
        # times, these kwargs are now used to activate either or both of the buttons
        if 'shareOnWall' in kwargs:
            if kwargs['shareOnWall'] is True:
                shareOnWall = True
            else:
                shareOnWall = False
        else:
            shareOnWall = False

        if 'sendMessage' in kwargs:
            if kwargs['sendMessage'] is True:
                sendMessage = True
            else:
                sendMessage = False
        else:
            sendMessage = False
        

        # name: the workshop's name or the item's title. This ends up as the name of the object being shared on facebook.
        if 'title' in kwargs:
          name = kwargs['title']
        else:
          name = c.name

        if 'description' in kwargs:
          description = kwargs['description']
        else:
          description = "Civinomics is an Open Intelligence platform. Collaborate to create solutions."

        # this is an elaborate way to get the item or workshop's description loaded as the caption
        if c.thing:
            if 'text' in c.thing.keys():
                caption = c.thing['text']
            else:
                if c.w:
                    if 'description' in c.w.keys():
                        caption = c.w['description'].replace("'", "\\'")
                    else:
                        caption = ''
                else:
                    caption = ''
        else:
            if 'description' in c.w.keys():
                caption = c.w['description'].replace("'", "\\'")
            else:
                caption = ''

        shareOk = False
        if 'photoShare' in kwargs:
            if kwargs['photoShare'] == True:
                shareOk = True
        if c.w:
            if workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w):
                shareOk = True
        if c.initiative:
            if c.initiative['public'] == '1':
                shareOk = True
        log.info("link: "+link)
    %>
    % if shareOk:
        <div id="fb-root"></div>
        <script src="/js/extauth.js" type="text/javascript"></script>
        <script>
            // activate facebook javascript sdk
            var fbAuthId = '';
            window.fbAsyncInit = function() {
                FB.init({
                    appId      : "${facebookAppId}", // App ID
                    channelUrl : "${channelUrl}", // Channel File
                    status     : true, // check login status
                    cookie     : false, // enable cookies to allow the server to access the session
                    xfbml      : true  // parse XFBML
                });
                FB.Event.subscribe('auth.authResponseChange', function(response) {
                // Here we specify what we do with the response anytime this event occurs.
                console.log('above response tree');
                if (response.status === 'connected') {
                    console.log('calling fb connected');
                    fbAuthId = response.authResponse.userID;
                } else if (response.status === 'not_authorized') {
                    console.log('not authd');                
                    //FB.login();
                } else {
                    console.log('else');
                    //FB.login();
                }
                });
            };
        
            // Load the SDK asynchronously
            (function(d){
                var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
                if (d.getElementById(id)) {return;}
                js = d.createElement('script'); js.id = id; js.async = true;
                js.src = "//connect.facebook.net/en_US/all.js";
                ref.parentNode.insertBefore(js, ref);
            }(document));

            function shareOnWall() {
                // grab checked value of checkbox IF it's on the page. add to description.
                //var shareChecked = $("#shareVote").is(':checked');
                var shareChecked = false;
                var shareText = '';
                var inputElements = document.getElementsByTagName('input');
                for(var i=0; inputElements[i]; ++i){
                    //console.log("input class: "+inputElements[i].className)
                    if(inputElements[i].className=="shareVote" && inputElements[i].checked) {
                        //console.log("it's checked ")
                        shareChecked = true;
                        break;
                    }
                }
                
                if (shareChecked) {
                    //console.log("share checked")
                    // get the value of the voted button
                    var linkElements = document.getElementsByTagName('a');
                    for(var j=0; linkElements[j]; ++j){
                        //console.log(linkElements[j].className)
                        if(linkElements[j].className=="voted yesVote" || linkElements[j].className=="yesVote voted"){
                            //console.log("HURRAH!")
                            shareText = 'I am in favor of this.';
                            break;
                        } else if(linkElements[j].className=="noVote voted" || linkElements[j].className=="voted noVote") {
                            //console.log("NAH AH!")
                            shareText = 'I am not in favor of this.';
                            break;
                        } else {
                            shareText = 'I have not voted on this yet.';
                        }
                    }
                }

                FB.ui(
                    {
                      method: 'feed',
                      name: "${name}",
                      link: "${link}",
                      picture: "${picture}",
                      caption: shareText,
                      description: "${description}"
                    },
                    function(response) 
                    {
                        if (response && response.post_id) {
                          // if there's a post_id, create share object
                          var thingCode = "${thingCode}";
                          var link = "${link}"
                          var userCode = fbAuthId;
                          var workshopCode = "${workshopCode}"
                          
                          //console.log('tc: '+thingCode);
                          //console.log('wc: '+workshopCode);

                          result = postShared(response, thingCode, link, response.post_id, userCode, workshopCode, 'facebook-wall');
                        }
                    }
                );
            };

            function messageFriends() {
                // there is no callback for messages sent
                // we can simply record that the message dialog was brought up
                // grab checked value of checkbox IF it's on the page. add to description.
                var thingCode = "${thingCode}";
                var link = "${link}"
                var userCode = fbAuthId;
                var workshopCode = "${workshopCode}"
                
                //console.log('tc mf: '+thingCode);
                //console.log('wc mf: '+workshopCode);
                          
                result = postShared("no response", thingCode, link, '0', userCode, workshopCode, 'facebook-message');
                FB.ui(
                    {
                      method: 'send',
                      name: "${name}",
                      link: "${link}",
                      picture: "${picture}"
                      //description: 'Civinomics is an Open Intelligence platform. Collaborate to create the solutions you need.'
                    }
                );
            };
        
        </script>
        <div class="btn-group facebook">
          % if 'btn' in kwargs:
            <a class="btn dropdown-toggle btn-primary" data-toggle="dropdown" href="#">
              <i class="icon-facebook icon-light right-space"></i> | Share
            </a>
          % else:
            <a class="btn dropdown-toggle clear" data-toggle="dropdown" href="#">
              <i class="icon-facebook-sign icon-2x"></i>
            </a>
          % endif
          <ul class="dropdown-menu share-icons" style="margin-left: -50px;">
            <li>
              % if shareOnWall:
                <a href="#" target='_top' onClick="shareOnWall()"><i class="icon-facebook-sign icon"></i> Post to Timeline</a>
              % endif
            </li>
            <li>
              % if sendMessage:
                  <a href="#" target='_top' onClick="messageFriends()"><i class="icon-user"></i> Share with Friends</a>
              % endif
            </li>
          </ul>
        </div>
        
        
    % endif
</%def>

<%def name="mailToShare(item, **kwargs)">
    <%  
        if 'workshop' in kwargs:
            workshop = kwargs['workshop']
        subj = 'Vote on "' + item['title'] + '"'
        subj = subj.replace(' ','%20')
        if item.objType == 'initiative':
            body = initiativeLink(c.initiative, embed=True, noHref=True, fullURL=True)
        elif item.objType == 'workshop':
            body = workshopLink(item)
        else:
            body = itemInWorkshopLink(item, workshop=workshop)
    %>
    <a class="listed-item-title" target="_blank" href="mailto:?subject=${subj}&body=${body}"><i class="icon-envelope icon-2x"></i></a>
</%def>

<%def name="emailShare(itemURL, itemCode)">
    % if ('user' in session and c.authuser) and (workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w) and not c.privs['provisional']):
        <% 
            memberMessage = "You might be interested in this online Civinomics workshop."
        %>
        <a href="#emailShare${itemCode}" role="button" data-toggle="modal" class="listed-item-title"><i class="icon-envelope icon-2x"></i></a>
    % endif
</%def>

<%def name="emailShareModal(itemURL, itemCode)">
    % if ('user' in session and c.authuser) and (workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w) and not c.privs['provisional']):
        <% 
            memberMessage = "I thought this might interest you!"
        %>
        <div id="emailShare${itemCode}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h3 id="myModalLabel">Share This With a Friend</h3>
            </div><!-- modal-header -->
            <div class="modal-body">
              <div class="row-fluid">
                <form ng-controller="shareController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; itemURL='${itemURL}'; itemCode='${itemCode}'; memberMessage='${memberMessage}'; recipientEmail=''; recipientName=''; shareEmailResponse='';" id="shareEmailForm" ng-submit="shareEmail()" class="form-inline" name="shareEmailForm">
                    <div class="alert" ng-show="shareEmailShow">{{shareEmailResponse}}</div>
                    Your friend's email:<br>
                    <input type="text" name="recipientEmail" ng-model="recipientEmail" required><br>
                    <br>
                    Add a message for your friend:<br />
                    <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>
                    <div class="spacer"></div>
                    <button class="btn btn-danger" data-dismiss="modal" aria-hidden="true">Close</button>
                    <button type="submit" class="btn btn-success">Send Email</button>
                    <br />
                </form>
              </div><!-- row -->
            </div><!-- modal-body -->
        </div><!-- modal -->
    % endif
</%def>

<%def name="validateSession()">
   <%
      if 'user' in session:
         if not c.authuser:
            session.delete()
   %>
</%def>

<%def name="upDownVote(thing)">
   <div class="voteWrapper">
      % if thing['disabled'] == '1' or thing.objType == 'revision':
         </div> <!-- /.voteWrapper -->
         <% return %>
      % endif
      <% rating = int(thing['ups']) - int(thing['downs']) %>
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['provisional'])  and not self.isReadOnly():
         <% 
            rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  voted = "voted"
                  commentClass = 'upVote'
                  voteClass = 'icon-chevron-sign-up icon-2x voted'
               else:
                  voted = ""
                  commentClass = 'upVote'
                  voteClass = 'icon-chevron-sign-up icon-2x'
            else:
               voted = ""
               commentClass = 'upVote'
               voteClass = 'icon-chevron-sign-up icon-2x'
               
            if 'readOnly' in thing:
                readonly = thing['readOnly']
            else:
                readonly = "0"
         %>
         % if readonly == "1":
            <a href="#" class="${voted}" style="color: #b6b6b6">
         % elif thing.objType != 'comment':
            <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="${voted} ${commentClass}">
         % else:
            <a href="/rate/${thing.objType}/${thing['urlCode']}/1" class="${voted} ${commentClass}">
         % endif
         <i class="${voteClass}"></i>
         </a>
         <br />
         <div class="centered chevron-score"> ${rating}</div>
         <%
            if rated:
               if rated['amount'] == '-1':
                  voted = "voted"
                  commentClass = 'downVote'
                  voteClass = 'icon-chevron-sign-down icon-2x voted'
               else:
                  voted = ""
                  commentClass = 'downVote'
                  voteClass = 'icon-chevron-sign-down icon-2x'
            else:
               voted = ""
               commentClass = 'downVote'
               voteClass = 'icon-chevron-sign-down icon-2x'
         %>
         % if readonly == "1":
            <a href="#" class="${voted}" style="color: #b6b6b6">
         % elif thing.objType != 'comment':
            <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="${voted} ${commentClass}">
         % else:
            <a href="/rate/${thing.objType}/${thing['urlCode']}/-1" class="${voted} ${commentClass}">
         % endif
         <i class="${voteClass}"></i>
         </a>
         % if readonly == "1":
            <br /><div class="centered"><small>Voting Complete</small></div>
         % endif
      % else:
         <a href="#signupLoginModal" data-toggle='modal' rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">
         <i class="icon-chevron-sign-up icon-2x"></i>
         </a>
         <br />
         <div class="centered chevron-score"> ${rating}</div>
         <a href="#signupLoginModal" data-toggle='modal' rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">
         <i class="icon-chevron-sign-down icon-2x"></i>
         </a>
         <br />
      % endif
   </div>
</%def>

<%def name="upDownVoteHorizontal(thing)">
      <% rating = int(thing['ups']) - int(thing['downs']) %>
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['provisional'])  and not self.isReadOnly():
         <% 
            rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  voted = "voted"
                  commentClass = 'upVote'
                  voteClass = 'glyphicon glyphicon-chevron-up voted'
               else:
                  voted = ""
                  commentClass = 'upVote'
                  voteClass = 'glyphicon glyphicon-chevron-up'
            else:
               voted = ""
               commentClass = 'upVote'
               voteClass = 'glyphicon glyphicon-chevron-up'
               
            if 'readOnly' in thing:
                readonly = thing['readOnly']
            else:
                readonly = "0"
         %>
         % if readonly == "1":
            <a href="#" class="${voted}" style="color: #b6b6b6">
         % elif thing.objType != 'comment':
            <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="${voted} ${commentClass}">
         % else:
            <a href="/rate/${thing.objType}/${thing['urlCode']}/1" class="${voted} ${commentClass}">
         % endif
         <i class="${voteClass}"></i>
         </a>
         <span class="centered chevron-score"> ${rating}</span>
         <%
            if rated:
               if rated['amount'] == '-1':
                  voted = "voted"
                  commentClass = 'downVote'
                  voteClass = 'glyphicon glyphicon-chevron-down voted'
               else:
                  voted = ""
                  commentClass = 'downVote'
                  voteClass = 'glyphicon glyphicon-chevron-down'
            else:
               voted = ""
               commentClass = 'downVote'
               voteClass = 'glyphicon glyphicon-chevron-down'
         %>
         % if readonly == "1":
            <a href="#" class="${voted}" style="color: #b6b6b6">
         % elif thing.objType != 'comment':
            <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="${voted} ${commentClass}">
         % else:
            <a href="/rate/${thing.objType}/${thing['urlCode']}/-1" class="${voted} ${commentClass}">
         % endif
         <i class="${voteClass}"></i>
         </a>
         % if readonly == "1":
            <span class="centered"><small>Voting Complete</small></span>
         % endif
      % else:
         <a href="#signupLoginModal" data-toggle='modal' rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">
         <i class="icon-chevron-sign-up icon-2x"></i>
         </a>
         <span class="centered chevron-score"> ${rating}</span>
         <a href="#signupLoginModal" data-toggle='modal' rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">
         <i class="icon-chevron-sign-down icon-2x"></i>
         </a>
      % endif
</%def>

<%def name="showPositions(thing)">
    <% 
        pStr = ""
        positions = discussionLib.getPositionsForItem(thing)
    %>
    % for p in positions:
        <% org = userLib.getUserByID(p.owner) %>
        ${userImage(org, className="avatar small-avatar")}
        % if p['position'] == 'support':
            <% pStr += '<a href="/profile/' + p['userCode'] + '/' + p['user_url'] + '">' + p['user_name'] + '</a> supports this initiative.</br>' %>
        % else:
            <% pStr += '<a href="/profile/' + p['userCode'] + '/' + p['user_url'] + '">' + p['user_name'] + '</a> opposes this initiative.</br>' %>
        % endif
    % endfor
    ${pStr | n}                                
</%def>

<%def name="orgPosition(thing)">

    <!-- if org has already made a position statement -->

    <div ng-show="userStatement.support" class="alert alert-success" ng-cloak>Your organization has posted a position statement in support of this {{objType}}.<br><a ng-href="{{userStatement.url}}" target="_blank">View or Edit Position</a></div>

    <div ng-show="userStatement.oppose" class="alert alert-danger" ng-cloak>Your organization has posted a position statement in opposition to this {{objType}}.<br><a ng-href="{{userStatement.url}}" target="_blank">View or Edit Position</a></div>

    <div ng-init="inPage = true;">
        <div ng-controller="yesNoVoteCtrl">
            <div ng-show="userStatement.madeStatement" ng-cloak>
                <small class="grey">{{totalVotes}} votes <span>| <span class="green">{{yesPercent | number:0}}% YES</span> | <span class="red">{{noPercent | number:0}}% NO</span></span></small> 
                <div class="progress" style="height: 12px; margin-bottom: 5px;">
                    <div class="progress-bar" role="progress-bar" style="width: {{100 * totalVotes / goal | number:0}}%;"></div>
                </div>
                <div class="text-right">
                    <small ng-if="item.goal == 100" class="grey clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes needed for this initiative to advance.">{{goal - totalVotes | number:0}} NEEDED</small>
                    <small ng-if="!(item.goal == 100)" class="grey clickable" tooltip-placement="bottom" tooltip-popup-delay="1000" tooltip="Number of votes calculated based on the total voting population of the initiative's scope.">{{goal - totalVotes | number}} NEEDED</small>
                </div>
            </div>
        </div>
    </div>

    <!-- if org has not yet made a position statement -->

    <form role="form" ng-hide="checkingMadeStatement || userStatement.madeStatement" action="/profile/${c.authuser['urlCode']}/${c.authuser['url']}/add/position/handler/${thing['urlCode']}" method="POST" ng-cloak>
        <div class="form-group">
            <label class="radio-inline">
                <input type="radio" name="position" id="positionSupport" value="support" checked>
                Support
            </label>
            <label class="radio-inline">
                <input type="radio" name="position" id="positionOppose" value="oppose">
                Oppose
            </label>
        </div>
        <div class="form-group">
            <label style="font-weight: 400;">
                Statement:
            </label>
            % if not c.privs['provisional']:
                <textarea class="form-control min-textarea" rows="3" name="text" required></textarea>
            % else:
                <a href="#activateAccountModal" data-toggle="modal">
                    <textarea class="form-control min-textarea" rows="3" name="text" required></textarea>
                </a>
            % endif
        </div>
        <div class="text-right">
        % if not c.privs['provisional']:
            <button class="btn btn-success">Submit</button>
        % else:
            <a class="btn btn-success" href="#activateAccountModal" data-toggle="modal">Submit</a>
        % endif
        </div>
    </form>
</%def>

<%def name="yesNoVote(thing, *args)">
   <div class="yesNoWrapper">
      % if thing['disabled'] == '1' or thing.objType == 'revision':
         </div> <!-- /.yesNoWrapper -->
         <% return %>
      % endif
      <% 
        rating = int(thing['ups']) - int(thing['downs']) 
        totalYes = int(thing['ups'])
        totalNo = int(thing['downs'])
        totalVotes = int(thing['ups']) + int(thing['downs'])
        percentYes = percentNo = 0
        if totalVotes > 0:
          percentYes = int(float(totalYes)/float(totalVotes) * 100)
          percentNo = int(float(totalNo)/float(totalVotes) * 100)
        if 'ratings' in session:
            myRatings = session["ratings"]
        else:
            myRatings = {}
            
        if 'readOnly' in thing:
            readonly = thing['readOnly']
        else:
            readonly = "0"
            
      %>
      % if 'user' in session and (c.privs['participant'] or c.privs['provisional']) and not self.isReadOnly() and c.authuser['memberType'] == 'organization':
        ${orgPosition(thing)}
      % elif 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['provisional'])  and not self.isReadOnly():
         <% 
            thingCode = thing['urlCode']
            #log.info("thingCode is %s"%thingCode)
            if thingCode in myRatings:
                myRating = myRatings[thingCode]
            else:
                myRating = "0"
                
            if myRating == '1':
                commentClass = 'voted yesVote'
                displayTally = ''
                displayPrompt = 'hidden'
            else:
                commentClass = 'yesVote'
                displayTally = ''
                displayPrompt = 'hidden'
                if myRating == '0' :
                    displayTally = 'hidden'
                    displayPrompt = ''
                    
            if readonly == '1':
                href = "#"
            else:
                href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/"

            #else:
            #   commentClass = 'yesVote'
            #   displayTally = 'hidden'
            #   displayPrompt = ''
         %>
         <a href="${href}1" class="${commentClass}">
              <div class="vote-icon yes-icon detail"></div>
              <div class="ynScoreWrapper ${displayTally}"><span class="yesScore">${percentYes}</span>%</div>
         </a>
         <br>
         <br>
         <%
            if myRating == '-1':
                commentClass = 'voted noVote'
            else:
                commentClass = 'noVote'
         %>
         <a href="${href}-1" class="${commentClass}">
              <div class="vote-icon no-icon detail"></div>
              <div class="ynScoreWrapper ${displayTally}"><span class="noScore">${percentNo}</span>%</div> 
         </a>
         <br>
         <div class="totalVotesWrapper">
          % if 'detail' in args:
            <span class="orange ${displayPrompt}"><strong>Vote to display rating</strong></span><br>
          % endif
          Total Votes: <span class="totalVotes">${locale.format("%d", totalVotes, grouping=True)}</span>
        </div>
      % else:
         <a href="#signupLoginModal" role="button" data-toggle="modal" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to vote" id="nulvote" class="nullvote">
         <div class="vote-icon yes-icon"></div>
         </a>
         <br>
         <br>
         <a href="#signupLoginModal" role="button" data-toggle="modal" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to vote" id="nulvote" class="nullvote">
         <div class="vote-icon no-icon"></div>
         </a>
         <br>
         <div class="totalVotesWrapper">
          % if 'detail' in args:
            <span class="orange"><strong>Vote to display rating</strong></span><br>
          % endif
          Total Votes: <span class="totalVotes">${locale.format("%d", totalVotes, grouping=True)}</span></div>
      % endif
   </div>
</%def>

<%def name="isReadOnly()">
   <%
      if (c.conf['read_only.value'] == 'true') or (c.conf['read_only.value'] == 'True'):
         return True
      else:
         return False
   %>
</%def>

<%def name="createNew(thing, *args)">
   <%
        if isReadOnly():
            readOnlyMessage(thing)
            return
        if c.w['allowResources'] == '0' and thing == 'resources' and not (c.privs['admin'] or c.privs['facilitator']):
            return
        if c.w['allowIdeas'] == '0' and not (c.privs['admin'] or c.privs['facilitator']):
            return

        printStr = ''
        btnX = "large"
        if 'small' in args or 'tiny' in args:
            btnX = "small"

        if c.privs['provisional']:
            printStr = '<a href="#activateAccountModal" data-toggle="modal"'
      
        elif c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['guest']:     
            printStr = '<a id="addButton" href="/workshop/%s/%s/add/' %(c.w['urlCode'], c.w['url'])

        else:
            printStr = '<a href="#signupLoginModal" data-toggle="modal"'
            
        if thing == 'discussion':
            printStr += 'discussion" title="Click to add a general conversation topic to this workshop"'
        elif thing == 'resources':
            printStr += 'resource" title="Click to add a resource to this workshop"'
        elif thing == 'ideas':
            printStr += 'idea" title="Click to add an idea to this workshop"'
                
        printStr += ' class="pull-right btn btn-' + btnX + ' btn-civ right-space" type="button"><i class="icon-white icon-plus"></i>'

        if not 'tiny' in args:
          if thing == 'discussion':
              printStr += ' Topic'
          elif thing == 'ideas':
              printStr += ' Idea'
          elif thing == 'resources':
              printStr += ' Resource'

        printStr += '</a>'

    %>

    ${printStr | n} 

</%def>

<%def name="readOnlyMessage(thing)">
   <p> Read-only: cannot add a ${thing}. </p>
</%def>

<%def name="userLink(user, **kwargs)">
   <%
      if type(user) == type(1L):
         user = userLib.getUserByID(user)
      elif type(user) == type(u''):
         user = userLib.getUserByCode(user)
      if user.objType == 'facilitator':
         user = userLib.getUserByID(user.owner)
      if user.objType == 'listener':
         user = userLib.getUserByEmail(user['email'])
      if 'raw' in kwargs:
         if kwargs['raw']:
            return '/profile/%s/%s/' %(user['urlCode'], user['url'])
      thisLink = "<a href='/profile/%s/%s/'" %(user['urlCode'], user['url'])
      if 'className' in kwargs:
         thisLink += ' class = "' + kwargs['className'] + '"'
      thisLink += '>'
      if 'title' in kwargs:
         thisTitle = kwargs['title']
      else:
         thisTitle = user['name']
      if 'maxChars' in kwargs:
         thisTitle = ellipsisIZE(thisTitle, kwargs['maxChars'])
      thisLink += thisTitle
      if 'image' in kwargs:
         if kwargs['image'] == True:
            thisLink += userImage(user)
      thisLink += "</a>"
   %>
   ${thisLink | n}
</%def>

<%def name="userGreetingMsg(user)">
  <%
    if type(user) == type(1L):
       user = userLib.getUserByID(user)
    elif type(user) == type(u''):
       user = userLib.getUserByCode(user)
    if user.objType == 'facilitator':
       user = userLib.getUserByID(user.owner)
    if user.objType == 'listener':
       user = userLib.getUserByEmail(user['email'])
  %>
  % if len(user['greetingMsg']) > 0:
    ${ellipsisIZE(user['greetingMsg'], 35)}
  % endif
</%def>

<%def name="workshopLink(w, **kwargs)">
   <%
    if 'embed' in kwargs:
        if kwargs['embed'] == True:
            if 'raw' in kwargs:
                if kwargs['raw'] == True:
                    return "/workshop/%s/%s" %(w['urlCode'], w['url'])
            return 'href = "/workshop/%s/%s"' %(w['urlCode'], w['url'])

    else:
        baseUrl = utilsLib.getBaseUrl()
        return '%s/workshop/%s/%s' % (baseUrl, w['urlCode'], w['url'])
   %>
   href="/workshops/${w['urlCode']}/${w['url']}"
</%def>

<%def name="itemInWorkshopLink(item, **kwargs)">
    <%
        workshop = kwargs['workshop']
        baseUrl = utilsLib.getBaseUrl()
        return '%s/workshop/%s/%s/%s/%s/%s' % (baseUrl, workshop['urlCode'],workshop['url'],item.objType, item['urlCode'], item['url'] )
    %>
</%def>

<%def name="workshopImage(w, **kwargs)">
    <%
      mainImage = mainImageLib.getMainImage(w)
      if 'raw' in kwargs:
         if kwargs['raw'] == True:
            if mainImage['pictureHash'] == 'supDawg':
               return "/images/slide/thumbnail/supDawg.thumbnail"
            elif 'format' in mainImage.keys():
                return "/images/mainImage/%s/thumbnail/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
            else:
               # note: due to a recent slideshow thumbnail bugfix, Todd believes this .jpg should be .png
               return "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
               
      imgStr = '<a href="'
      imgStr += workshopLink(w, embed=True, raw=True)
      if 'linkClass' in kwargs:
         imgStr += '" class="%s"' %(kwargs['linkClass'])
      imgStr += '">'
      if mainImage['pictureHash'] == 'supDawg':
         picturePath = "/images/slide/thumbnail/supDawg.thumbnail"
      elif 'format' in mainImage.keys():
         picturePath = "/images/mainImage/%s/thumbnail/%s.%s" %(mainImage['directoryNum'], mainImage['pictureHash'], mainImage['format'])
      else:
         picturePath = "/images/mainImage/%s/thumbnail/%s.jpg" %(mainImage['directoryNum'], mainImage['pictureHash'])
      title = w['title']
      imgStr += '<img src="%s" alt="%s" title="%s"' %(picturePath, title, title)
         
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      
      imgStr += '></a>'
   %>
   ${imgStr | n}
</%def>

<%def name="commentLinkAppender(**kwargs)">
    ## Small refactoring of the resource/discussion/idea link generation when a comment is involved
    <%
        appendedLink = ''
        if 'id' not in kwargs and 'commentCode' not in kwargs:
            return appendedLink
        if 'id' in kwargs:
            appendedLink = '#%s' % kwargs['id']
        elif 'commentCode' in kwargs:
            appendedLink = '?comment=%s' % kwargs['commentCode']
        return appendedLink
    %>
</%def>

<%def name="resourceLink(r, p, **kwargs)">
   <%
        if 'initiativeCode' in p:
            parentBase = 'initiative'
            parentCode = p['initiativeCode']
            parentURL = p['initiative_url']
        else:
            parentBase = 'workshop'
            parentCode = p['urlCode']
            parentURL = p['url']
            
        if 'directLink' in kwargs:
            if kwargs['directLink'] == True and r['type'] == 'url':
                    resourceStr = 'href="%s' %(r['info'])
            else:
                if 'noHref' in kwargs:
                    resourceStr = '/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
                else:
                    resourceStr = 'href="/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
        else:
            if 'noHref' in kwargs:
                resourceStr = '/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])
            else:
                resourceStr = 'href="/%s/%s/%s/resource/%s/%s' %(parentBase, parentCode, parentURL, r["urlCode"], r["url"])

        resourceStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            resourceStr += ''
        else:
            resourceStr += '"'

        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return resourceStr
   %>
   ${resourceStr | n}
</%def>

<%def name="photoLink(photo, dparent, **kwargs)">
   <%
        photoStr = 'href="/profile/%s/%s/photo/show/%s' %(dparent["urlCode"], dparent["url"], photo["urlCode"])
        
        photoStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            photoStr += ''
        else:
            photoStr += '"'

        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return photoStr
   %>
   ${photoStr | n}
</%def>

<%def name="initiativeLink(initiative, **kwargs)">
   <%
        if 'noHref' in kwargs:
            initiativeStr = '/initiative/%s/%s/show' %(initiative["urlCode"], initiative["url"])
            if 'fullURL' in kwargs:
              baseURL = utilsLib.getBaseUrl()
              initiativeStr = '%s/initiative/%s/%s/show' %(baseURL, initiative["urlCode"], initiative["url"])

        else:
            initiativeStr = 'href="/initiative/%s/%s/show' %(initiative["urlCode"], initiative["url"])
        initiativeStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            initiativeStr += ''
        else:
            initiativeStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return initiativeStr
   %>
   ${initiativeStr | n}
</%def>

<%def name="ideaLink(i, w, **kwargs)">
   <%
        if 'noHref' in kwargs:
            ideaStr = '/workshop/%s/%s/idea/%s/%s' %(w["urlCode"], w["url"], i["urlCode"], i["url"])
        else:
            ideaStr = 'href="/workshop/%s/%s/idea/%s/%s' %(w["urlCode"], w["url"], i["urlCode"], i["url"])
        ideaStr += commentLinkAppender(**kwargs)
        if 'noHref' in kwargs:
            ideaStr += ''
        else:
            ideaStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return ideaStr
   %>
   ${ideaStr | n}
</%def>

<%def name="discussionLink(d, p, **kwargs)">
    <%
        if 'workshopCode' in d and p != None:
            if 'noHref' in kwargs:
                discussionStr = '/workshop/%s/%s/discussion/%s/%s' %(p["urlCode"], p["url"], d["urlCode"], d["url"])
            else:
                discussionStr = 'href="/workshop/%s/%s/discussion/%s/%s' %(p["urlCode"], p["url"], d["urlCode"], d["url"])
            log.info("bout to comment link append")
            discussionStr += commentLinkAppender(**kwargs)
            if 'noHref' in kwargs:
                discussionStr += ''
            else:
                discussionStr += '"'
        elif 'initiativeCode' in d:
            if 'noHref' in kwargs:
                discussionStr = '/initiative/%s/%s/updateShow/%s'%(d['initiativeCode'], d['initiative_url'], d['urlCode'])
            else:
                discussionStr = 'href="/initiative/%s/%s/updateShow/%s"'%(d['initiativeCode'], d['initiative_url'], d['urlCode'])

        elif 'discType' in d and d['discType'] == 'organization_general':
            if 'noHref' in kwargs:
                discussionStr = '/profile/%s/%s/discussion/show/%s'%(d['userCode'], d['user_url'], d['urlCode'])
            else:
                discussionStr = 'href="/profile/%s/%s/discussion/show/%s"'%(d['userCode'], d['user_url'], d['urlCode'])

        else:
            discussionStr = 'href="/discussion/%s/%s"'%(d['urlCode'], d['url'])

        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return discussionStr
    %>
    ${discussionStr | n}
</%def>

<%def name="commentLink(comment, dparent, **kwargs)">
   <% 
        if dparent.objType.replace("Unpublished", "") == 'workshop':
            parentBase = 'workshop'
            commentSuffix = "/comment/%s"%comment['urlCode']
        elif dparent.objType.replace("Unpublished", "") == 'user':
            parentBase = 'profile'
        elif dparent.objType.replace("Unpublished", "") == 'initiative':
            parentBase = 'initiative'
        else:
            parentBase = dparent.objType.replace("Unpublished", "")
            
        if 'noHref' in kwargs:
            linkStr = '/%s/%s/%s/comment/%s' %(parentBase, dparent["urlCode"], dparent["url"], comment["urlCode"])
        else:
            linkStr = 'href="/%s/%s/%s/comment/%s"' %(parentBase, dparent["urlCode"], dparent["url"], comment["urlCode"])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return linkStr
   %>
   ${linkStr | n}
</%def>

<%def name="thingLinkRouter(thing, dparent, **kwargs)">
    <%
        if thing.objType == 'revision':
            objType = thing['objType'].replace("Unpublished", "")
        else:
            objType = thing.objType.replace("Unpublished", "")
            
        #log.info("working on objType %s with id of %s"%(thing.objType, thing.id))
        if objType == 'discussion':
            return discussionLink(thing, dparent, **kwargs)
        elif objType == 'resource':
            #log.info("before resouce link, parent is type %s"%dparent.objType)
            return resourceLink(thing, dparent, **kwargs)
        elif objType == 'idea':
            return ideaLink(thing, dparent, **kwargs)
        elif objType == 'initiative':
            return initiativeLink(thing, **kwargs)
        elif objType == 'comment':
            if thing.objType == 'revision':
                return commentLink(thing, dparent, **kwargs)
            # set up for member activity feeds in profile.py getMemberPosts  
            if 'ideaCode' in thing.keys():
                idea = ideaLib.getIdea(thing['ideaCode'])
                if not idea:
                    return False
                return ideaLink(idea, dparent, **kwargs)
            elif 'resourceCode' in thing.keys():
                resource = resourceLib.getResourceByCode(thing['resourceCode'])
                if not resource:
                    return False
                return resourceLink(resource, dparent, **kwargs)
            elif 'photoCode' in thing.keys():
                photo = photoLib.getPhoto(thing['photoCode'])
                if not photo:
                    return False
                return photoLink(photo, dparent, **kwargs)
            elif 'initiativeCode' in thing.keys():
                initiative = initiativeLib.getInitiative(thing['initiativeCode'])
                if not initiative:
                    return False
                return initiativeLink(initiative, **kwargs)
            else:
                discussion = discussionLib.getDiscussion(thing['discussionCode'])
                if not discussion:
                    return False
                return discussionLink(discussion, dparent, **kwargs)
    %>
</%def>

<%def name="userImage(user, **kwargs)">
    <%
      if type(user) == type(1L):
         user = userLib.getUserByID(user)
      imgStr = ''
      if user.objType == 'facilitator':
         user = userLib.getUserByID(user.owner)
      if user.objType == 'listener':
         user = userLib.getUserByEmail(user['email'])
      imgStr += '<a class="hidden-print" href="'
      imgStr += userLink(user, raw=True)
      imgStr += '"'
      if 'linkClass' in kwargs:
         imgStr += ' class="%s"' %(kwargs['linkClass'])
      if 'rel' in kwargs:
         imgStr += ' rel="%s"' %(kwargs['rel'])
      imgStr += '>'
      if 'revision' in kwargs:
         revision = kwargs['revision']
         title = revision['data']
      else:
         title = user['name']
            
      imageSource = _userImageSource(user, **kwargs)
      imgStr += '<img src="%s" alt="%s" title="%s"' %(imageSource, title, title)
      if 'className' in kwargs:
         imgStr += ' class="%s"' % kwargs['className']
      if 'placement' in kwargs:
         imgStr += ' data-placement="%s"' % kwargs['placement']
      
      imgStr += '></a>'
    %>
    % if 'noLink' in kwargs:
      <img src="${_userImageSource(user, **kwargs)}" class="${kwargs['className']}" alt="${title}" title="${title}">
    % elif 'bgImage' in kwargs:
        <!-- to handle large facebook photos which are not cropped to squares -->
        <div class="avatar avatar-large" style="background-image: url(${_userImageSource(user, **kwargs)}); background-size: cover cover; background-position: center top"></div>

    % else:
    ${imgStr | n}
    % endif
</%def>

<%def name="_userImageSource(user, **kwargs)">
    <%
        # Assumes 'user' is a Thing.
        # Defaults to a gravatar source
        # kwargs:   forceSource:   Instead of returning a source based on the user-set preference in the profile editor,
        #                          we return a source based on the value given here (civ/gravatar)
        source = 'http://www.gravatar.com/avatar/%s?r=pg&d=identicon' % md5(user['email']).hexdigest()
        large = False
        gravatar = True

        if 'className' in kwargs:
            if 'avatar-large' in kwargs['className']:
                large = True
        if 'forceSource' in kwargs:
            if kwargs['forceSource'] == 'civ':
                gravatar = False
                if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                    source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                else:
                    source = '/images/hamilton.png'
            elif kwargs['forceSource'] == 'facebook':
                if large:
                    source = user['facebookProfileBig']
                else:
                    source = user['facebookProfileSmall']
            elif kwargs['forceSource'] == 'twitter':
                source = user['twitterProfilePic']

        else:
            if 'avatarSource' in user.keys():
                if user['avatarSource'] == 'civ':
                    if 'directoryNum_avatar' in user.keys() and 'pictureHash_avatar' in user.keys():
                        source = '/images/avatar/%s/avatar/%s.png' %(user['directoryNum_avatar'], user['pictureHash_avatar'])
                        gravatar = False
                elif user['avatarSource'] == 'facebook':
                    gravatar = False
                    if large:
                        source = user['facebookProfileBig']
                    else:
                        source = user['facebookProfileSmall']
                elif user['avatarSource'] == 'twitter':
                    gravatar = False
                    source = user['twitterProfilePic']

            elif 'extSource' in user.keys():
                # this is needed untl we're sure all facebook connected users have properly 
                # functioning profile pics - the logic here is now handled 
                # with the above user['avatarSource'] == 'facebook': ..
                if 'facebookSource' in user.keys():
                    if user['facebookSource'] == u'1':
                        gravatar = False
                        # NOTE - when to provide large or small link?
                        if large:
                            source = user['facebookProfileBig']
                        else:
                            source = user['facebookProfileSmall']
        if large and gravatar:
            source += '&s=170'
        return source
        %>
</%def>

<%def name="geoBreadcrumbs()">
    <%
        outOfScope = False
        if 'user' in session:
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
            scopeMapping = [    ('earth', 'Earth'),
                            ('country', c.authuser_geo['countryTitle']),
                            ('state', c.authuser_geo['stateTitle']),
                            ('county', county),
                            ('city', city),
                            ('postalCode', c.authuser_geo['postalCode'])
                            ]
    %>
    % if 'user' in session:
      <ul class="nav nav-pills geo-breadcrumbs">
            % for scopeLevel in scopeMapping:
                <%
                    activeClass = ''
                        
                    if c.scope['level'] == scopeLevel[0]:
                        if scopeLevel[0] != 'earth':
                            scopeKey = '%sURL' % scopeLevel[0] 
                            userScope = c.authuser_geo[scopeKey]
                        else:
                            userScope = 'earth'
                        if c.scope['name'] == userScope:
                            activeClass = 'active'
                        else:
                            outOfScope = True
                %>
                <li class="${activeClass}">
                    <a ${self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) | n}>${scopeLevel[1]}</a>
                    % if scopeLevel[0] != 'postalCode':
                        <span class="divider">/</span>
                    % endif
                </li>
            % endfor
        </ul>
    % endif
    <% 
        return outOfScope
    %>
</%def>

<%def name="geoDropdown(*args)">
    <%
        outOfScope = False
        if 'user' in session:
            county = c.authuser_geo['countyTitle']
            city = c.authuser_geo['cityTitle']
            if county == city:
                county = 'County of ' + county
                city = 'City of ' + city
            scopeMapping = [    ('earth', 'Earth'),
                            ('country', c.authuser_geo['countryTitle']),
                            ('state', c.authuser_geo['stateTitle']),
                            ('county', county),
                            ('city', city),
                            ('postalCode', c.authuser_geo['postalCode'])
                            ]
    %>
    % if 'user' in session:
      % if 'navBar' in args:
        ${myPlaces(scopeMapping)}
      % else:
        ${geoButton(scopeMapping)}
      % endif

    % endif
</%def>

<%def name="geoButton(scopeMapping)">
  <div class="btn-group pull-right left-space">
        <button class="btn dropdown-toggle" data-toggle="dropdown">
          Search by Region
          <span class="caret"></span>
        </button>
        <ul class="dropdown-menu">
          % for scopeLevel in scopeMapping:
              <%
                  activeClass = ''
                      
                  if c.scope['level'] == scopeLevel[0]:
                      if scopeLevel[0] != 'earth':
                          scopeKey = '%sURL' % scopeLevel[0] 
                          userScope = c.authuser_geo[scopeKey]
                      else:
                          userScope = 'earth'
                      if c.scope['name'] == userScope:
                          activeClass = 'active'
                      else:
                          outOfScope = True
              %>
              <li class="${activeClass}">
                  <a ${self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) | n}>${scopeLevel[1]}</a>
              </li>
            % endfor
        </ul>
      </div>
</%def>

<%def name="myPlaces(scopeMapping)">
  
  <li class="dropdown">
    <a href="#" class="dropdown-toggle" data-toggle="dropdown">My Places<b class="caret"></b></a>
    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
        % for scopeLevel in scopeMapping:
            <li>
                <a ${self._geoWorkshopLink(c.authuser_geo, depth = scopeLevel[0]) | n}>${scopeLevel[1]}</a>
            </li>
          % endfor
      </ul>
  </li>
</%def>




<%def name="outOfScope()">
    <%
        scopeName = c.scope['level']

        # More mapping for the postal code, this time to display Postal Code instead of just Postal.
        # The real fix for this is through use of message catalogs, which we will need to implement
        # when we support multiple languages in the interface, so for right now this kludge is
        # "good enough" 
        if scopeName == 'postalCode':
            scopeName = 'Postal Code'

        scopeName += " of "
        scopeName += c.scope['name']\
                        .replace('-', ' ')\
                        .title()
    %>
    <div class="alert alert-info span6 offset3">
        <button type="button" class="close" data-dismiss="alert">x</button>
        This page is scoped for the ${scopeName}
    </div>
</%def>

<%def name="userGeoLink(user, **kwargs)">
    <%
        if type(user) == type(1L):
            user = userLib.getUserByID(user)
        if user:
            try:
                userGeo = getGeoInfo(user.id)[0]
                geoLinkStr = ''
                geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'city'), userGeo['cityTitle'])
                geoLinkStr += ', '
                geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'state'), userGeo['stateTitle'])
                if 'comment' not in kwargs:
                    geoLinkStr += ', '
                    geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'country'), userGeo['countryTitle'])
            except:
                geoLinkStr = ''
    %>
    ${geoLinkStr | n}
</%def>

<%def name="_geoWorkshopLink(geoInfo, depth = None, **kwargs)">
    <%
        link = 'href="/workshops/geo/earth/'
        if depth is None or depth == 'earth':
            link += '0"'
        elif depth == 'country':
            link += '%s"' % geoInfo['countryURL']
        elif depth == 'state':
            link += '%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'])
        elif depth == 'county':
            link += '%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'])
        elif depth == 'city':
            link += '%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'])
        elif depth == 'postalCode':
            link += '%s/%s/%s/%s/%s"' % (geoInfo['countryURL'], geoInfo['stateURL'], geoInfo['countyURL'], geoInfo['cityURL'], geoInfo['postalCodeURL'])
        return link
    %>
</%def>

<%def name="disableThingLink(thing, **kwargs)">
    <%
        disableStr = '"/disable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return disableStr
                    return 'href = ' + disableStr
                return 'href = ' + disableStr
        disableStr = 'href = ' + disableStr
    %>
    ${disableStr | n}
</%def>

<%def name="enableThingLink(thing, **kwargs)">
    <%
        enableStr = '"/enable/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return enableStr
                    return 'href = ' + enableStr
                return 'href = ' + enableStr
        enableStr = 'href = ' + enableStr
    %>
    ${enableStr | n}
</%def>

<%def name="immunifyThingLink(thing, **kwargs)">
    <%
        immunifyStr = '"/immunify/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return immunifyStr
                    return 'href = ' + immunifyStr
                return 'href = ' + immunifyStr
        immunifyStr = 'href = ' + immunifyStr
    %>
    ${immunifyStr | n}
</%def>

<%def name="adoptThingLink(thing, **kwargs)">
    <%
        adoptStr = '"/adopt/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return adoptStr
                    return 'href = ' + adoptStr
                return 'href = ' + adoptStr
        adoptStr = 'href = ' + adoptStr
    %>
    ${adoptStr | n}
</%def>

<%def name="promoteThingLink(thing, **kwargs)">
    <%
        author = userLib.getUserByID(thing.owner)
        promoteStr = '"/initiative/%s/%s/promoteIdea"' %(author['urlCode'], author['url'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return promoteStr
                    return 'href = ' + promoteStr
                return 'href = ' + promoteStr
        promoteStr = 'href = ' + promoteStr
    %>
    ${promoteStr | n}
</%def>


<%def name="deleteThingLink(thing, **kwargs)">
    <%
        deleteStr = '"/delete/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return deleteStr
                    return 'href = ' + deleteStr
                return 'href = ' + deleteStr
        deleteStr = 'href = ' + deleteStr
    %>
    ${deleteStr | n}
</%def>

<%def name="flagThingLink(thing, **kwargs)">
    <%
        flagStr = '"/flag/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return flagStr
                    return 'href = ' + flagStr
                return 'href = ' + flagStr
        flagStr = 'href = ' + flagStr
    %>
    ${flagStr | n}
</%def>

<%def name="unpublishThingLink(thing, **kwargs)">
    <%
        unpublishStr = '"/unpublish/%s/%s"' %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return unpublishStr
                    return 'href = ' + unpublishStr
                return 'href = ' + unpublishStr
        unpublishStr = 'href = ' + unpublishStr
    %>
    ${unpublishStr | n}
</%def>

<%def name="publishThingLink(thing, **kwargs)">
    <%
        publishStr = '"/publish/%s/%s"' %(thing.objType.replace("Unpublish", ""), thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return publishStr
                    return 'href = ' + publishStr
                return 'href = ' + publishStr
        publishStr = 'href = ' + publishStr
    %>
    ${publishStr | n}
</%def>

<%def name="editThingLink(thing, **kwargs)">
    <%
        editStr = "/edit/%s/%s" %(thing.objType, thing['urlCode'])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                if 'raw' in kwargs:
                    if kwargs['raw'] == True:
                        return editStr
                    return 'href = ' + editStr
                return 'href = ' + editStr
        editStr = 'href = ' + editStr
    %>
    ${editStr | n}
</%def>

<%def name="flagThing(thing, **kwargs)">
    <% flagID = 'flag-%s' % thing['urlCode'] %>
    <div class="row collapse" id="${flagID}">
        <div class="col-sm-11 col-sm-offset-1 alert">
            <strong>Are you sure you want to flag this ${thing.objType}?</strong>
            <br />
            <a ${flagThingLink(thing)} class="btn btn-danger flagCommentButton">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#${flagID}">No</a>
            <span id = "flagged_${thing['urlCode']}"></span>
        </div>
    </div>
</%def>

<%def name="flagThingAngular()">
    <div class="row collapse" id="flag-{{item.urlCode}}">
        <div class="col-sm-11 col-sm-offset-1 alert">
            <strong>Are you sure you want to flag this {{item.objType}}</strong>
            <br />
            <a href="/flag/{{item.objType}}/{{item.urlcode}}" class="btn btn-danger flagCommentButton">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#flag-{{item.urlCode}}">No</a>
            <span id = "flagged_{{item.urlCode}}"></span>
        </div>
    </div>
</%def>

<%def name="unpublishThing(thing, **kwargs)">
    <% unpublishID = 'unpublish-%s' % thing['urlCode'] %>
    <div class="row-fluid collapse" id="${unpublishID}">
        <div class="span11 offset1 alert">
            <strong>Are you sure you want to send this ${thing.objType} to the trash?</strong>
            <br />
            <a ${unpublishThingLink(thing)} class="btn btn-danger">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#${unpublishID}">No</a>
            <span id = "unpublish_${thing['urlCode']}"></span>
        </div>
    </div>
</%def>

<%def name="publishThing(thing, **kwargs)">
    <% publishID = 'publish-%s' % thing['urlCode'] %>
    <div class="row-fluid collapse" id="${publishID}">
        <div class="span11 offset1 alert">
            <strong>Are you sure you want to publish this ${thing.objType.replace("Unpublished", "")}?</strong>
            <br />
            <a ${publishThingLink(thing)} class="btn btn-danger">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#${publishID}">No</a>
            <span id = "publish_${thing['urlCode']}"></span>
        </div>
    </div>
</%def>

<%def name="editThing(thing, **kwargs)">

    <% editID = 'edit-%s' % thing['urlCode'] %>
    <% 
        text = ''
        if 'text' in thing.keys():
            text = thing['text']
            
        ctype = ""
        if thing.objType == 'comment':
            if c.discussion and c.discussion['discType'] == 'organization_position':
                ctype = "regular"
            elif 'initiativeCode' in thing and 'resourceCode' not in thing:
                ctype = "initiative"
            elif 'ideaCode' in thing:
                ctype = "idea"
            else:
                ctype = "reguar"

            yesChecked = ""
            noChecked = ""
            neutralChecked = ""
            
            if ctype != "regular":
                if 'commentRole' in thing:
                    if thing['commentRole'] == 'yes':
                        yesChecked = 'checked'
                    elif thing['commentRole'] == 'no':
                        noChecked = 'checked'
                    else:
                        neutralChecked = 'checked'
                else:
                    neutralChecked = 'checked'
        if thing.objType == 'discussion' and 'position' in thing:
            supportChecked = ""
            opposeChecked = ""
            if thing['position'] == 'support':
                supportChecked = 'checked'
            else:
                opposeChecked = 'checked'
            ctype = ""
            if 'initiativeCode' in thing:
                ctype = 'initiative'
            elif 'ideaCode' in thing:
                ctype = 'idea'
    %>
    <div class="row collapse" id="${editID}">
        <div class="col-xs-12">
            <div class="spacer"></div>
            <form action="${editThingLink(thing, embed=True, raw=True)}" ng-controller="editItemController" method="post" class="form" id="edit-${thing.objType}">
                % if thing.objType == 'comment':
                    % if ctype == 'initiative' or ctype == 'idea':
                        <div class="row">
                            <div class="col-sm-12">
                                <span class="radio inline">
                                    <input type=radio name="commentRole${thing['urlCode']}" value="yes" ${yesChecked}> Pro
                                </span>
                                <span class="radio inline">
                                    <input type=radio name="commentRole${thing['urlCode']}" value="neutral" ${neutralChecked}> Neutral
                                </span>
                                <span class="radio inline">
                                    <input type=radio name="commentRole${thing['urlCode']}" value="no" ${noChecked}> Con
                                </span>
                            </div>
                        </div>
                    % endif
                    <textarea class="comment-reply col-sm-10 form-control" name="textarea${thing['urlCode']}" required>${thing['data']}</textarea>
                % elif thing.objType == 'idea':
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" class="input-block-level form-control" name="title" value = "${thing['title']}" maxlength="120" id = "title" required>
                    </div>
                    <div class="form-group">
                        <label>Additional nformation <a href="#" class="btn btn-xs btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                        <textarea name="text" rows="3" class="input-block-level form-control">${thing['text']}</textarea>
                    </div>
                % elif thing.objType == 'discussion':
                    <div class="form-group">
                        <label>Topic title</label>
                        <input type="text" class="input-block-level form-control" name="title" value = "${thing['title']}" maxlength="120" id = "title" required>
                    </div>
                    % if 'position' in thing:
                        <div class="form-group">
                            <label class="radio inline">
                                <input type=radio name="position" value="support" ${supportChecked}> We support this ${ctype}
                            </label>
                            <label class="radio inline">
                                <input type=radio name="position" value="oppose" ${opposeChecked}> We oppose this ${ctype}
                            </label>
                        </div><!-- row-->
                    % endif
                    <div class="form-group">
                        <label>Additional information <a href="#" class="btn btn-xs btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                        <textarea name="text" rows="3" class="input-block-level form-control">${text}</textarea>
                    </div>
                % elif thing.objType == 'resource':
                    <div class="form-group">
                        <label>Resource title</label>
                        <input type="text" class="input-block-level form-control" name="title" value = "${thing['title']}" maxlength="120" id="title" required>
                    </div>
                    <div class="form-group">
                        <label>Resource URL</label>
                        <input type="url" class="input-block-level form-control" name="link" value = "${thing['link']}" id = "link" required>
                    </div>
                    <div class="form-group">
                        <label>Additional information <a href="#" class="btn btn-xs btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                        <textarea name="text" rows="3" class="input-block-level form-control">${thing['text']}</textarea>
                    </div>
                % endif
                <div class="form-group">
                    <button type="submit" class="btn btn-primary pull-right" name = "submit" value = "reply">Submit</button>
                </div>
            </form>
        </div>
    </div>
</%def>

<%def name="adminThing(thing, **kwargs)">
    <% 
        if thing.objType == 'revision':
            return
        adminID = 'admin-%s' % thing['urlCode']
    %>
    <div class="row collapse" id="${adminID}">
        <div class="col-sm-11 col-sm-offset-1 alert">
            <div class="tabbable"> <!-- Only required for left/right tabs -->
                <ul class="nav nav-tabs">
                    <li class="active"><a href="#disable-${adminID}" data-toggle="tab">Disable</a></li>
                    <li><a href="#enable-${adminID}" data-toggle="tab">Enable</a></li>
                    <li><a href="#immunify-${adminID}" data-toggle="tab">Immunify</a></li>
                    % if thing.objType == 'idea':
                    <li><a href="#adopt-${adminID}" data-toggle="tab">Adopt</a></li>
                    <li><a href="#promote-${adminID}" data-toggle="tab">Promote</a></li>
                    % endif
                    % if c.privs['admin']:
                    <li><a href="#delete-${adminID}" data-toggle="tab">Delete</a></li>
                    % endif
                </ul>
                <div class="spacer"></div>
                <div class="tab-content">
                    <div class="tab-pane active" id="disable-${adminID}">
                        <form class="form-inline" action = ${disableThingLink(thing, embed=True, raw=True) | n}>
                            <div class="form-group">
                                <label for="reason">Reason:</label>
                                <input type="text" name="reason" class="form-control">
                                <button type="submit" name="submit" class="btn btn-default disableButton" ${disableThingLink(thing, embed=True) | n}>Submit</button>
                            </div>
                        </form>
                        <span id="disableResponse-${thing['urlCode']}"></span>
                    </div>
                    <div class="tab-pane" id="enable-${adminID}">
                        <form class="form-inline" action = ${enableThingLink(thing, embed=True, raw=True) | n}>
                            <div class="form-group">
                                <label>Reason:</label>
                                <input type="text" name="reason" class="form-control">
                                <button type="submit" name = "submit" class="btn btn-default enableButton" ${enableThingLink(thing, embed=True) | n}>Submit</button>
                            </div>
                        </form>
                        <span id="enableResponse-${thing['urlCode']}"></span>
                    </div>
                    <div class="tab-pane" id="immunify-${adminID}">
                        <form class="form-inline" action = ${immunifyThingLink(thing, embed=True, raw=True) | n}>
                            <div class="form-group">
                                <label>Reason:</label>
                                <input type="text" name="reason" class="form-control">
                                <button type="submit" name = "submit" class="btn btn-default immunifyButton" ${immunifyThingLink(thing, embed=True) | n}>Submit</button>
                            </div>
                        </form>
                        <span id="immunifyResponse-${thing['urlCode']}"></span>
                    </div>
                    % if thing.objType == 'idea':
                    <div class="tab-pane" id="adopt-${adminID}">
                        <form class="form-inline" action = ${adoptThingLink(thing, embed=True, raw=True) | n}>
                            <div class="form-group">
                                <label>Reason:</label>
                                <input type="text" name="reason" class="form-control">
                                <button class="btn btn-default adoptButton" type="submit" name="submit" ${adoptThingLink(thing, embed=True) | n}>Submit</button>
                            </div>
                        </form>
                        <span id="adoptResponse-${thing['urlCode']}"></span>
                    </div>
                    % endif
                    % if thing.objType == 'idea':
                    <div class="tab-pane" id="promote-${adminID}">
                        <form class="form-inline" action = ${promoteThingLink(thing, embed=True, raw=True) | n}>
                            <div class="form-group">

                                <input type="hidden" name="initiativeTitle" value="${thing['title']}">
                                <input type="hidden" name="initiativeDescription" value="${thing['text']}">

                                <%
                                    if 'scope' in thing:
                                        scope = thing['scope']
                                    elif 'workshop_public_scope' in thing:
                                        scope = thing['workshop_public_scope']
                                    else: 
                                        scope = None
                                %>
                                <input type="hidden" name="initiativeRegionScope" value="${scope}">
                                <%
                                    if 'workshopCode' in thing:
                                        workshopCode = thing['workshopCode']
                                    else:
                                        workshopCode = None
                                %>
                                <input type="hidden" name="workshopCode" value="${workshopCode}">
                                <%
                                    if 'tags' in thing:
                                        tags = thing['tags']
                                    elif 'workshop_category_tags' in thing:
                                        tags = thing['workshop_category_tags']
                                    else:
                                        tags = None
                                %>
                                <input type="hidden" name="tags" value="${tags}">

                                <label>Reason:</label>
                                <input type="text" name="reason" class="form-control">
                                <button class="btn btn-default adoptButton" type="submit" name="submit" ${promoteThingLink(thing, embed=True) | n}>Submit</button>
                            </div>
                        </form>
                        <span id="promoteResponse-${thing['urlCode']}"></span>
                    </div>
                    % endif
                    % if c.privs['admin']:
                    <div class="tab-pane" id="delete-${adminID}">
                        <form class="form-inline" action = ${deleteThingLink(thing, embed=True, raw=True) | n}>
                            <div class="form-group">
                                <label>Reason:</label>
                                <input type="text" name="reason" class="form-control">
                                <button class="btn btn-default deleteButton" type="submit" name="submit" ${deleteThingLink(thing, embed=True) | n}>Submit</button>
                            </div>
                        </form>
                        <span id="deleteResponse-${thing['urlCode']}"></span>
                    </div>
                    % endif
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="ellipsisIZE(string, numChars, **kwargs)">
    <%
        if numChars > len(string):
            return string
        else:
            return string[:numChars] + "..."
    %>
</%def>

<%def name="fields_alert()">
    % if 'alert' in session:
        <% 
            alert = session['alert']
            if 'type' not in alert.keys() or 'title' not in alert.keys() or 'content' not in alert.keys():
                # Something went wrong...clear and ignore the alert
                session.pop('alert')
                session.save()
                return
        %> 
        <div class="alert alert-${alert['type']}">
            <button data-dismiss="alert" class="close">x</button>
            <strong>${alert['title']}</strong>
            ${alert['content']}
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
    % endif
</%def>

<%def name="revisionHistory(revisions, parent)">
    % if revisions:
        <div class="accordion" id="revision-wrapper">
            <div class="accordion-group no-border">
                <div class="accordion-heading">
                    <a class="accordion-toggle green green-hover" data-toggle="collapse" data-parent="#revision-wrapper" href="#revisionsTable-${parent['urlCode']}">
                        <small>Click to show revisions</small>
                    </a>
                </div>
                <div id="revisionsTable-${parent['urlCode']}" class="accordion-body collapse">
                    <div class="accordion-inner no-border">
                        <table class="table table-hover table-condensed">
                            <tr>
                                <th>Revision</th>
                                <th>Author</th>
                            </tr>
                            % for rev in revisions:
                                <% 
                                    if c.w:
                                        dparent = c.w
                                    elif c.initiative:
                                        dparent = c.initiative
                                    elif c.user:
                                        dparent = c.user
                                    elif c.thing:
                                        dparent = c.thing
                                    else:
                                        dparent = None
                                    linkStr = '<a %s>%s</a>' %(thingLinkRouter(rev, dparent, embed=True), rev.date) 
                                %>
                                <tr>
                                    <td>${linkStr | n}</td>
                                    <td>${userLink(rev.owner)}</td>
                                </tr>
                            % endfor
                        </table>
                    </div><!-- accordian-inner -->
                </div><!-- accordian-body -->
            </div><!-- accordian-group -->
        </div><!-- accordian -->
    % endif
</%def>

<%def name="showItemInActivity(item, w, **kwargs)">
    <%
        thisUser = userLib.getUserByID(item.owner)
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'update': 'added an initiative progress report',
                            'idea': 'posed the idea',
                            'initiative': 'launched the initiative',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
                            'initiative':'initiative',
                            'comment':'comment'}
        eclass = ""
        if 'expandable' in kwargs:
            if kwargs['expandable']:
                eclass=' class="expandable"'
                if item.objType == 'comment':
                    title = item['data']
                else:
                    title = item['title']
            else:
                if item.objType == 'comment':
                    title = ellipsisIZE(item['data'], 40)
                else:
                    title = ellipsisIZE(item['title'], 40)
        else:
            if item.objType == 'comment':
                title = ellipsisIZE(item['data'], 40)
            else:
                title = ellipsisIZE(item['title'], 40)
        
        if item.objType == 'discussion' and item['discType'] == 'update':
            activityStr = actionMapping['update']
        else:
            activityStr = actionMapping[item.objType]
        # used for string mapping below
        objType = item.objType
        if item.objType == 'comment':
            if 'ideaCode' in item.keys():
                activityStr += 'n'
                objType = 'idea'
            elif 'resourceCode' in item.keys():
                objType = 'resource'
            elif 'initiativeCode' in item.keys():
                objType = 'initiative'
            elif item.keys():
                objType = 'discussion'
            
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + '>' + objTypeMapping[objType]
            activityStr += '</a>, saying '
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True, commentCode=item['urlCode']) + eclass + '>' + title + '</a>'
        else:
            activityStr += ' <a ' + thingLinkRouter(item, w, embed = True) + eclass + '>' + title + '</a>'
    %>
    ${activityStr | n}
</%def>

<%def name="fingerprintFile(path)">
    <%
        # Adds a fingerprint so we can cache-bust the browser if the file is modified
        prefix = 'pylowiki/public'
        modTime = os.stat(prefix + path).st_mtime
        return "%s?t=%s" %(path, modTime)
    %>
</%def>

<%def name="public_tags()">
  <%  categories = tagLib.getTagCategories() %>
  <div class="btn-group pull-right left-space">
    <button class="btn dropdown-toggle" data-toggle="dropdown">
      Search by Tag
      <span class="caret"></span>
    </button>
    <ul class="dropdown-menu">
        % for category in sorted(categories):
            <li><a href="/searchTags/${category.replace(" ", "_")}/" title="Click to view workshops with this tag">${category.replace(" ", "_")}</a></li>
        % endfor
    </ul> <!-- /.unstyled -->
  </div>
</%def>

<%def name="public_tag_filter()">
  <%  categories = tagLib.getTagCategories() %>
  <select class="med-width" ng-model="query">
      <option value=''>All Tags</option>
    % for category in sorted(categories):
      <option value="${category}">${category}</option>
    % endfor
  </select>
</%def>

<%def name="public_tag_list_filter()">
  <%  categories = tagLib.getTagCategories() %>
      <li ng-class="{active: query == ''}"><a href="" ng-click="query = '' ">All Categories</a></li>
    % for category in sorted(categories):
      <li ng-class="{active: query == '${category}'}"><a href="#" ng-click="query = '${category}' ">${category}</a></li>
    % endfor
</%def>

<%def name="public_tag_links()">
  <%  categories = tagLib.getTagCategories() %>
    % for category in sorted(categories):
      <a href="/searchTags/${category}">${category}</a><br>
    % endfor
</%def>

<%def name="bookmarkOptions(user, workshop)">
  <% f = followLib.getFollow(user, workshop) %>
    % if f:
      <%
          itemsChecked = ''
          digestChecked = ''
          if 'itemAlerts' in f and f['itemAlerts'] == '1':
              itemsChecked = 'checked'
          if 'digest' in f and f['digest'] == '1':
              digestChecked = 'checked'
      %>
      <div class="btn-group pull-right" ng-controller="followerController" ng-init="code='${workshop['urlCode']}'; url='${workshop['url']}'; user='${user['urlCode']}'">
        <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
          <i class="icon-envelope"></i>
          <span class="caret"></span>
        </a>
        <ul class="dropdown-menu bookmark-options">
          <li>Email on:</li>
          <li>
            <label class="checkbox">
              <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnAdded()" ${itemsChecked}> New Items
            </label>
          </li>
          <li>
            <label class="checkbox">
              <input type="checkbox" name="digest" value="items" ng-click="emailDigest()" ${digestChecked}> Daily Digest
            </label>
          </li>
        </ul>
      </div>
    % endif
</%def>

<%def name="listBookmarks(bookmarked, ltitle)">
  <table class="table table-hover table-condensed no-bottom">
    % for item in bookmarked:
      <tr>
        <td>
            <div class="media profile-workshop" style="overflow:visible;">
                <a class="pull-left" ${workshopLink(item)}>
                  <div class="thumbnail tight media-object" style="height: 60px; width: 90px; margin-bottom: 5px; background-image:url(${workshopImage(item, raw=True) | n}); background-size: cover; background-position: center center;"></div>
                </a>
                <div class="media-body" style="overflow:visible;">
                  <a ${workshopLink(item)} class="listed-item-title media-heading lead bookmark-title">${item['title']}</a>
                    % if ltitle == 'Facilitating' or ltitle == 'Author' or userLib.isAdmin(c.authuser.id):
                      <a class="btn pull-right" href="/workshop/${item['urlCode']}/${item['url']}/preferences"><strong>Edit Workshop</strong></a> &nbsp;
                    % else:
                      % if ltitle == 'Bookmarked':
                        ${homeHelpers.watchButton(item, following = True)}
                      % endif
                      ${bookmarkOptions(c.authuser, item)}
                    % endif
                    <br>
                    % if item['public_private'] == 'public':
                      <span class="grey">Workshop for</span> ${showScope(item) | n}
                    % else:
                      <span class="grey">Private Workshop</span>
                    % endif
                </div>
            </div>
        </td>
      </tr>
    % endfor
  </table>
</%def>

<%def name="formattingGuide()">
  <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-picture"></i> <i class="icon-list"></i> View Formatting Guide</a>
</%def>

<%def name="showTags(item)">
    <% 
        try:
          tagList = item['tags'].split('|')
        except KeyError:
          tagList = item['workshop_category_tags'].split('|')
        tagList = tagList[:3]
    %>
      % for tag in tagList:
          % if tag and tag != '':
              <% 
                tagValue = tag.replace(" ", "_")
              %>
              <span> / </span><a class="label label-default workshop-tag ${tagValue}" href="/searchTags/${tagValue}/" >${tag}</a>
          % endif
      % endfor
</%def>

<%def name="showSubcategoryTags(item)">
    <% 
        try:
          tagList = item['subcategory_tags'].split('|')
        except (KeyError, AttributeError):
            return ""
    %>
      % for tag in tagList:
          % if tag and tag != '':
              <% 
                tagValue = tag.replace(" ", "_")
              %>
              <span> / </span><a class="label label-default workshop-tag ${tagValue}" href="/searchTags/${tagValue}/" >${tag}</a>
          % endif
      % endfor
</%def>

<%def name="showSubcategoryTagsJSON(tL)">
    <% 
        tagList = tl.split('|')
    %>
      % for tag in tagList:
          % if tag and tag != '':
              <% 
                tagValue = tag.replace(" ", "_")
              %>
              <span> / </span><a class="label label-default workshop-tag ${tagValue}" href="/searchTags/${tagValue}/" >${tag}</a>
          % endif
      % endfor
</%def>

<%def name="showScope(item)">
    <%  
        try:
          try:
            log.info(item['scope'])
            scopeList = item['scope']
          except KeyError:
            scopeList = item['workshop_public_scope']
        except:
          scopeList = "0|0|0|0|0|0|0|0|0|0"


        log.info(scopeList)
        scopeList = scopeList.split('|')
        country = scopeList[2].replace("-", " ")
        state = scopeList[4].replace("-", " ")
        county = scopeList[6].replace("-", " ")
        city = scopeList[8].replace("-", " ")
        postalCode = scopeList[9]
        scopeString = ""
        if country == '0':
            scopeString = 'Planet Earth'
        elif state == '0':
            scopeString = 'Country of %s' %country.title()
        elif county == '0':
            scopeString = 'State of %s' %state.title()
        elif city == '0':
            scopeString = 'County of %s'%county.title()
        elif postalCode == '0':
            scopeString += 'City of %s'%city.title()
        else:
            scopeString += 'Zip Code %s</span>'%postalCode
    %>
    <span class="badge badge-info">${scopeString | n}</span>
</%def>

<%def name="showFullScope(item)">
    <%  
        try:
          try:
            
            scopeList = item['scope']
          except KeyError:
            scopeList = item['workshop_public_scope']
        except:
          scopeList = "0|0|0|0|0|0|0|0|0|0"


        scopeList = scopeList.split('|')
        country = scopeList[2].replace("-", " ")
        state = scopeList[4].replace("-", " ")
        county = scopeList[6].replace("-", " ")
        city = scopeList[8].replace("-", " ")
        postalCode = scopeList[9]
        if country == '0':
            scopeString = '<span class="badge badge-info">Planet Earth</span>'
        else:
            scopeString = "Planet Earth"
            if state == '0':
                scopeString += ', <span class="badge badge-info">Country of %s</span>'%country.title()
            else:
                scopeString += ', Country of %s'%country.title()
                if county == '0':
                    scopeString += ', <span class="badge badge-info">State of %s</span>'%state.title()
                else:
                    scopeString += ', State of %s'%state.title()
                    if city == '0':
                        scopeString += ', <span class="badge badge-info">County of %s</span>'%county.title()
                    else:
                        scopeString += ', County of %s'%county.title()
                        if postalCode == '0':
                            scopeString += ', <span class="badge badge-info">City of %s</span>'%city.title()
                        else:
                            scopeString += ", City of %s"%city.title()
                            scopeString += ', <span class="badge badge-info">Zip code of %s</span>'%postalCode
    %>
    ${scopeString | n}
</%def>

<%def name="initiativeImage(i)">
  <%
    if 'directoryNum_photos' in i and 'pictureHash_photos' in i:
      imgURL = "/images/photos/" + i['directoryNum_photos'] + "/thumbnail/" + i['pictureHash_photos'] + ".png" 
    else:
      imgURL = "/images/icons/generalInitiative.jpg"
  %>

  <a ${initiativeLink(i)}>
      <div style="height:80px; width:110px; background-image:url('${imgURL}'); background-repeat:no-repeat; background-size:cover; background-position:center;"/></div>
  </a>
</%def>

<%def name="create(**kwargs)">
    <% 
    if 'createClass' in kwargs:
        createClass = kwargs['createClass']
    else:
        createClass = 'well-grey'
    %>
    <div ng-controller="createController" ng-cloak>
        <div class="media well ${createClass} search-listing">
            <div class="row">
                <div class="col-xs-12">
                    <span class="glyphicon glyphicon-remove pull-right" ng-if="showAll" ng-click="changeShowAll()">
                    </span>

                    <div class="row">
                        <div class="col-xs-12" style="display: inline-block">

                            <label>Add <span ng-show="phase">{{thing}}: &nbsp;</span></label>
                            <select ng-model="thing" ng-show="!(phase)" ng-change="showAll = true">
                                <option ng-repeat="objType in thingList" ng-value="objType">{{objType}}</option>
                            </select>    

                        </div>   
                    </div>

                    ###Basic
                    % if 'user' in session:
                        <form enctype="multipart/form-data" action="/create/{{thing}}/${c.authuser['urlCode']}/${c.authuser['url']}" method="POST">     
                    % else:
                        <form>
                    % endif

                    <input class="form-control ng-pristine ng-valid" type="text" ng-click="showAll = true" ng-model="title" placeholder="{{thing}} Title" name="title" required style="margin-bottom:8px;"></input>  

                    <div ng-show="thing == 'Resource'">
                        <input class="form-control ng-pristine ng-valid" ng-if="showAll" type="text" ng-model="link" placeholder="Link - http://" style="margin-bottom:8px;" name="link" ng-required="thing == 'Resource'"></input> 
                    </div>

                    <div class="form-group">
                        <textarea ng-if="showAll"  class="form-control ng-pristine ng-valid" rows="4" type="text" ng-model="description" placeholder="{{thing}} Description" name="description"></textarea>
                    </div>
            
                    <div ng-show="showAll">
                        % if not 'parentCode' in kwargs:
                            <hr>
                            <div class="col-xs-5" ng-show="geoScope == ''">
                                <label>Geographic Scope</label>
                                ${ng_helpers.ngGeoSelect()}
                            </div>
                            <div class="col-xs-5">
                                <label>Category Tag</label><br>
                                <select name="tags" ng-model="tag">
                                    <option value="">Select One</option>
                                    % for tag in c.tagList:
                                        <option value="${tag}"> ${tag}</option>
                                    % endfor
                                </select>
                            </div>
                        % endif
                    </div>

                    ###Conditional Fields
                    <div ng-if="thing == 'Workshop' && showAll">
                        <label>Privacy level</label>
                        <select ng-model="workshopAccess" name="privacy" required>
                            <option value=""></option>
                            <option value="public">Public</option>
                            <option value="private">Private</option>
                        </select>
                    </div>
            
                    <div ng-show="false" class="col-xs-12">
                        <label>Deadline</label>
                        <div class="row-">
                            <div class="col-xs-6">
                                <p class="input-group">
                                    <input type="text" class="form-control" datepicker-popup="{{format}}" ng-model="date" is-open="opened" min="minDate" max="'2015-06-22'" datepicker-options="dateOptions" date-disabled="disabled(date, mode)" close-text="Close" />
                                    <span class="input-group-btn">
                                        <button class="btn btn-default" ng-click="open($event)"><i class="icon-calendar"></i></button>
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="col-xs-12" ng-show="thing == 'Initiative' || thing == 'Workshop'" ng-if="showAll">
                        <hr>
                        <label>Photos</label>
                        <h5>ID Photo</h5>
                        <input type="file" name="avatar[]" id="imgAvatar" />
                        <img style="display:none;" id="avatarPreview" name="avatarPreview" src="#" alt="your {{thing}} image" ng-required="thing=='Initiative'"/>
                        <div ng-show="thing == 'Initiative'">
                            <h5>Cover Photo</h5>
                            <input type='file' id="imgCover" name="cover[]" />
                            <img style="display:none;" id="coverPreview" name="coverPreview" src="#" alt="your cover image" />
                        </div>
                    </div>

                    ###Extra info (hidden)
                    <input ng-if="scope != ''" type="hidden" name="geoScope" value="{{scope}}" \>
                    <input ng-if="geoScope != ''" type="hidden" name="geoScope" value="{{geoScope}}" \>
                    <input type="hidden" name="deadline" value="{{date}}" \>
                    % if 'parentCode' in kwargs:
                        <input type="hidden" name="parentCode" value="${kwargs['parentCode']}" \>
                    % endif
                    % if 'parentObjType' in kwargs:
                        <input type="hidden" name="parentObjType" value="${kwargs['parentObjType']}" \>
                    % endif
                    % if 'returnTo' in kwargs:
                        <input type="hidden" name="returnTo" value="${kwargs['returnTo']}" \>
                    % endif
                </div><!-- col-xs-12 -->
            </div><!-- row -->

            <div ng-show="showAll" class="form-group text-right">
                % if 'user' in session:
                    <button type="submit" class="btn btn-large btn-success">Submit</button>
                % else:
                    <a href="#signupLoginModal" role="button" data-toggle="modal"><button type="submit" class="btn btn-large btn-success">Submit</button></a>
                % endif
            </div>
            </form> 
        </div><!-- media-well -->
    </div><!-- ng-controller -->
</%def>

<%def name="zipLookup()">
    <div ng-init="zipValue = ${c.postalCode}">
        <div ng-controller="zipLookupCtrl" ng-cloak>
          <i class="icon-spinner icon-spin icon-2x" ng-show="loading" ng-cloak></i>
          <div class="row" ng-show="!loading">
            <div class="col-sm-12 col-xs-3">
                <a class="flag-filter" ng-click="getAllActivity()" tooltip-placement="right" tooltip="Home"><img class="thumbnail flag bottom-space full-width" src="/images/flags/homeFlag.gif" ng-class="{activeGeo : geoScope === geo.scope, inactiveGeo: geo.scope != '' && geoScope}"></a>
            </div>
            <div class="col-sm-12 col-xs-3" ng-repeat="geo in geos">
                <a class="flag-filter" ng-click="getGeoScopedActivity(geo.scope, geo.fullName, geo.flag, geo.population, geo.href, geo.photo)" tooltip-placement="right" tooltip="{{geo.name}}"><img class="thumbnail flag full-width bottom-space" src="{{geo.flag}}" ng-class="{activeGeo : geoScope === geo.scope, inactiveGeo: geo.scope != '' && geoScope}"></a>
            </div>
            <div class="col-sm-12 col-xs-3">
                <div class="btn-group" ng-show="!loading">
                    <a class="btn clear dropdown-toggle flag-filter" data-toggle="dropdown" href="#">
                      <i class="grey icon-search centered"></i>
                    </a>
                    <ul class="dropdown-menu" >
                      <li class="dropdown-form">
                        <p>Look up a zip code</p>
                        <form class="form-inline" name="zipForm">
                          <div ng-class=" {'error': zipForm.zipValue.$error.pattern} " ng-cloak>
                              <input class="input-small form-control" type="number" name="zipValue" id="zipValue" ng-model="zipValue" ng-pattern="zipValueRegex" ng-minlength="5" ng-maxlength="5" placeholder="{{zipValue}}" ng-cloak>
                              <button class="btn btn-primary top-space" ng-click="lookup()">Search</button><br>
                              <span class="error help-block" ng-show="zipForm.zipValue.$error.pattern" ng-cloak>Invalid zip code!</span>
                          </div>
                        </form>
                      </li>
                    </ul>
                </div>
            </div>

          </div><!-- row -->
          
        </div><!-- ng-controller ziplookup-->
    </div><!-- ng-init -->
</%def>

<%def name="commentFooterAngular()">
    ########################################################################
    ##
    ## Displays the {reply, flag, edit, admin} buttons
    ## 
    ## comment          ->  The comment Thing
    ## author           ->  The owner of the comment (a user Thing)
    ##
    ########################################################################
    <div class="row hidden-print">
        <div class="col-xs-12">
            <div class="btn-group">
                % if 'user' in session and not c.privs['provisional']:
                        <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#reply-{{item.urlCode}}">reply</a>
                        <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#flag-{{item.urlCode}}">flag</a>
                        % if c.privs['facilitator'] or c.privs['admin']:
                            <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#edit-{{item.urlCode}}">edit</a>
                        % endif
                    % if c.privs['facilitator'] or c.privs['admin']:
                        <a class="btn btn-default btn-xs panel-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
                    % endif
                % elif not c.privs['provisional']:
                    <a class="btn btn-default btn-xs panel-toggle" data-toggle="modal" data-target="#signupLoginModal">reply</a>
                    <a class="btn btn-default btn-xs panel-toggle" data-toggle="modal" data-target="#signupLoginModal">flag</a>
                % endif
            </div>
        </div><!--/.col-sm-11.offset1-->
    </div><!--/.row-->
    
    ## Reply
    <div class="row collapse" id="reply-{{item.urlCode}}">
        <div class="col-sm-11 col-sm-offset-1">
            <form action="/comment/add/handler" method="post" id="commentAddHandler_reply">
                <textarea name="comment-textarea" class="comment-reply col-sm-12 form-control" placeholder="Add a reply..."></textarea>
                <input type="hidden" name="parentCode" value="{{item.urlCode}}" />
                <input type="hidden" name="thingCode" value = "{{$parent.urlCode}}" />
                <button type="submit" class="btn btn-primary left-space" name = "submit" value = "reply">Submit</button>
            </form>
        </div>
    </div>
    
    ## Flag
    ${flagThingAngular()}
    
    % if 'user' in session:
        ## Edit
        % if c.privs['admin'] or c.privs['facilitator']:
            EDIT DOESNT WORK
        % endif
    
        ## Admin
        % if c.privs['facilitator'] or c.privs['admin']:
            ADMIN DOESNT WORK EITHER
        % endif
    % endif
</%def>