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
   
   from hashlib import md5
   import logging, os
   log = logging.getLogger(__name__)
%>
<%namespace name="homeHelpers" file="/lib/derived/6_workshop_home.mako"/>


<%def name="facebookDialogShare(link, picture, **kwargs)">
    <%
        # link: direct url to item being shared
        # picture: url of the parent workshop's background image
        facebookAppId = c.facebookAppId
        channelUrl = c.channelUrl
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
        name = c.name
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
                      description: "Civinomics is an Open Intelligence platform. Collaborate to create solutions."
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

<%def name="emailShare(itemURL, itemCode)">
    % if ('user' in session and c.authuser) and (workshopLib.isPublished(c.w) and workshopLib.isPublic(c.w)):
        <% 
            memberMessage = "You might be interested in this online Civinomics workshop."
        %>
        <a href="#emailShare" role="button" data-toggle="modal" class="listed-item-title"><i class="icon-envelope icon-2x"></i></a>
        <div id="emailShare" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h3 id="myModalLabel">Share This With a Friend</h3>
            </div><!-- modal-header -->
            <div class="modal-body">
                <form ng-controller="shareController" ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${c.authuser['urlCode']}'; itemURL='${itemURL}'; itemCode='${itemCode}'; memberMessage='${memberMessage}'; recipientEmail=''; recipientName=''; shareEmailResponse='';" id="shareEmailForm" ng-submit="shareEmail()" class="form-inline" name="shareEmailForm">
                    Your friend's name:<br>
                    <input type="text" name="recipientName" ng-model="recipientName" required><br />
                    Your friend's email:<br>
                    <input type="text" name="recipientEmail" ng-model="recipientEmail" required><br />
                    Add a message for your friend:<br />
                    <textarea rows="6" class="field span12" ng-model="memberMessage" name="memberMessage">{{memberMessage}}</textarea>
                    <div class="spacer"></div>
                    <button class="btn btn-warning" data-dismiss="modal" aria-hidden="true">Close</button>
                    <button type="submit" class="btn btn-warning">Send Email</button>
                    <br />
                    <span ng-show="shareEmailShow">{{shareEmailResponse}}</span>
                </form>
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
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'])  and not self.isReadOnly():
         <% 
            rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  commentClass = 'voted upVote'
                  voteClass = 'icon-chevron-sign-up icon-2x voted'
               else:
                  commentClass = 'upVote'
                  voteClass = 'icon-chevron-sign-up icon-2x'
            else:
               commentClass = 'upVote'
               voteClass = 'icon-chevron-sign-up icon-2x'
         %>
         % if thing.objType != 'comment':
            <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="${commentClass}">
         % else:
            <a href="/rate/${thing.objType}/${thing['urlCode']}/1" class="${commentClass}">
         % endif
         <i class="${voteClass}"></i>
         </a>
         <br />
         <div class="centered chevron-score"> ${rating}</div>
         <%
            if rated:
               if rated['amount'] == '-1':
                  commentClass = 'voted downVote'
                  voteClass = 'icon-chevron-sign-down icon-2x voted'
               else:
                  commentClass = 'downVote'
                  voteClass = 'icon-chevron-sign-down icon-2x'
            else:
               commentClass = 'downVote'
               voteClass = 'icon-chevron-sign-down icon-2x'
         %>
         % if thing.objType != 'comment':
            <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="${commentClass}">
         % else:
            <a href="/rate/${thing.objType}/${thing['urlCode']}/-1" class="${commentClass}">
         % endif
         <i class="${voteClass}"></i>
         </a>
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
      %>
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'])  and not self.isReadOnly():
         <% 
            if 'vote' in thing and 'amount' in thing['vote']:
                rated = thing['vote']
            else:
                rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  commentClass = 'voted yesVote'
                  displayTally = ''
                  displayPrompt = 'hidden'
               else:
                  commentClass = 'yesVote'
                  displayTally = ''
                  displayPrompt = 'hidden'
                  if rated['amount'] == '0' :
                    displayTally = 'hidden'
                    displayPrompt = ''

            else:
               commentClass = 'yesVote'
               displayTally = 'hidden'
               displayPrompt = ''
         %>
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="${commentClass}">
              <div class="vote-icon yes-icon detail"></div>
              <div class="ynScoreWrapper ${displayTally}"><span class="yesScore">${percentYes}</span>%</div>
         </a>
         <br>
         <br>
         <%
            if rated:
               if rated['amount'] == '-1':
                  commentClass = 'voted noVote'
               else:
                  commentClass = 'noVote'
            else:
               commentClass = 'noVote'
         %>
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/-1" class="${commentClass}">
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
        if c.w['allowIdeas'] == '0' and thing == 'ideas' and not (c.privs['admin'] or c.privs['facilitator']):
            return

        printStr = ''
        btnX = "large"
        if 'small' in args or 'tiny' in args:
            btnX = "small"
      
        if c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['guest']:     
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
   %>
   href="/workshops/${w['urlCode']}/${w['url']}"
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

<%def name="discussionLink(d, w, **kwargs)">
    <%
        if 'workshopCode' in d:
            if 'noHref' in kwargs:
                discussionStr = '/workshop/%s/%s/discussion/%s/%s' %(w["urlCode"], w["url"], d["urlCode"], d["url"])
            else:
                discussionStr = 'href="/workshop/%s/%s/discussion/%s/%s' %(w["urlCode"], w["url"], d["urlCode"], d["url"])
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
      imgStr += '<a href="'
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
            source += '&s=200'
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
        userGeo = getGeoInfo(user.id)[0]
        geoLinkStr = ''
        
        geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'city'), userGeo['cityTitle'])
        geoLinkStr += ', '
        geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'state'), userGeo['stateTitle'])
        if 'comment' not in kwargs:
            geoLinkStr += ', '
            geoLinkStr += '<a %s class="geoLink">%s</a>' %(self._geoWorkshopLink(userGeo, depth = 'country'), userGeo['countryTitle'])
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
    ${immunifyStr | n}
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
    <div class="row-fluid collapse" id="${flagID}">
        <div class="span11 offset1 alert">
            <strong>Are you sure you want to flag this ${thing.objType}?</strong>
            <br />
            <a ${flagThingLink(thing)} class="btn btn-danger flagCommentButton">Yes</a>
            <a class="btn accordion-toggle" data-toggle="collapse" data-target="#${flagID}">No</a>
            <span id = "flagged_${thing['urlCode']}"></span>
        </div>
    </div>
</%def>

<%def name="unpublishThing(thing, **kwargs)">
    <% unpublishID = 'unpublish-%s' % thing['urlCode'] %>
    <div class="row-fluid collapse" id="${unpublishID}">
        <div class="span11 offset1 alert">
            <strong>Are you sure you want to unpublish this ${thing.objType}?</strong>
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
            if 'initiativeCode' in thing and 'resourceCode' not in thing:
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
    %>
    <div class="row-fluid collapse" id="${editID}">
        <div class="span11 offset1">
            <div class="spacer"></div>
            <form action="${editThingLink(thing, embed=True, raw=True)}" ng-controller="editItemController" method="post" class="form" id="edit-${thing.objType}">
                <fieldset>
                <label>Edit</label>
                <span ng-show="editItemShow"><div class="alert alert-danger">{{editItemResponse}}</div></span>
                % if thing.objType == 'comment':
                    <label>Comment text</label>
                    % if ctype == 'initiative' or ctype == 'idea':
                        <div class="row-fluid">
                                <label class="radio inline">
                                    <input type=radio name="commentRole${thing['urlCode']}" value="yes" ${yesChecked}> I support this ${ctype}
                                </label>
                                <label class="radio inline">
                                    <input type=radio name="commentRole${thing['urlCode']}" value="neutral" ${neutralChecked}> Neutral
                                </label>
                                <label class="radio inline">
                                    <input type=radio name="commentRole${thing['urlCode']}" value="no" ${noChecked}> I am against this ${ctype}
                                </label>
                        </div><!-- row-fluid -->
                    % endif
                    <textarea class="comment-reply span12" name="textarea${thing['urlCode']}" required>${thing['data']}</textarea>
                % elif thing.objType == 'idea':
                    <label>Idea title</label>
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title" required>
                    <label>Additional information <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                    <textarea name="text" rows="3" class="input-block-level">${thing['text']}</textarea>
                % elif thing.objType == 'discussion':
                    <label>Topic title</label>
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title" required>
                    <label>Additional information <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                    <textarea name="text" rows="3" class="input-block-level">${text}</textarea>
                % elif thing.objType == 'resource':
                    <label>Resource title</label>
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id="title" required>
                    <label>Resource URL</label>
                    <input type="url" class="input-block-level" name="link" value = "${thing['link']}" id = "link" required>
                    <label>Additional information <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">View Formatting Guide</a></label>
                    <textarea name="text" rows="3" class="input-block-level">${thing['text']}</textarea>
                % endif
                </fieldset>
                <button type="submit" class="btn btn-civ pull-right" name = "submit" value = "reply">Submit</button>
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
    <div class="row-fluid collapse" id="${adminID}">
        <div class="span11 offset1 alert">
            <div class="tabbable"> <!-- Only required for left/right tabs -->
                <ul class="nav nav-tabs">
                    <li class="active"><a href="#disable-${adminID}" data-toggle="tab">Disable</a></li>
                    <li><a href="#enable-${adminID}" data-toggle="tab">Enable</a></li>
                    <li><a href="#immunify-${adminID}" data-toggle="tab">Immunify</a></li>
                    % if thing.objType == 'idea':
                    <li><a href="#adopt-${adminID}" data-toggle="tab">Adopt</a></li>
                    % endif
                    % if c.privs['admin']:
                    <li><a href="#delete-${adminID}" data-toggle="tab">Delete</a></li>
                    % endif
                </ul>
                <div class="tab-content">
                    <div class="tab-pane active" id="disable-${adminID}">
                        <form class="form-inline" action = ${disableThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button type="submit" name="submit" class="btn disableButton" ${disableThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="disableResponse-${thing['urlCode']}"></span>
                    </div>
                    <div class="tab-pane" id="enable-${adminID}">
                        <form class="form-inline" action = ${enableThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button type="submit" name = "submit" class="btn enableButton" ${enableThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="enableResponse-${thing['urlCode']}"></span>
                    </div>
                    <div class="tab-pane" id="immunify-${adminID}">
                        <form class="form-inline" action = ${immunifyThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button type="submit" name = "submit" class="btn immunifyButton" ${immunifyThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="immunifyResponse-${thing['urlCode']}"></span>
                    </div>
                    % if thing.objType == 'idea':
                    <div class="tab-pane" id="adopt-${adminID}">
                        <form class="form-inline" action = ${adoptThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button class="btn adoptButton" type="submit" name="submit" ${adoptThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
                        </form>
                        <span id="adoptResponse-${thing['urlCode']}"></span>
                    </div>
                    % endif
                    % if c.privs['admin']:
                    <div class="tab-pane" id="delete-${adminID}">
                        <form class="form-inline" action = ${deleteThingLink(thing, embed=True, raw=True) | n}>
                            <fieldset>
                                <label>Reason:</label>
                                <input type="text" name="reason" class="span8">
                                <button class="btn deleteButton" type="submit" name="submit" ${deleteThingLink(thing, embed=True) | n}>Submit</button>
                            </fieldset>
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
  <%  categories = workshopLib.getWorkshopTagCategories() %>
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
  <%  categories = workshopLib.getWorkshopTagCategories() %>
  <select class="med-width" ng-model="query">
      <option value=''>All Tags</option>
    % for category in sorted(categories):
      <option value="${category}">${category}</option>
    % endfor
  </select>
</%def>
<%def name="public_tag_links()">
  <%  categories = workshopLib.getWorkshopTagCategories() %>
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
  <a href="#" class="btn btn-mini btn-info" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"><i class="icon-picture"></i> <i class="icon-list"></i> View Formatting Guide</a></label>
</%def>

<%def name="showTags(item)">
    <% 
        colors = workshopLib.getWorkshopTagColouring()
        try:
          tagList = item['tags'].split('|')
        except KeyError:
          tagList = item['workshop_category_tags'].split('|')
        tagList = tagList[:3]
    %>
      % for tag in tagList:
          % if tag and tag != '':
              <% 
                tagClass = colors[tag] 
                tagValue = tag.replace(" ", "_")
              %>
              <a class="label workshop-tag ${tagClass}" href="/searchTags/${tagValue}/" >${tag}</a>
          % endif
      % endfor
</%def>

<%def name="showScope(item)">
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
