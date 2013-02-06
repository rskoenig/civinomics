<%!
    import pylowiki.lib.db.discussion       as discussionLib
    import pylowiki.lib.db.idea             as ideaLib
    import pylowiki.lib.db.comment          as commentLib
    import pylowiki.lib.db.flag             as flagLib
    import pylowiki.lib.db.user             as userLib
    import pylowiki.lib.db.event            as eventLib
%>  
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="admin_show()">
	<div class="row-fluid">
        <h4 class="section-header smaller">Facilitator Tools</h4>
        <%doc>
        ## MOTD isn't being displayed anywhere yet.
	    <form name="admin_issue" id="admin_issue" class="form-inline" action="/workshop/${c.w['urlCode']}/${c.w['url']}/adminWorkshopHandler" enctype="multipart/form-data" method="post" >
        <strong>Message to Participants:</strong>
        <p>This is displayed on the workshop landing page. Use this to welcome members to the workshop or to make announcements.</p>
        <textarea name="motd" rows="2" cols="80">${c.motd['data']}</textarea>
        &nbsp; &nbsp;
        <% 
            if c.motd['enabled'] == '1':
                pChecked = 'checked'
                uChecked = ''
            else:
                pChecked = ''
                uChecked = 'checked'
        %>
        <input type="radio" name="enableMOTD" value="1" ${pChecked}> Publish Message&nbsp;&nbsp;&nbsp;<input type="radio" name="enableMOTD" value="0" ${uChecked}> Unpublish Message
        <br /><br />
        </%doc>
        % if c.w['startTime'] != '0000-00-00':
            % if c.w['deleted'] == '1':
                <strong>Publish Workshop</strong><br />
                This republishes the workshop, displaying it in lists of active workshops. It may be unpublished again later.<br />
                <% eAction = 'Publish' %>
            % else:
                <strong>Unpublish Workshop</strong><br />
                This unpublishes the workshop, removing it from lists of active workshops. It may be republished again later.<br />
                <% eAction = 'Unpublish' %>
            % endif
            Reason: <input type="text" name="eventReason" id="eventReason"> &nbsp; &nbsp;
            <input type="radio" name="enableWorkshop" value="1"> ${eAction}&nbsp;&nbsp;&nbsp;<input type="radio" name="verifyEnableWorkshop" value="0"> Verify ${eAction}
        % endif
        <br /><br />
        <button type="submit" class="btn btn-warning">Save All Changes</button>
        </form>
    </div><!-- row-fluid -->
</%def>

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
                    <br /><br />
                    % for wE in wEvents:
                        <tr><td><strong>${wE.date} ${wE['title']}</strong> ${wE['data']}</td></tr>
                    % endfor
                % endif
                </tbody>
                </table>
            </div><!-- browse -->
        </div><!-- section-wrapper -->
    <div><!-- row-fluid -->
</%def>


<%def name="admin_facilitators()">
    % if c.w['public_private'] != 'trial':
       <p>To invite a member to be a listener of, or co-facilitate this workshop, visit their Civinomics profile page and look for the "Invite ..." button!</p>
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
            % if len(c.f) > 1 and fUser.id == c.authuser.id:
                <form id="resignFacilitator" name="resignFacilitator" action="/workshop/${c.w['urlCode']}/${c.w['url']}/facilitate/resign/handler/" method="post">
                    &nbsp; &nbsp; &nbsp;Note: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;
                    <button type="submit" class="gold" value="Resign">Resign</button>
                    <br />
                </form>
            % endif
            </td></tr>
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
                <% 
                    fUser = userLib.getUserByID(f.owner)
                    fEvents = eventLib.getParentEvents(f) 
                %>
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
        % endif
    % endif
</%def>

<%def name="admin_listeners()">
    % if c.w['public_private'] != 'trial':
        <table class="table table-bordered">
        <thead>
        <tr><th>Current Listeners</th></tr>
        </thead>
        <tbody>
        % for listener in c.listeners:
            <%
                lUser = userLib.getUserByCode(listener['userCode'])
                lEvents = eventLib.getParentEvents(listener)
                lPending = ""
                if listener['pending'] == '1':
                    lPending = "(Pending)"
            %>
            <tr><td><a href="/profile/${lUser['urlCode']}/${lUser['url']}">${lUser['name']}</a> ${lPending}<br />
            <form id="resignListener" class="well form-inline" name="resignListener" action="/workshop/${c.w['urlCode']}/${c.w['url']}/listener/resign/handler/" method="post">
            Disable litener:<br />
            &nbsp; &nbsp; &nbsp;Reason: <input type="text" name="resignReason"> &nbsp;&nbsp;&nbsp;
            <input type="hidden" name="userCode" value="${lUser['urlCode']}">
            <button type="submit" class="btn btn-warning" value="Resign">Disable</button>
            <br />
            </form><br />
            <form id="titleListener" class="well form-inline" name="titleListener" action="/workshop/${c.w['urlCode']}/${c.w['url']}/listener/title/handler/" method="post">
            Add a job title to listener (18 characters max):<br />
            <% 
                if 'title' in listener:
                    ltitle = listener['title']
                else:
                    ltitle = ""
            %>
            &nbsp; &nbsp; &nbsp;Title: <input type="text" name="listenerTitle" value="${ltitle}" size="18" maxlength="18"> &nbsp;&nbsp;&nbsp;
            <input type="hidden" name="userCode" value="${lUser['urlCode']}">
            <button type="submit" class="btn btn-warning">Save Title</button>
            <br />
            </form><br />

            % if lEvents:
                % for lE in lEvents:
                    &nbsp; &nbsp; &nbsp; <strong>${lE.date} ${lE['title']}</strong>  ${lE['data']}<br />
                % endfor
            % endif
            </td></tr>
        % endfor
        </tbody>
        </table>
        % if len(c.disabledListeners) > 0:
            <table class="table table-bordered">
            <thead>
            <tr><th>Disabled Listeners</th></tr>
            </thead>
            <tbody>
            % for listener in c.disabledListeners:
                <%
                    lUser = userLib.getUserByCode(listener['userCode'])
                    lEvents = eventLib.getParentEvents(listener)
                %>
                <tr><td><a href="/profile/${lUser['urlCode']}/${lUser['url']}">${lUser['name']}</a> (Disabled)<br />
                % if lEvents:
                    % for lE in lEvents:
                        &nbsp; &nbsp; &nbsp; <strong>${lE.date} ${lE['title']}</strong>  ${lE['data']}<br />
                    % endfor
                % endif
                </tr></td>
            % endfor
            </tbody>
            </table>
        % endif
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
       <% fUser = userLib.getUserByID(f.owner) %>
       <% fEvents = eventLib.getParentEvents(f) %>
       <% fPending = "" %>
       % if pending in f and f['pending'] == '1':
          <% fPending = "(Pending)" %>
       % endif
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

<%def name="admin_items(items, title, listType, active = False)">
    <%
        thisClass = 'tab-pane'
        if active == True:
            thisClass += ' active'
        thisID = '%s-%s' %(listType, title.lower())
    %>
    <div class="${thisClass}" id="${thisID}">
        % if len(items) == 0:
            <p class="centered">There doesn't appear to be anything here.  Hooray!</p>
        % else:
        <table class="table table-bordered table-hover table-condensed">
            <thead>
                <tr>
                    <th>Flags</th>
                    <th>Submitter</th>
                    % if title != 'Comments':
                        <th>Title</th>
                    % else:
                        <th>Comment</th>
                    % endif
                    <th>Action</th> 
                </tr>
            </thead>
            <tbody>
                % for item in items:
                    <%
                        rowClass = None
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
                    % if rowClass is not None:
                        <tr class="${rowClass}">
                    % else:
                        <tr>
                    % endif
                        <td> ${flagLib.getNumFlags(item)} </td>
                        <td>
                            <% 
                                owner = userLib.getUserByID(item.owner)
                                lib_6.userImage(owner, className = 'avatar small-avatar')
                                lib_6.userLink(owner)
                            %>
                        </td>
                        <td>
                            % if title != 'Comments':
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

<%def name="marked_items()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header smaller">Marked Items</h4>
            <p>Items that have been flagged, <span class="badge badge-warning">disabled</span>, or <span class="badge badge-success">enabled</span></p>
            <div class="tabbable">
                <ul class="nav nav-tabs">
                    <li class="active">
                        <a href="#marked-resources" data-toggle="tab">Resources</a>
                    </li>
                    <li>
                        <a href="#marked-ideas" data-toggle="tab">Ideas</a>
                    </li>
                    <li>
                        <a href="#marked-conversations" data-toggle="tab">Conversations</a>
                    </li>
                    <li>
                        <a href="#marked-comments" data-toggle="tab">Comments</a>
                    </li>
                </ul>
                <div class="tab-content">
                    <%
                        admin_items(c.flaggedItems['resources'], 'Resources', 'marked', active = True)
                        admin_items(c.flaggedItems['ideas'], 'Ideas', 'marked')
                        admin_items(c.flaggedItems['discussions'], 'Conversations', 'marked')
                        admin_items(c.flaggedItems['comments'], 'Comments', 'marked')
                    %>
                </div> <!-- /.tab-content -->
            </div> <!-- /.tabbable -->
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

