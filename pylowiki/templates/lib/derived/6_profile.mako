<%!
    from pylowiki.lib.db.workshop import getWorkshopByID, getWorkshopByCode
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="thingCount(user, things, title)">
    <% thingListingURL = "/profile/%s/%s/%s" %(user['urlCode'], user['url'], title) %>
    <h3 class="profile-count centered">
        <a class="black" href="${thingListingURL}">${len(things)}</a>
    </h3>
    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">${title}</a></p></div>
</%def>

<%def name="showWorkshop(workshop, **kwargs)">
    <div class="media profile-workshop">
        <a class="pull-left" ${lib_6.workshopLink(workshop)}>
            <img class="media-object" src="${lib_6.workshopImage(workshop, raw=True) | n}">
        </a>
        <%
            if 'imageOnly' in kwargs:
                if kwargs['imageOnly'] == True:
                    return
        %>
        <div class="media-body">
            <a ${lib_6.workshopLink(workshop)}><h5 class="media-heading">${workshop['title']}</h5></a>
            Short, one sentence description here
        </div>
    </div>
</%def>

<%def name="listCreatedThings(user, things, title)">
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="centered section-header"> ${title} </h3>
            <table class="table table-condensed table-hover user-thing-listing">
                <tbody>
                <% counter = 0 %>
                    % for thing in things:
                        % if counter == 0:
                            <tr> <td class="no-border">
                        % else:
                            <tr> <td>
                        % endif
                            <%
                                if thing.objType != 'discussion':
                                    workshop = getWorkshopByID(thing['workshop_id'])
                                else:
                                    workshop = getWorkshopByCode(thing['workshopCode'])
                                thingLink = lib_6.thingLinkRouter(thing, workshop, raw=True, embed=True)
                                workshopLink = lib_6.workshopLink(workshop, embed=True)
                                descriptionText = 'No description'
                                if 'comment' in thing.keys():
                                    if thing['comment'] != '':
                                        descriptionText = thing['comment']
                                elif 'text' in thing.keys():
                                    if thing['text'] != '':
                                        descriptionText = thing['text']
                            %>
                            ${showWorkshop(workshop, imageOnly = True)}
                            <a ${thingLink | n}> ${lib_6.ellipsisIZE(thing['title'], 60)} </a> in workshop <a ${workshopLink | n}> ${workshop['title']} </a> on <span class="green">${thing.date.strftime('%b %d, %Y')}</span>
                            <br />
                            Description: ${lib_6.ellipsisIZE(descriptionText, 150)}
                        </td> </tr>
                        <% counter += 1 %>
                    % endfor
                </tbody>
            </table>
        </div>
    </div>
</%def>

<%def name="listInterestedThings(user, things, title)">
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="centered section-header"> ${title} </h3>
            % if len(things) == 0:
                There doesn't seem to be anything here!
                <% return %>
            % endif
            <% 
                objType = things[0].objType
                counter = 0
            %>
            <ul class="thumbnails">
                % for thing in things:
                    <li class="follow">
                        ${lib_6.userImage(thing, className="avatar hoverTip", rel="tooltip", placement="bottom")}
                    </li>
                % endfor
            </ul>
        </div>
    </div>
</%def>

<%def name="followButton(user)">
   <a class="btn round pull-right followButton" href="#">
      <img class="watch" src="/images/glyphicons_pro/glyphicons/png/glyphicons_051_eye_open.png">
      <span> Follow </span>
   </a>
</%def>

<%def name="profileDashboard()">
    <div class="centered">
        ${lib_6.userImage(c.user, className="avatar avatar-large")}
    </div>
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="section-header">${c.user['name']}</h3>
            <p>${lib_6.userGeoLink(c.user)}</p>
            <p>Joined ${c.user.date.strftime('%b %d, %Y')}</p>
            <hr>
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.resources, 'resources')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.ideas, 'ideas')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.discussions, 'discussions')}
                </div>
            </div> <!--/.row-fluid-->
            <hr>
            <div class="row-fluid">
                <div class="span4">
                    ${thingCount(c.user, c.ideas, 'followers')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.ideas, 'following')}
                </div>
                <div class="span4">
                    ${thingCount(c.user, c.ideas, 'watching')}
                </div>
            </div> <!--/.row-fluid-->
            <hr>
            Placeholder for listing organizations
        </div><!--/.browse-->
    </div><!--/.section-wrapper-->
</%def>