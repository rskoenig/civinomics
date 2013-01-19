<%!
    from pylowiki.lib.db.event import getParentEvents
    from pylowiki.lib.db.user import getUserByID
    import pylowiki.lib.db.discussion       as discussionLib
    import pylowiki.lib.db.idea             as ideaLib
    import pylowiki.lib.db.comment          as commentLib
    import pylowiki.lib.db.flag             as flagLib
%>  
<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="admin_show()">
	<div class="row-fluid">
        <div class="section-wrapper">
            <div class="browse">
                <h4 class="section-header" style="text-align: center"><br />Facilitator Tools</h4>
                <br />
	            <form name="admin_issue" id="admin_issue" class="form-inline" action="/workshop/${c.w['urlCode']}/${c.w['url']}/adminWorkshopHandler" enctype="multipart/form-data" method="post" >
                <strong>Message to Participants:</strong>
                <br />
                This is displayed on the workshop landing page. Use this to welcome members to the workshop or to make announcements.<br />
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
            </div><!-- browse -->
        </div><!-- browse -->
    </div><!-- row-fluid -->
</%def>

<%def name="admin_event_log()">
    <div class="row-fluid">
        <div class="section-wrapper">
            <div class="browse">
                <h4 class="section-header" style="text-align: center"><br />Event Log</h4>
                A record of configuration and administrative changes to the workshop.<br />
                <% wEvents = getParentEvents(c.w) %>
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
        <table class="table table-bordered">
        <thead>
        <tr><th>Current Facilitators</th></tr>
        </thead>
        <tbody>
        % for f in c.f:
            <% fUser = getUserByID(f.owner) %>
            <% fEvents = getParentEvents(f) %>
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
        <p>To invite an active member to co-facilitate this workshop, visit their profile page and look for the "Invite to co-facilitate" button!</p>
        % if len(c.df) > 0:
            <table class="table table-bordered">
            <thead>
            <tr><th>Disabled Facilitators</th></tr>
            </thead>
            <tbody>
            % for f in c.df:
                <% fUser = getUserByID(f.owner) %>
                <% fEvents = getParentEvents(f) %>
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


<%def name="admin_info()">
    <% wEvents = getParentEvents(c.w) %>
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
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
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
       <% fUser = getUserByID(f.owner) %>
       <% fEvents = getParentEvents(f) %>
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

<%def name="admin_items(items, title)">
    <table class="table table-bordered">
        <thead>
            <tr><th>${title}</th></tr>
        </thead>
        <tbody>
            % for item in items:
                % if item['deleted'] == '0': 
                    <tr>
                        <td>
                            (${flagLib.getNumFlags(item)})
                            <a ${lib_6.thingLinkRouter(item, c.w)} class="expandable">${item['title']}</a>
                        </td>
                    </tr>
                % endif
            % endfor
        </tbody>
    </table>
</%def>

<%def name="admin_flagged()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Flagged Items</h4>
            These are items in the workshop which have been flagged by members. Each flagged item needs to be examined by the facilitator and some action taken, even if it is only clearing the flags.<br />
            <br /><br />
            ${admin_items(c.flaggedItems['resources'], 'Flagged Resources and Comments')}
            <br /><br />
            ${admin_items(c.flaggedItems['ideas'], 'Flagged Ideas and Comments')}
            <br /><br />
            ${admin_items(c.flaggedItems['discussions'], 'Flagged Discussions and Comments')}
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="admin_disabled()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Disabled Items</h4>
            These are items in the workshop which have been disabled by a facilitator or admin. These items are 
            filtered to the bottom of lists or not displayed by default. Items are often disabled for being off-topic, 
            duplicates of existing items, or have been flagged as offensive or otherwise violating the terms of service. 
            <br /><br />
            ${admin_items(c.disabledItems['resources'], 'Disabled Resources and Comments')}
            <br /><br />
            ${admin_items(c.disabledItems['ideas'], 'Disabled Ideas and Comments')}
            <br /><br />
            ${admin_items(c.disabledItems['discussions'], 'Disabled Discussions and Comments')}
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>

<%def name="admin_deleted()">
    <div class="section-wrapper">
        <div class="browse">
            <h4 class="section-header" style="text-align: center"><br />Deleted Items</h4>
            These are items in the workshop which have been deleted by a facilitator or admin. These items are filtered to the bottom of lists 
            and their content not displayed to anyone, including members and admins. Items are deleted when they are in violation of the law such 
            as linking to pirated content or child porn or if they are serious breech of the terms of service such as displaying or linking to porn.
            <br /><br />
            ${admin_items(c.deletedItems['resources'], 'Deleted Resources and Comments')}
            <br /><br />
            ${admin_items(c.deletedItems['ideas'], 'Deletede Ideas and Comments')}
            <br /><br />
            ${admin_items(c.deletedItems['discussions'], 'Deleted Discussions and Comments')}
        </div><!-- browse -->
    </div><!-- section-wrapper -->
</%def>
