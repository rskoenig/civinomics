<%!
    import pylowiki.lib.db.discussion       as discussionLib
    import pylowiki.lib.db.idea             as ideaLib
    import pylowiki.lib.db.comment          as commentLib
    import pylowiki.lib.db.flag             as flagLib
    import pylowiki.lib.db.user             as userLib
    import pylowiki.lib.db.event            as eventLib
    import pylowiki.lib.db.workshop         as workshopLib
    import simplejson as json
%>  
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="admin_event_log()">
    <div class="row-fluid">
        <div class="section-wrapper">
            <div class="browse">
                <h4 class="section-header smaller">Event Log</h4>
                A record of configuration and administrative changes to the workshop.<br />
                <% wEvents = eventLib.getParentEvents(c.w) %>
                <table class="table table-bordered">
                <thead>
                <tr><th>Workshop Events</th></tr>
                </thead>
                <tbody>
                % if wEvents:
                    % for wE in wEvents:
                        <tr><td><strong>${wE.date} ${wE['title']}</strong> ${wE['data']}</td></tr>
                    % endfor
                % endif
                </tbody>
                </table>
            </div><!-- browse -->
        </div><!-- section-wrapper -->
    </div><!-- row-fluid -->
</%def>

<%def name="admin()">
    <div class="row-fluid" ng-controller="adminController">
        <div class="section-wrapper">
            <div class="browse">
                <h4 class="section-header smaller">Civ Admin Panel</h4>
                <form class="form-horizontal" ng-init="code='${c.w['urlCode']}'">
                    <div class="control-group">
                        <label class="control-label" for="setDemo">Set as demo?</label>
                        <div class="controls">
                            <a id="setDemo" class="btn btn-primary" ng-click="setDemo()" href="#">Do it</a>
                            <span class="help-block" ng-show="showResponse">{{response}}</span>
                        </div>
                    </div>
                </form>
            </div><!-- browse -->
        </div><!-- section-wrapper -->
    </div><!-- row-fluid -->
</%def>

<%def name="admin_facilitators()">
    <p>To invite a member to be a listener of, or co-facilitate this workshop, visit their Civinomics profile page and look for the "Invite ..." button!</p>
    <table class="table table-bordered table-condensed" ng-controller="facilitatorController">
        <thead>
            <tr>
                <th>Facilitators</th>
                <th>Email on new items</th>
                <th>Email on flagging</th>
            </tr>
        </thead>
        <tbody>
        <% 
            activeFacilitators = 0
            for f in c.f:
                if f['disabled'] == '0' and f['pending'] == '0':
                    activeFacilitators += 1
        %>
        % for f in c.f:
            <%
                fUser = userLib.getUserByID(f.owner)
                fEvents = eventLib.getParentEvents(f)
                fPending = ""
                if pending in f and f['pending'] == '1':
                    fPending = "(Pending)"
            %>
            <tr>
                <td>
                    <%
                        lib_6.userImage(fUser, className = 'avatar small-avatar')
                        lib_6.userLink(fUser)
                    %>
                    ${fPending}
                </td>
                % if (f['pending'] != '1' and fUser.id == c.authuser.id) or c.privs['admin']:
                    <%
                        itemsChecked = ''
                        flagsChecked = ''
                        if 'itemAlerts' in f and f['itemAlerts'] == '1':
                            itemsChecked = 'checked'
                        if 'flagAlerts' in f and f['flagAlerts'] == '1':
                            flagsChecked = 'checked'
                    %>
                    <td>
                        <form ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${fUser['urlCode']}'" class="no-bottom">
                            <input type="checkbox" name="flagAlerts" value="flags" ng-click="emailOnAdded()" ${itemsChecked}>
                            <span ng-show="emailOnAddedShow">{{emailOnAddedResponse}}</span>
                        </form>
                    </td>
                    <td>
                        <form ng-init="code='${c.w['urlCode']}'; url='${c.w['url']}'; user='${fUser['urlCode']}'" class="no-bottom">
                            <input type="checkbox" name="itemAlerts" value="items" ng-click="emailOnFlagged()" ${flagsChecked}>
                            <span ng-show="emailOnFlaggedShow">{{emailOnFlaggedResponse}}</span>
                        </form>
                    </td>
                % else:
                    <td>${fPending}</td>
                    <td>${fPending}</td>
                % endif
                % if activeFacilitators > 1 and fUser.id == c.authuser.id:
                    </tr><tr><td colspan=3>
                    <form class="form-inline" id="resignFacilitator" name="resignFacilitator" action="/workshop/${c.w['urlCode']}/${c.w['url']}/facilitate/resign/handler/" method="post">
                        Resign as facilitator? &nbsp;&nbsp;Reason: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;
                        <button type="submit" class="btn btn-warning" value="Resign">Resign</button>
                        <br />
                    </form>
                    </td>
                % endif
            </tr>
        % endfor
        </tbody>
    </table>
    % if len(c.df) > 0:
        <table class="table table-bordered">
        <thead>
        <tr><th>Disabled Facilitators</th></tr>
        </thead>
        <tbody>
        % for f in c.df:
            <tr><td>
            <% 
                fUser = userLib.getUserByID(f.owner)
                fEvents = eventLib.getParentEvents(f) 
                lib_6.userImage(fUser, className = 'avatar small-avatar')
                lib_6.userLink(fUser)
            %>
            <br />
            % if fEvents:
                % for fE in fEvents:
                    <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
                % endfor
            % endif
            </tr></td>
        % endfor
        </tbody>
        </table>
    % endif
</%def>

<%def name="admin_listeners()">
    % if c.w['public_private'] != 'trial':
        <div ng-controller="listenerController" ng-init="user='${c.authuser['urlCode']}'; code='${c.w['urlCode']}'; url='${c.w['url']}'; getList()">
        <table class="table table-bordered">
        <thead>
        <tr><th>Officials 
        <button type="button" class="pull-right btn btn-small btn-success" data-toggle="collapse" data-target="#addlistener">
        + Listener
        </button>
        <div id="addlistener" class="collapse">
            <div class="spacer"></div>
            <form id="addListener" ng-submit="saveListener()" class="form-inline" name="addListener">
                New Listener: 
                <input type="text" name="lName" class="input-medium" ng-model="lName" placeholder="Name" required>
                <input type="text" name="lTitle" class="input-medium" ng-model="lTitle" placeholder="Title" required>
                <input type="text" name="lEmail" class="input-medium" ng-model="lEmail" placeholder="Email" required>
                <button type="submit" class="btn btn-warning">Save</button>
                <br />
                <span ng-show="addListenerShow">{{addListenerResponse}}</span>
            </form>
        </div><!-- collapse -->
        </th></th>
        </thead>
        <tbody>
        <tr ng-repeat="listener in listeners">
        <td>
            <a href="{{listener.profileLink}}" class="{{listener.state}}"><img class="avatar small-avatar" src="{{listener.userImage}}"> <span id="listenerName{{listener.urlCode}}">{{listener.lName}}</span>, <span id="listenerTitle{{listener.urlCode}}">{{listener.lTitle}}</span> ({{listener.state}})</a>
            <div class="btn-group pull-right"><button class=" btn btn-small btn-success" data-toggle="collapse" id="toggleButton{{listener.urlCode}}" data-target="#disableListener{{listener.urlCode}}">
            {{listener.button}}</button> <button class="btn btn-small btn-success" data-toggle="collapse" data-target="#editListener{{listener.urlCode}}">
            Edit</button></div><!-- btn-group -->
            <div id="disableListener{{listener.urlCode}}" class="collapse">
                <form id="toggleForm{{listener.urlCode}}" ng-submit="toggleListener('{{listener.urlCode}}')" class="form-inline" name="toggleForm{{listener.urlCode}}">
                <input type="text" name="lReason" ng-model="lReason" placeholder="Reason" required>
                <button type="submit" class="btn btn-warning" id="toggleSubmit{{listener.urlCode}}">{{listener.button}} Listener</button>
                <br />
                <span id="toggleListenerResponse{{listener.urlCode}}"></span>
                </form>
            </div><!-- collapse -->
            <div id="editListener{{listener.urlCode}}" class="collapse">
                <form id="editForm{{listener.urlCode}}" ng-submit="editListener('{{listener.urlCode}}')" class="form-inline" name="editForm{{listener.urlCode}}">
                Edit Listener:<br />
                Name: <input type="text" class="input-small" id="lName" name="lName" value="{{listener.lName}}" required>
                Title: <input type="text" class="input-small" id="lTitle" name="lTitle" value="{{listener.lTitle}}" required>
                Email: <input type="text" class="input-small" id="lEmail" name="lEmail" value="{{listener.lEmail}}" required>
                <button type="submit" class="btn btn-warning">Save Changes</button>
                <br />
                <span id="editListenerResponse{{listener.urlCode}}"></span>
                </form>
            </div><!-- collapse -->
        </td>
        </tr>
        </tbody>
        </table>
        </div><!-- listenerController -->
    % endif
</%def>

<%def name="admin_info()">
    <% wEvents = eventLib.getParentEvents(c.w) %>
    <table class="table table-bordered">
    <thead>
    <tr><th>Workshop Events</th></tr>
    </thead>
    <tbody>
    % if wEvents:
        <br /><br />
        % for wE in wEvents:
            <tr><td><strong>${wE.date} ${wE['title']}</strong> ${wE['data']}</td></tr>
        % endfor
    % endif
    </tbody>
    </table>
    <br /><br />
    <br /><br />
    <table class="table table-bordered">
    <thead>
    <tr><th>Current Facilitators</th></tr>
    </thead>
    <tbody>
    % for f in c.f:
        <% 
            fUser = userLib.getUserByID(f.owner)
            fEvents = eventLib.getParentEvents(f)
            fPending = "" 
        
            if pending in f and f['pending'] == '1':
                fPending = "(Pending)"
        %>
        <tr><td><a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> ${fPending}<br />
        % if fEvents:
          % for fE in fEvents:
          &nbsp; &nbsp; &nbsp; <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
          % endfor
        % endif
        % if c.authuser.id == f.owner and c.authuser.id != c.w.owner:
           <form id="resignFacilitator" name="resignFacilitator" action="/workshop/${c.w['urlCode']}/${c.w['url']}/resignFacilitator" method="post">
               &nbsp; &nbsp; &nbsp;Note: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;
               <button type="submit" class="gold" value="Resign">Resign</button>
           <br />
           </form>
        % endif
        </td></tr>
    % endfor
    </tbody>
    </table>
    <table class="table table-bordered">
    <thead>
    <tr><th>Disabled Facilitators</th></tr>
    </thead>
    <tbody>
    % for f in c.df:
       <% fUser = userLib.getUserByID(f.owner) %>
       <% fEvents = eventLib.getParentEvents(f) %>
       <tr><td><a href="/profile/${fUser['urlCode']}/${fUser['url']}">${fUser['name']}</a> (Disabled)<br />
       % if fEvents:
          % for fE in fEvents:
          &nbsp; &nbsp; &nbsp; <strong>${fE.date} ${fE['title']}</strong>  ${fE['data']}<br />
          % endfor
       % endif
       </tr></td>
    % endfor
    </tbody>
    </table>
    <br /><br />
</%def>

<%def name="marked_items()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Manage Workshop</h4>
            <p>Items that have been flagged, <span class="badge badge-warning">disabled</span>, or <span class="badge badge-success">enabled</span></p>
            ${flaggedItems(c.flaggedItems)}
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="flaggedItems(items)">
    <%
        thisClass = 'tab-pane'
        if active == True:
            thisClass += ' active'
        objectMapping = {'comment': 'Comment', 'discussion':'Conversation', 'idea':'Idea', 'resource':'Resource'}
    %>
    <div class="${thisClass}">
        % if not items:
            <p class="centered">There doesn't appear to be anything here.  Hooray!</p>
        % elif len(items) == 0:
            <p class="centered">There doesn't appear to be anything here.  Hooray!</p>
        % else:
            <table class="table table-bordered table-hover table-condensed">
                <thead>
                    <tr>
                        <th>Flags</th>
                        <th>Author</th>
                        <th>Item</th>
                        <th>Content</th>
                        <th>Action</th> 
                    </tr>
                </thead>
                <tbody>
                    % for item in items:
                        <%
                            rowClass = ''
                            if item['deleted'] == '1' and not c.privs['admin']:
                                continue
                            elif item['deleted'] == '1' and c.privs['admin']:
                                rowClass = 'error'
                                action = 'deleted'
                            elif item['disabled'] == '1':
                                rowClass = 'warning'
                                action = 'disabled'
                            else:
                                action = 'enabled'
                            event = eventLib.getEventForThingWithAction(item, action)
                            if action == 'enabled' and event:
                                rowClass = 'success'
                        %>
                        <tr class="${rowClass}">
                            <td> ${flagLib.getNumFlags(item)} </td>
                            <td>
                                <% 
                                    owner = userLib.getUserByID(item.owner)
                                    lib_6.userImage(owner, className = 'avatar small-avatar')
                                    lib_6.userLink(owner)
                                %>
                            </td>
                            <td> ${objectMapping[item.objType]} </td>
                            <td>
                                % if item.objType != 'comment':
                                    <a ${lib_6.thingLinkRouter(item, c.w)} class="expandable">${item['title']}</a>
                                % else:
                                    <a ${lib_6.thingLinkRouter(item, c.w, id='accordion-%s'%item['urlCode'])} class="expandable">${item['data']}</a>
                                % endif
                            </td>
                            <td>
                                % if event:
                                    <p>
                                    <%
                                        owner = userLib.getUserByID(event.owner)
                                        lib_6.userImage(owner, className = 'avatar small-avatar')
                                        lib_6.userLink(owner)
                                    %>
                                    : ${event['reason']}
                                    </p>
                                % endif
                            </td>
                        </tr>
                    % endfor
                </tbody>
            </table>
        % endif
    </div>
</%def>
