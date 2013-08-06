<%!
   from pylowiki.lib.db.geoInfo import getGeoInfo

   import locale
   locale.setlocale(locale.LC_ALL, 'en_US')

   import pylowiki.lib.db.discussion    as discussionLib
   import pylowiki.lib.db.idea          as ideaLib
   import pylowiki.lib.db.resource      as resourceLib
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.rating        as ratingLib
   import pylowiki.lib.db.mainImage     as mainImageLib
   import pylowiki.lib.db.tag           as tagLib
   
   from hashlib import md5
   import logging, os
   log = logging.getLogger(__name__)
%>

<%def name="facebookDialogShare(link)">
    <%
        # NOTE - link should probably be created by the function in this file, thingLinkRouter.
        # However, I need to do some homework on how to strip the href=" " out, and place an
        # http://www.civinomics.com in.
        facebookAppId = c.facebookAppId
        channelUrl = c.channelUrl
    %>
    <div id="fb-root"></div>
    <script src="/js/extauth.js" type="text/javascript"></script>
    <script>
        console.log('before window init');
        window.fbAsyncInit = function() {
            FB.init({
                appId      : "${facebookAppId}", // App ID
                channelUrl : "${channelUrl}", // Channel File
                status     : true, // check login status
                cookie     : false, // enable cookies to allow the server to access the session
                xfbml      : true  // parse XFBML
            });
            console.log('after window init');
            FB.Event.subscribe('auth.authResponseChange', function(response) {
              // Here we specify what we do with the response anytime this event occurs.
              console.log('above response tree');
              if (response.status === 'connected') {
                console.log('calling fb connected');
                //shareOnWall(response.authResponse);
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

        function shareOnWall(authResponse) {
            FB.ui({
                method: "stream.share",
                u: ""
            });
        }
    </script>
    <a href="#" onClick="shareOnWall()"><img src="/images/fb_share2.png"></a>
</%def>

<%def name="emailShare(itemURL, itemCode)">
    % if 'user' in session and c.authuser:
        <% 
            memberMessage = "You might be interested in this online Civinomics workshop."
        %>
        <a href="#emailShare" role="button" class="btn btn-primary btn-mini" data-toggle="modal"><i class="icon-envelope icon-white"></i> Share</a>
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
         <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/login/${thing.objType}" rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nulvote" class="nullvote">
         <!--
         <a href="#" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to make your vote count" id="nulvote" class="nullvote">
         -->
         <i class="icon-chevron-sign-up icon-2x"></i>
         </a>
         <br />
         <div class="centered chevron-score"> ${rating}</div>
         <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/login/${thing.objType}" rel="tooltip" data-placement="right" data-trigger="hover" title="Login to make your vote count" id="nulvote" class="nullvote">
         <!--
         <a href="#" rel="tooltip" data-placement="bottom" data-trigger="hover" title="Login to make your vote count" id="nullvote" class="nullvote">
         -->
         <i class="icon-chevron-sign-down icon-2x"></i>
         </a>
         <br />
         <% log.info("vote") %>
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
      %>
      % if 'user' in session and (c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'])  and not self.isReadOnly():
         <% 
            rated = ratingLib.getRatingForThing(c.authuser, thing) 
            if rated:
               if rated['amount'] == '1':
                  commentClass = 'voted yesVote'
                  displayTally = ''
               else:
                  commentClass = 'yesVote'
                  displayTally = ''
                  if rated['amount'] == '0' :
                    displayTally = 'hidden'

            else:
               commentClass = 'yesVote'
               displayTally = 'hidden'
         %>
         <a href="/rate/${thing.objType}/${thing['urlCode']}/${thing['url']}/1" class="${commentClass}">
           % if 'detail' in args:
              <div class="vote-icon yes-icon detail"></div>
              <div class="yesScore ${displayTally}">${locale.format("%d", totalYes, grouping=True)}</div>
           % else:
              <div class="vote-icon yes-icon detail"></div>
           % endif
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
           % if 'detail' in args:
              <div class="vote-icon no-icon detail"></div>
              <div class="noScore ${displayTally}">${locale.format("%d", totalNo, grouping=True)}</div> 
           % else:
              <div class="vote-icon no-icon"></div>
           % endif
         </a>
         <br>
         <div class="totalVotesWrapper">Total Votes: <span class="totalVotes">${locale.format("%d", totalVotes, grouping=True)}</span></div>
      % else:
         <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/login/${thing.objType}" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to vote" id="nulvote" class="nullvote">
          <div class="vote-icon yes-icon"></div>
         </a>
         <br>
         <br>
         <a href="/workshop/${c.w['urlCode']}/${c.w['url']}/login/${thing.objType}" rel="tooltip" data-placement="top" data-trigger="hover" title="Login to vote" id="nulvote" class="nullvote">
          <div class="vote-icon no-icon"></div>
         </a>
         <br>
         <div class="totalVotesWrapper">Total Votes: <span class="totalVotes">${locale.format("%d", totalVotes, grouping=True)}</span></div>
         <% log.info("vote") %>
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
        if 'small' in args:
            btnX = "small"
      
        if c.privs['participant'] or c.privs['facilitator'] or c.privs['admin'] or c.privs['guest']:     
            printStr = '<a id="addButton" href="/workshop/%s/%s/add/' %(c.w['urlCode'], c.w['url'])
        else:
            printStr = '<a href="/workshop/' + c.w['urlCode'] + '/' + c.w['url'] + '/login/'
            
        if thing == 'discussion':
            printStr += 'discussion" title="Click to add a general conversation topic to this workshop"'
        elif thing == 'resources':
            printStr += 'resource" title="Click to add a resource to this workshop"'
        elif thing == 'ideas':
            printStr += 'idea" title="Click to add an idea to this workshop"'
                
        printStr += ' class="pull-right btn btn-' + btnX + ' btn-civ right-space" type="button"><i class="icon-white icon-plus"></i>'

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
  ${user['greetingMsg']}
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

<%def name="resourceLink(r, w, **kwargs)">
   <%
        if 'directLink' in kwargs:
            if kwargs['directLink'] == True:
                resourceStr = 'href="%s' %(r['link'])
            else:
                resourceStr = 'href="/workshop/%s/%s/resource/%s/%s' %(w["urlCode"], w["url"], r["urlCode"], r["url"])
        else:
            resourceStr = 'href="/workshop/%s/%s/resource/%s/%s' %(w["urlCode"], w["url"], r["urlCode"], r["url"])
        
        resourceStr += commentLinkAppender(**kwargs)
        resourceStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return resourceStr
   %>
   ${resourceStr | n}
</%def>

<%def name="ideaLink(i, w, **kwargs)">
   <%
        ideaStr = 'href="/workshop/%s/%s/idea/%s/%s' %(w["urlCode"], w["url"], i["urlCode"], i["url"])
        ideaStr += commentLinkAppender(**kwargs)
        ideaStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return ideaStr
   %>
   ${ideaStr | n}
</%def>

<%def name="discussionLink(d, w, **kwargs)">
    <%
        discussionStr = 'href="/workshop/%s/%s/discussion/%s/%s' %(w["urlCode"], w["url"], d["urlCode"], d["url"])
        discussionStr += commentLinkAppender(**kwargs)
        discussionStr += '"'
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return discussionStr
    %>
    ${discussionStr | n}
</%def>

<%def name="commentLink(comment, w, **kwargs)">
   <% 
        linkStr = 'href="/workshop/%s/%s/comment/%s"' %(w["urlCode"], w["url"], comment["urlCode"])
        if 'embed' in kwargs:
            if kwargs['embed'] == True:
                return linkStr
   %>
   ${linkStr | n}
</%def>

<%def name="thingLinkRouter(thing, workshop, **kwargs)">
    <%
        if thing.objType == 'revision':
            objType = thing['objType']
        else:
            objType = thing.objType
        if objType == 'discussion':
            return discussionLink(thing, workshop, **kwargs)
        elif objType == 'resource':
            return resourceLink(thing, workshop, **kwargs)
        elif objType == 'idea':
            return ideaLink(thing, workshop, **kwargs)
        elif objType == 'comment':
            if thing.objType == 'revision':
                return commentLink(thing, workshop, **kwargs)
            # set up for member activity feeds in profile.py getMemberPosts  
            if 'ideaCode' in thing.keys():
                idea = ideaLib.getIdea(thing['ideaCode'])
                if not idea:
                    return False
                return ideaLink(idea, workshop, **kwargs)
            elif 'resourceCode' in thing.keys():
                resource = resourceLib.getResourceByCode(thing['resourceCode'])
                if not resource:
                    return False
                return resourceLink(resource, workshop, **kwargs)
            else:
                discussion = discussionLib.getDiscussion(thing['discussionCode'])
                if not discussion:
                    return False
                return discussionLink(discussion, workshop, **kwargs)
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

<%def name="geoDropdown()">
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
      <div class="btn-group pull-right left-space">
        <button class="btn dropdown-toggle" data-toggle="dropdown">
          Sort by Region
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
    % endif
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
            link += '"'
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

<%def name="editThing(thing, **kwargs)">
    <% editID = 'edit-%s' % thing['urlCode'] %>
    <% 
        text = ''
        if 'text' in thing.keys():
            text = thing['text']
    %>
    <div class="row-fluid collapse" id="${editID}">
        <div class="span11 offset1">
            <form action="${editThingLink(thing, embed=True, raw=True)}" method="post" class="form" id="edit-${thing.objType}">
                <label>edit</label>
                % if thing.objType == 'comment':
                    <textarea class="comment-reply span12" name="textarea${thing['urlCode']}">${thing['data']}</textarea>
                % elif thing.objType == 'idea':
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title">
                    <textarea name="text" rows="3" class="input-block-level">${thing['text']}</textarea>
                % elif thing.objType == 'discussion':
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title">
                    <textarea name="text" rows="3" class="input-block-level">${text}</textarea>
                % elif thing.objType == 'resource':
                    <input type="text" class="input-block-level" name="title" value = "${thing['title']}" maxlength="120" id = "title">
                    <input type="text" class="input-block-level" name="link" value = "${thing['link']}">
                    <textarea name="text" rows="3" class="input-block-level">${thing['text']}</textarea>
                % endif
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
                              <% linkStr = '<a %s>%s</a>' %(thingLinkRouter(rev, c.w, embed=True), rev.date) %>
                              <tr>
                                  <td>${linkStr | n}</td>
                                  <td>${userLink(rev.owner)}</td>
                              </tr>
                          % endfor
                      </table>
                  </div>
              </div>
          </div>
    % endif
</%def>

<%def name="showItemInActivity(item, w, **kwargs)">
    <%
        thisUser = userLib.getUserByID(item.owner)
        actionMapping = {   'resource': 'added the resource',
                            'discussion': 'started the conversation',
                            'idea': 'posed the idea',
                            'comment': 'commented on a'}
        objTypeMapping = {  'resource':'resource',
                            'discussion':'conversation',
                            'idea':'idea',
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
        
        activityStr = actionMapping[item.objType]
        # used for string mapping below
        objType = item.objType
        if item.objType == 'comment':
            if 'ideaCode' in item.keys():
                activityStr += 'n'
                objType = 'idea'
            elif 'resourceCode' in item.keys():
                objType = 'resource'
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
  <%  categories = tagLib.getWorkshopTagCategories() %>
  <div class="btn-group pull-right left-space">
    <button class="btn dropdown-toggle" data-toggle="dropdown">
      Sort by Tag
      <span class="caret"></span>
    </button>
    <ul class="dropdown-menu">
        % for category in sorted(categories):
            <li><a href="/searchTags/${category.replace(" ", "_")}/" title="Click to view workshops with this tag">${category.replace(" ", "_")}</a></li>
        % endfor
    </ul> <!-- /.unstyled -->
  </div>
</%def>
