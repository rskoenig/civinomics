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

<%def name="listProfileMessages()">
    <div ng-init="">
        <div class="media-body object-in-listing {{message.rowClass}} border-bottom" data-code="{{message.messageCode}}">
            
            <div class="span2 message-avatar">
                <img src="{{message.userImage}}" title="{{message.userName}}" alt="{{message.userName}}">
            </div>
            <div class="span8 message-content">
                
                % if {{message.extraInfo}} in ['listenerInvite', 'facilitationInvite']:
                    % if {{message.read}} == u'1':
                        <div class="media">
                            ${lib_6.itemImage(link="{{message.itemImage}}", linkClass="pull-left message-workshop-image")}
                            <div class="media-body">
                                <h5 class="media-heading">
                                    {{message.messageTitle}}
                                </h5>
                                <p>
                                    ${lib_6.userLink2(link="{{message.userLink}}")} 
                                    invites you to facilitate 
                                    ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                                </p>
                                <p>
                                    {{message.messageText}}
                                </p>
                                <p>
                                    (You have already responded by 
                                    {{message.responseAction}}
                                </p>
                                <p class="pull-right"><small>
                                    {{message.messageDate}}
                                     (PST)
                                </small></p>
                            </div>
                        </div>
                    % else:
                        {{message.formStr}}
                            <input type="hidden" name="workshopCode" value="{{message.itemCode}}">
                            <input type="hidden" name="workshopURL" value="{{message.itemUrl}}">
                            <input type="hidden" name="messageCode" value="{{message.messageCode}}">
                            <div class="media">
                                ${lib_6.itemImage(link="{{message.itemImage}}", linkClass="pull-left")}
                                <div class="media-body">
                                    <h5 class="media-heading">
                                        {{message.messageTitle}}
                                    </h5>
                                    <p>
                                        ${lib_6.userLink2(link="{{message.userLink}}")} 
                                        invites you to 
                                        {{message.action}} 
                                        ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                                    </p>
                                    <p>
                                        {{message.messageText}}
                                    </p>
                                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{message.action}} the workshop">Accept</button>
                                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{message.action}} the workshop">Decline</button>
                                    <p class="pull-right"><small>
                                        {{message.messageDate}} 
                                        (PST)
                                    </small></p>
                                </div>
                            </div>
                        </form>
                    % endif

                % elif {{message.extraInfo}} in ['listenerSuggestion']:
                    <div class="media">
                        <div class="media-body">
                            <h5 class="media-heading">
                                {{message.messageTitle}}
                            </h5>
                            Member 
                            ${lib_6.userLink2(link="{{message.userLink}}")} 
                            has a listener suggestion for workshop 
                            ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}:
                            <br />
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['authorInvite']:
                    % if {{message.read}} == u'1':
                        <div class="media">
                            ${lib_6.itemImage(link="{{message.itemImage}}")}
                            <div class="media-body">
                                <h5 class="media-heading">
                                    {{message.messageTitle}}
                                </h5>
                                <p>
                                    ${lib_6.userLink2(link="{{message.userLink}}")} 
                                    invites you to facilitate 
                                    ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                                </p>
                                <p>
                                    {{message.messageText}}
                                </p>
                                <p>
                                    (You have already responded by 
                                    {{message.responseAction}})
                                </p>
                                <p class="pull-right"><small>
                                    {{message.messageDate}} 
                                    (PST)
                                </small></p>
                            </div>
                        </div>
                    % else:
                        {{message.formStr}}
                            <input type="hidden" name="initiativeCode" value="{{message.itemCode}}">
                            <input type="hidden" name="initiativeURL" value="{{message.itemUrl}}">
                            <input type="hidden" name="messageCode" value="{{message.messageCode}}">
                            <div class="media">
                                ${lib_6.itemImage(link="{{message.itemImage}}")}
                                <div class="media-body">
                                    <h5 class="media-heading">
                                        {{message.messageTitle}}
                                    </h5>
                                    <p>
                                        ${lib_6.userLink2(link="{{message.userLink}}")} 
                                        invites you to 
                                        {{message.action}} 
                                        ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                                    </p>
                                    <p>
                                        {{message.messageText}}
                                    </p>
                                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{message.action}} the initiative">Accept</button>
                                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{message.action}} the initiative">Decline</button>
                                    <p class="pull-right"><small>
                                        {{message.messageDate}} 
                                        (PST)
                                    </small></p>
                                </div>
                            </div>
                        </form>
                    % endif

                % elif {{message.extraInfo}} in ['authorResponse']:
                    <div class="media">
                        <div class="media-body">
                            <h5 class="media-heading">
                                {{message.messageTitle}}
                            </h5>
                            <p>
                                ${lib_6.userLink2(link="{{message.userLink}}")} 
                                {{message.messageText}} 
                                ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>

                % elif {{message.extraInfo}} in ['commentResponse']:
                    <div class="media">
                        <div class="media-body">
                            <h5 class="media-heading">
                                ${lib_6.userLink2(link="{{message.userLink}}")} 
                                {{message.messageTitle}}
                            </h5>
                            <p>
                                ${lib_6.itemLinker(link="{{message.itemLink}}", class="green green-hover", title="{{message.commentData}}")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['commentOnPhoto', 'commentOnInitiative']:
                    <div class="media">
                        <div class="media-body">
                            <h5 class="media-heading">
                                ${lib_6.userLink2(link="{{message.userLink}}")} 
                                {{message.messageTitle}}
                            </h5>
                            <p>
                                ${lib_6.itemLinker(link="{{message.itemLink}}", class="green green-hover", title="{{message.commentData}}")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['commentOnResource']:
                    <div class="media">
                        <div class="media-body">
                            <h5 class="media-heading">
                                ${lib_6.userLink2(link="{{message.userLink}}")} 
                                {{message.messageTitle}}
                            </h5>
                            <p>
                                ${lib_6.itemLinker(link="{{message.itemLink}}", class="green green-hover")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['commentOnUpdate']:
                    <div class="media">
                        <div class="media-body">
                            <h5 class="media-heading">
                                ${lib_6.userLink2(link="{{message.userLink}}")} 
                                {{message.messageTitle}}
                            </h5>
                            <p>
                                ${lib_6.itemLinker(link="{{message.itemLink}}", class="green green-hover")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['disabledPhoto', 'enabledPhoto', 'deletedPhoto']:
                    <div class="media">
                        <div class="media-body">
                            <h4 class="media-heading centered">
                                {{message.messageTitle}}
                            </h4>
                            <p>
                                It was 
                                {{message.action}} 
                                because: 
                                {{message.reason}}
                            </p>
                            <p>
                                Your photo:
                                ${lib_6.itemLinker(link="{{message.itemLink}}", class="green green-hover", photo=True)}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['disabledInitiative', 'enabledInitiative', 'deletedInitiative']:
                    <div class="media">
                        <div class="media-body">
                            <h4 class="media-heading centered">
                                {{message.messageTitle}}
                            </h4>
                            <p>
                                It was 
                                {{message.action}} 
                                because: 
                                {{message.reason}}
                            </p>
                            <p>
                                Your initiative:
                                ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['disabledInitiativeResource', 'enabledInitiativeResource', 'deletedInitiativeResource']:
                    <div class="media">
                        <div class="media-body">
                            <h4 class="media-heading centered">
                                {{message.messageTitle}}
                            </h4>
                            <p>
                                It was 
                                {{message.action}} 
                                because: 
                                {{message.reason}}
                            </p>
                            <p>
                                Your initiative resource:
                                ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['disabledInitiativeUpdate', 'enabledInitiativeUpdate', 'deletedInitiativeUpdate']:
                    <div class="media">
                        <div class="media-body">
                            <h4 class="media-heading centered">
                                {{message.messageTitle}}
                            </h4>
                            <p>
                                It was 
                                {{message.action}} 
                                because: 
                                {{message.reason}}
                            </p>
                            <p>
                                Your initiative update:
                                ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % elif {{message.extraInfo}} in ['disabled', 'enabled', 'deleted', 'adopted']:
                    <div class="media">
                        <div class="media-body">
                            <h4 class="media-heading centered">
                                {{message.messageTitle}}
                            </h4>
                            <p>
                                It was 
                                {{message.action}} 
                                because: 
                                {{message.reason}}
                            </p>
                            <p>
                                You posted:
                                ${lib_6.itemLinker(link="{{message.itemLink}}", title="{{message.itemTitle}}")}
                            </p>
                            <p>
                                {{message.messageText}}
                            </p>
                            <p class="pull-right"><small>
                                {{message.messageDate}} 
                                (PST)
                            </small></p>
                        </div>
                    </div>
                % endif
                
            </span>
            
        </div>
    </div> <!-- /ng-init -->
</%def>
