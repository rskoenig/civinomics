<%!
    from pylowiki.lib.db.workshop import getWorkshopByID
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="thingCount(user, things, title)">
    <% thingListingURL = "/profile/%s/%s/%s" %(user['urlCode'], user['url'], title) %>
    <h3 class="profile-count centered">
        <a class="black" href="${thingListingURL}">${len(things)}</a>
    </h3>
    <div class="centered"><p><a class="green green-hover" href="${thingListingURL}">${title}</a></p></div>
</%def>

<%def name="showWorkshop(workshop)">
    <div class="media profile-workshop">
        <a class="pull-left" ${lib_6.workshopLink(workshop)}>
            <img class="media-object" src="${lib_6.workshopImage(workshop, raw=True) | n}">
        </a>
        <div class="media-body">
            <a ${lib_6.workshopLink(workshop)}><h5 class="media-heading">${workshop['title']}</h5></a>
            Short, one sentence description here
        </div>
    </div>
</%def>

<%def name="listThings(user, things, title)">
    <div class="section-wrapper">
        <div class="browse">
            <h3 class="centered section-header"> ${title} </h3>
            <table class="table table-condensed table-hover user-thing-listing">
                <tbody>
                    % for thing in things:
                        <tr> <td>
                            <%
                                workshop = getWorkshopByID(thing['workshop_id'])
                                thingLink = lib_6.thingLinkRouter(thing, workshop, raw=True, embed=True)
                                workshopLink = lib_6.workshopLink(workshop, embed=True)
                            %>
                            <a ${thingLink | n}> ${thing['title']} </a> in workshop <a ${workshopLink | n}> ${workshop['title']} </a> on <span class="green">${thing.date.strftime('%b %d, %Y')}</span>
                            % if thing['comment'] != '':
                                <br />
                                Description: ${lib_6.ellipsisIZE(thing['comment'], 150)}
                            % endif
                        </td> </tr>
                    % endfor
                </tbody>
            </table>
        </div>
    </div>
</%def>