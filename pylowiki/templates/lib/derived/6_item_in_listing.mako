<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%!
   import misaka as misaka
   import pylowiki.lib.db.facilitator   as facilitatorLib
   import pylowiki.lib.db.user          as userLib
%>

<%def name="extraText(thing)">
    % if thing.objType == 'discussion':
        <div class="row-fluid">
            <div class="span11 offset1">
                ${misaka.html(thing['text']) | n}
            </div>
        </div><!--/.row-fluid-->
    % endif
    % if thing.objType == 'resource':
        <div class="row-fluid">
            <div class="span11 offset1">
                ${misaka.html(thing['comment']) | n}
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
                if thing.objType == 'resource':
                    link = '<a href="%s" class="listed-item-title">%s</a>' %(thing['link'], thing['title'])
                else:
                    link = '<a %s class="listed-item-title">%s</a>' %(lib_6.thingLinkRouter(thing, c.w, embed=True), thing['title']) 
            %>
            ${link | n}
        </h4>
    </div>
</%def>

<%def name="showItemOwner(thing)">
    <div class="span11 offset1">
        ${lib_6.userImage(thing.owner, className="avatar")}
        Posted by ${lib_6.userLink(thing.owner)} from ${lib_6.userGeoLink(thing.owner)}
    </div>
</%def>

<%def name="moderationPanel(thing)">
    <%
        if 'user' not in session:
            return
        flagID = 'flag-%s' % thing['urlCode']
        editID = 'edit-%s' % thing['urlCode']
        adminID = 'admin-%s' % thing['urlCode']
    %>
    <div class="row-fluid">
        <div class="span11 offset1">
            <div class="btn-group">
                <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${flagID}">flag</a>
                % if c.authuser.id == thing.owner or userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser.id):
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${editID}">edit</a>>
                % endif
                % if userLib.isAdmin(c.authuser.id) or facilitatorLib.isFacilitator(c.authuser.id):
                    <a class="btn btn-mini accordion-toggle" data-toggle="collapse" data-target="#${adminID}">admin</a>
                % endif
            </div>
        </div>
    </div>
</%def>