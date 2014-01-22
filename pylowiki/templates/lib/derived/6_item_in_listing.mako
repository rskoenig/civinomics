<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%!
   import misaka as misaka
   import pylowiki.lib.db.facilitator   as facilitatorLib
   import pylowiki.lib.db.user          as userLib
   import pylowiki.lib.db.event         as eventLib
   
   import logging
   log = logging.getLogger(__name__)
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

<%def name="showAdoptedMessage(thing)">
    <% event = eventLib.getEventForThingWithAction(thing, 'adopted') %>
    <div class="row-fluid">
        <div class="span11 offset1">
            <% 
                    eventOwner = userLib.getUserByID(event.owner)
            %>
            <small><i class="icon-star"></i> This idea has been adopted by ${lib_6.userLink(eventOwner)} because: ${event['reason']}</small>
        </div>
    </div>
</%def>

<%def name="extraText(thing)">
    % if 'text' in thing.keys():
        ${misaka.html(thing['text']) | n}
    % endif
</%def>

<%def name="showItemTitle(thing)">
    <h4>
        <% 
            link = ""
            title = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title'])
            if thing.objType == 'resource':
                    link = '<small>(<a href=%s target=_blank>%s</a>)</small>' %(thing['link'], lib_6.ellipsisIZE(thing['link'], 75))
                    if thing['type'] == 'rich' or thing['type'] == 'video':
                        link = link + '<div class="spacer"></div>' + thing['info']
                    if thing['type'] == 'photo':
                        link = link + '<div class="spacer"></div><img src="' + thing['info'] + '">'
            elif thing.objType == 'revision':
                title = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title'])
                if thing['objType'] == 'resource':
                    link = '<small>(<a href=%s target=_blank>%s</a>)</small>' %(thing['link'], lib_6.ellipsisIZE(thing['link'], 75))
                    if 'info' in thing:
                        link = link + '<div class="spacer"></div>' + thing['info']
            else:
                title = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title']) 
        %>
        ${title | n}<br>
        <div class="spacer"></div>
        ${link | n}
    </h4>
</%def>

<%def name="showItemOwner(thing)">
    <%
        role = ''
        if 'addedAs' in thing.keys():
            roles = ['admin', 'facilitator', 'listener']
            if thing['addedAs'] in roles:
                role = ' (%s)' % thing['addedAs']
    %>
    ${lib_6.userLink(thing.owner)}${role}<span class="grey">${lib_6.userGreetingMsg(thing.owner)}</span> from ${lib_6.userGeoLink(thing.owner)}${lib_6.userImage(thing.owner, className="avatar med-avatar")}
    <br />Originally posted  ${thing.date}
    % if 'views' in thing:
        <i class="icon-eye-open"></i> ${str(thing['views'])} views
    % endif
</%def>

<%def name="moderationPanel(thing)">
    <%
        if 'user' not in session or thing.objType == 'revision':
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
        log.info("thing keys is %s"%thing.keys())
    %>
    <div class="btn-group" style="margin-top: -10px;">
        % if thing['disabled'] == '0':
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
        % endif
        % if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id) or (c.w and facilitatorLib.isFacilitator(c.authuser, c.w)):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>>
        % endif
        % if userLib.isAdmin(c.authuser.id) or (c.w and facilitatorLib.isFacilitator(c.authuser, c.w)):
            <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
        % endif

    </div>
    <%
        if thing['disabled'] == '0':
            lib_6.flagThing(thing)
            if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id) or (c.w and facilitatorLib.isFacilitator(c.authuser, c.w)):
                lib_6.editThing(thing)
            if userLib.isAdmin(c.authuser.id) or (c.w and facilitatorLib.isFacilitator(c.authuser, c.w)):
                lib_6.adminThing(thing)
        else:
            if userLib.isAdmin(c.authuser.id) or (c.w and facilitatorLib.isFacilitator(c.authuser, c.w)):
                lib_6.editThing(thing)
            if userLib.isAdmin(c.authuser.id) or (c.w and facilitatorLib.isFacilitator(c.authuser, c.w)):
                lib_6.adminThing(thing)
    %>
</%def>
