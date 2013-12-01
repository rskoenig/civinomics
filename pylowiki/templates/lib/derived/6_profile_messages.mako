<%!
    import pylowiki.lib.db.user             as userLib
    import pylowiki.lib.db.listener         as listenerLib
    import pylowiki.lib.db.facilitator      as facilitatorLib
    import pylowiki.lib.db.workshop         as workshopLib
    import pylowiki.lib.db.initiative       as initiativeLib
    import pylowiki.lib.db.comment          as commentLib
    import pylowiki.lib.db.event            as eventLib
    import pylowiki.lib.db.generic          as generic

    import logging, os
    log = logging.getLogger(__name__)

%> 

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="profileMessages()">
    <table class="table table-condensed table-hover">
        % for message in c.messages:
            % if 'commentCode' in message and not commentLib.getCommentByCode(message['commentCode']):
                <% continue %>
            % endif
            <%
                rowClass = ''
                if message['read'] == u'0':
                    rowClass = 'warning unread-message'
            %>
            <tr class = "${rowClass}" data-code="${message['urlCode']}">
                <%
                    if message['sender'] == u'0':
                        sender = 'Civinomics'
                    else:
                        sender = userLib.getUserByCode(message['sender'])
                %>
                <td class="message-avatar">
                    % if sender == 'Civinomics':
                        <img src="/images/handdove_medium.png" title="Civinomics" alt="Civinomics">
                        <p>Civinomics</p>
                    % else:
                        ${lib_6.userImage(sender, className="avatar")}
                    % endif
                </td>
                <td class="message-content"> 
                    % if 'extraInfo' in message.keys():
                        % if message['extraInfo'] in ['listenerInvite', 'facilitationInvite']:
                            <% 
                                workshop = workshopLib.getWorkshopByCode(message['workshopCode'])
                                if message['extraInfo'] == 'listenerInvite':
                                    formStr = """<form method="post" name="inviteListener" id="inviteListener" action="/profile/%s/%s/listener/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                    action = 'be a listener for'
                                    role = listenerLib.getListenerByCode(message['listenerCode'])
                                else:
                                    formStr = """<form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/%s/%s/facilitate/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                    action = 'facilitate'
                                    role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                            %>
                            % if message['read'] == u'1':
                                <%
                                    # Since this is tied to the individual message, we will only have one action
                                    # The query here should be rewritten to make use of map/reduce for a single query
                                    event = eventLib.getEventsWithAction(message, 'accepted')
                                    if not event:
                                        responseAction = 'declining'
                                    else:
                                        responseAction = 'accepting'
                                %>
                                <div class="media">
                                    ${lib_6.workshopImage(workshop, linkClass="pull-left message-workshop-image")}
                                    <div class="media-body">
                                        <h5 class="media-heading">${message['title']}</h5>
                                        <p>${lib_6.userLink(sender)} invites you to facilitate <a ${lib_6.workshopLink(workshop)}>${workshop['title']}</a></p>
                                        <p>${message['text']}</p>
                                        <p>(You have already responded by ${responseAction})</p>
                                        <p class="pull-right"><small>${message.date} (PST)</small></p>
                                    </div>
                                </div>
                            % else:
                                ${formStr | n}
                                    <input type="hidden" name="workshopCode" value="${workshop['urlCode']}">
                                    <input type="hidden" name="workshopURL" value="${workshop['url']}">
                                    <input type="hidden" name="messageCode" value="${message['urlCode']}">
                                    <div class="media">
                                        ${lib_6.workshopImage(workshop, linkClass="pull-left")}
                                        <div class="media-body">
                                            <h5 class="media-heading">${message['title']}</h5>
                                            <p>${lib_6.userLink(sender)} invites you to ${action} <a ${lib_6.workshopLink(workshop)}>${workshop['title']}</a></p>
                                            <p>${message['text']}</p>
                                            <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to ${action} the workshop">Accept</button>
                                            <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to ${action} the workshop">Decline</button>
                                            <p class="pull-right"><small>${message.date} (PST)</small></p>
                                        </div>
                                    </div>
                                </form>
                            % endif
                        % elif message['extraInfo'] in ['listenerSuggestion']:
                            <% workshop = workshopLib.getWorkshopByCode(message['workshopCode']) %>
                            <div class="media">
                                <div class="media-body">
                                    <h5 class="media-heading">${message['title']}</h5>
                                    Member ${lib_6.userLink(sender)} has a listener suggestion for workshop <a ${lib_6.workshopLink(workshop)}>${workshop['title']}</a>:<br />
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['authorInvite']:
                            <% 
                                initiative = initiativeLib.getInitiative(message['initiativeCode'])
                                formStr = """<form method="post" name="inviteFacilitate" id="inviteFacilitate" action="/profile/%s/%s/facilitate/response/handler/">""" %(c.user['urlCode'], c.user['url'])
                                action = 'coauthor'
                                role = facilitatorLib.getFacilitatorByCode(message['facilitatorCode'])
                            %>
                            % if message['read'] == u'1':
                                <%
                                    # Since this is tied to the individual message, we will only have one action
                                    # The query here should be rewritten to make use of map/reduce for a single query
                                    event = eventLib.getEventsWithAction(message, 'accepted')
                                    if not event:
                                        responseAction = 'declining'
                                    else:
                                        responseAction = 'accepting'
                                %>
                                <div class="media">
                                    ${lib_6.initiativeImage(initiative)}
                                    <div class="media-body">
                                        <h5 class="media-heading">${message['title']}</h5>
                                        <p>${lib_6.userLink(sender)} invites you to facilitate <a ${lib_6.initiativeLink(initiative)}>${initiative['title']}</a></p>
                                        <p>${message['text']}</p>
                                        <p>(You have already responded by ${responseAction})</p>
                                        <p class="pull-right"><small>${message.date} (PST)</small></p>
                                    </div>
                                </div>
                            % else:
                                ${formStr | n}
                                    <input type="hidden" name="initiativeCode" value="${initiative['urlCode']}">
                                    <input type="hidden" name="initiativeURL" value="${initiative['url']}">
                                    <input type="hidden" name="messageCode" value="${message['urlCode']}">
                                    <div class="media">
                                        ${lib_6.initiativeImage(initiative)}
                                        <div class="media-body">
                                            <h5 class="media-heading">${message['title']}</h5>
                                            <p>${lib_6.userLink(sender)} invites you to ${action} <a ${lib_6.initiativeLink(initiative)}>${initiative['title']}</a></p>
                                            <p>${message['text']}</p>
                                            <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to ${action} the initiative">Accept</button>
                                            <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to ${action} the initiative">Decline</button>
                                            <p class="pull-right"><small>${message.date} (PST)</small></p>
                                        </div>
                                    </div>
                                </form>
                            % endif

                        % elif message['extraInfo'] in ['commentResponse']:
                            <%
                                comment = commentLib.getCommentByCode(message['commentCode'])
                                workshop = workshopLib.getWorkshopByCode(comment['workshopCode'])
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h5 class="media-heading">${lib_6.userLink(sender)} ${message['title']}</h5>
                                    <p><a ${lib_6.thingLinkRouter(comment, workshop, embed=True, commentCode=comment['urlCode']) | n} class="green green-hover">${comment['data']}</a></p>
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['commentOnPhoto', 'commentOnInitiative']:
                            <%
                                comment = commentLib.getCommentByCode(message['commentCode'])
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h5 class="media-heading">${lib_6.userLink(sender)} ${message['title']}</h5>
                                    <p><a ${lib_6.thingLinkRouter(comment, c.user, embed=True, commentCode=comment['urlCode']) | n} class="green green-hover">${comment['data']}</a></p>
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['commentOnResource']:
                            <%
                                comment = commentLib.getCommentByCode(message['commentCode'])
                                resource = generic.getThing(comment['resourceCode'])
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h5 class="media-heading">${lib_6.userLink(sender)} ${message['title']}</h5>
                                    <p><a ${lib_6.thingLinkRouter(comment, resource, embed=True, commentCode=comment['urlCode']) | n} class="green green-hover">${comment['data']}</a></p>
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['disabledPhoto', 'enabledPhoto', 'deletedPhoto']:
                            <%
                                photoCode = message['photoCode']
                                thing = generic.getThing(photoCode)
                                title = thing['title']
                                if message['extraInfo'] in ['disabledPhoto']:
                                    event = eventLib.getEventsWithAction(message, 'disabled')
                                elif message['extraInfo'] in ['enabledPhoto']:
                                    event = eventLib.getEventsWithAction(message, 'enabled')
                                elif message['extraInfo'] in ['deletedPhoto']:
                                    event = eventLib.getEventsWithAction(message, 'deleted')
                                
                                action = event[0]['action']
                                reason = event[0]['reason']
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h4 class="media-heading centered">${message['title']}</h4>
                                    <p>It was ${action} because: ${reason}</p>
                                    <p>Your photo:
                                        <a href="/profile/${c.user['urlCode']}/${c.user['url']}/photo/show/${photoCode}" class="green green-hover">${title}</a>
                                    </p>
                                    % if 'text' in message:
                                        <p>${message['text']}</p>
                                    % endif
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['disabledInitiative', 'enabledInitiative', 'deletedInitiative']:
                            <%
                                initiativeCode = message['initiativeCode']
                                thing = generic.getThing(initiativeCode)
                                title = thing['title']
                                if message['extraInfo'] in ['disabledInitiative']:
                                    event = eventLib.getEventsWithAction(message, 'disabled')
                                elif message['extraInfo'] in ['enabledInitiative']:
                                    event = eventLib.getEventsWithAction(message, 'enabled')
                                elif message['extraInfo'] in ['deletedInitiative']:
                                    event = eventLib.getEventsWithAction(message, 'deleted')
                                
                                action = event[0]['action']
                                reason = event[0]['reason']
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h4 class="media-heading centered">${message['title']}</h4>
                                    <p>It was ${action} because: ${reason}</p>
                                    <p>Your initiative:
                                        <a href="/initiative/${thing['urlCode']}/${thing['url']}/show" class="green green-hover">${title}</a>
                                    </p>
                                    % if 'text' in message:
                                        <p>${message['text']}</p>
                                    % endif
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['disabledInitiativeResource', 'enabledInitiativeResource', 'deletedInitiativeResource']:
                            <%
                                resourceCode = message['resourceCode']
                                thing = generic.getThing(resourceCode)
                                title = thing['title']
                                if message['extraInfo'] in ['disabledInitiativeResource']:
                                    event = eventLib.getEventsWithAction(message, 'disabled')
                                elif message['extraInfo'] in ['enabledInitiativeResource']:
                                    event = eventLib.getEventsWithAction(message, 'enabled')
                                elif message['extraInfo'] in ['deletedInitiativeResource']:
                                    event = eventLib.getEventsWithAction(message, 'deleted')
                                
                                action = event[0]['action']
                                reason = event[0]['reason']
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h4 class="media-heading centered">${message['title']}</h4>
                                    <p>It was ${action} because: ${reason}</p>
                                    <p>Your initiative resource:
                                        <a href="/initiative/${thing['initiativeCode']}/${thing['initiative_url']}/resource/${thing['urlCode']}/${thing['url']}" class="green green-hover">${title}</a>
                                    </p>
                                    % if 'text' in message:
                                        <p>${message['text']}</p>
                                    % endif
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % elif message['extraInfo'] in ['disabled', 'enabled', 'deleted', 'adopted']:
                            <%
                                event = eventLib.getEventsWithAction(message, message['extraInfo'])
                                if not event:
                                    continue
                                event = event[0]
                                
                                # Mako was bugging out on me when I tried to do this with sets
                                codeTypes = ['commentCode', 'discussionCode', 'ideaCode', 'resourceCode', 'initiativeCode']
                                thing = None
                                for codeType in codeTypes:
                                    if codeType in message.keys():
                                        thing = generic.getThing(message[codeType])
                                        break
                                if thing is None:
                                    continue
                                if 'workshopCode' in thing:
                                    parent = generic.getThing(thing['workshopCode'])
                                elif 'initiativeCode' in thing:
                                    parent = generic.getThing(thing['initiativeCode'])
                                elif 'resourceCode' in thing:
                                    parent = generic.getThing(thing['resourceCode'])
                            %>
                            <div class="media">
                                <div class="media-body">
                                    <h4 class="media-heading centered">${message['title']}</h4>
                                    <p>It was ${event['action']} because: ${event['reason']}</p>
                                    <p>You posted:
                                    % if thing.objType == 'comment':
                                        <a ${lib_6.thingLinkRouter(thing, parent, embed=True, commentCode=thing['urlCode']) | n} class="green green-hover">${thing['data']}</a>
                                    % else:
                                        <a ${lib_6.thingLinkRouter(thing, parent, embed=True) | n} class="green green-hover">${thing['title']}</a>
                                    % endif
                                    </p>
                                    <p>${message['text']}</p>
                                    <p class="pull-right"><small>${message.date} (PST)</small></p>
                                </div>
                            </div>
                        % endif
                    % endif
                </td>
            </tr>
        % endfor
    </table>
</%def>
