<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%!
   import misaka as misaka
   import pylowiki.lib.db.facilitator   as facilitatorLib
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.event         as eventLib
%>

<%def name="showDisabledMessage(thing)">
    <%
        events = eventLib.getEventsWithAction(thing, 'disabled')
        objTypeMapping = {  'discussion':'conversation',
                            'idea':'idea',
                            'resource':'resource'}
    %>
    <div class="row-fluid">
        <div class="span11 offset1">
            % for event in events:
                <% 
                    eventOwner = userLib.getUserByID(event.owner)
                %>
                <small>This ${objTypeMapping[thing.objType]} has been disabled by ${lib_6.userLink(eventOwner)} because: ${event['reason']}</small>
            % endfor
        </div>
    </div>
</%def>

<%def name="extraText(thing)">
    % if 'text' in thing.keys():
        <div class="row-fluid">
            <div class="span11 offset1">
                ${misaka.html(thing['text']) | n}
            </div>
        </div><!--/.row-fluid-->
    % endif
</%def>

<%def name="showItemTitle(thing)">
    <div class="span1">
        ${lib_6.upDownVote(thing)}
    </div>
    <div class="span11">
        <h4>
            <% 
                link = ''
                title = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title'])
                if thing.objType == 'resource':
                    link = '<small>(<a %s target=_blank>%s</a>)</small>' %(lib_6.thingLinkRouter(thing, c.w, embed=True, directLink=True), lib_6.ellipsisIZE(thing['link'], 75))
                elif thing.objType == 'revision':
                    if thing['objType'] == 'resource':
                        title = '<a href="%s" class="listed-item-title" target="_blank">%s</a>' %(thing['link'], thing['title'])
                    else:
                        title = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title']) 
                else:
                    title = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title']) 
            %>
            ${title | n}<br>
            ${link | n}
        </h4>
    </div>
</%def>

<%def name="showItemOwner(thing)">
    <div class="span11 offset1">
        <%
            lib_6.userImage(thing.owner, className="avatar")
            role = ''
            if 'addedAs' in thing.keys():
                roles = ['admin', 'facilitator', 'listener']
                if thing['addedAs'] in roles:
                    role = '(%s) ' % thing['addedAs']
        %>
        Posted by ${lib_6.userLink(thing.owner)} ${role}from ${lib_6.userGeoLink(thing.owner)}
    </div>
</%def>

<%def name="moderationPanel(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
    %>
    <div class="row-fluid">
        <div class="span11 offset1">
            <div class="btn-group">
                % if thing['disabled'] == '0':
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
                % endif
                % if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser, c.w):
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>>
                % endif
                % if userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser, c.w):
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
                % endif
            </div>
        </div>
    </div>
    
    <%
        if thing['disabled'] == '0':
            lib_6.flagThing(thing)
            if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser, c.w):
                lib_6.editThing(thing)
            if userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser, c.w):
                lib_6.adminThing(thing)
        else:
            if userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser, c.w):
                lib_6.editThing(thing)
            if userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser, c.w):
                lib_6.adminThing(thing)
    %>
</%def>
