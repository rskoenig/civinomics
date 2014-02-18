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
<%namespace name="ng_helpers" file="/lib/ng_lib.mako" />

<%def name="listProfileMessages()">

    <div class="browse" ng-controller="profileMessagesCtrl">

        <div class="row-fluid" ng-repeat="message in messages | orderBy:orderProp | filter:filterProp " ng-cloak>

            <div class="media-body object-in-listing {{message.rowClass}} border-bottom" data-code="{{message.messageCode}}">
                
                <div class="span2 message-avatar">
                    <img src="{{message.userImage}}" title="{{message.userName}}" alt="{{message.userName}}">
                </div>
                <div class="span8 message-content">
                    <!-- this init clause covers all varaiables that can possibly be used in the following cases -->
                    <div ng-init="rowClass=message.rowClass; read=message.read; userName=message.userName; userLink=message.userLink; userImage=message.userImage; messageTitle=message.messageTitle; messageText=message.messageText; messageCode=message.messageCode; messageDate=message.messageDate; responseAction=message.responseAction; formStr=message.formStr; action=message.action; itemCode=message.itemCode; itemImage=message.itemImage; itemLink=message.itemLink; itemTitle=message.itemTitle; itemUrl=message.itemUrl; commentData=message.commentData; extraInfo=message.extraInfo; eventAction=message.eventAction; eventReason=message.eventReason;">
                        % if {{message.extraInfo}} in ['listenerInvite', 'facilitationInvite']:
                            ${ng_helpers.listenerFacilitationInvite()}
                        % elif {{message.extraInfo}} in ['listenerSuggestion']:
                            ${ng_helpers.listenerSuggestion()}
                        % elif {{message.extraInfo}} in ['authorInvite']:
                            ${ng_helpers.authorInvite()}
                        % elif {{message.extraInfo}} in ['authorResponse']:
                            ${ng_helpers.authorResponse()}
                        % elif {{message.extraInfo}} in ['commentResponse']:
                            
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
                    </div>
                </span>
                
            </div>
            
        </div>

    </div>

</%def>
