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
                    <div ng-init="rowClass=message.rowClass; read=message.read; userName=message.userName; userLink=message.userLink; userImage=message.userImage; messageTitle=message.messageTitle; messageText=message.messageText; messageCode=message.messageCode; messageDate=message.messageDate; responseAction=message.responseAction; formStr=message.formStr; action=message.action; itemCode=message.itemCode; itemImage=message.itemImage; itemLink=message.itemLink; itemTitle=message.itemTitle; itemUrl=message.itemUrl; commentData=message.commentData; extraInfo=message.extraInfo; combinedInfo=message.combinedInfo; eventAction=message.eventAction; eventReason=message.eventReason;">
                        <div ng-switch on="combinedInfo">
                        <!-- handles these cases, not ng_helpers.profileMessages() -->
                            <div class="animate-switch" ng-switch-when="listenerFacilitationInvite">
                                ${ng_helpers.listenerFacilitationInvite()}
                            </div>
                        </div>
                        <!-- 
                        'listenerFacilitationInvite'
                        ['listenerInvite', 'facilitationInvite']:
                        'listenerSuggestion'
                        ['listenerSuggestion']:
                        'authorInvite'
                        ['authorInvite']:
                        'authorResponse'
                        ['authorResponse']:
                        'commentResponse'
                        ['commentResponse']:
                        'commentOnPhotoOnInitiative'
                        ['commentOnPhoto', 'commentOnInitiative']:
                        'commentOnResource'
                        ['commentOnResource']:
                        'commentOnUpdate'
                        ['commentOnUpdate']:
                        'disabledEnabledDeletedPhoto'
                        ['disabledPhoto', 'enabledPhoto', 'deletedPhoto']:
                        'disabledEnabledDeletedInitiative'
                        ['disabledInitiative', 'enabledInitiative', 'deletedInitiative']:
                        'disabledEnabledDeletedInitiativeResource'
                        ['disabledInitiativeResource', 'enabledInitiativeResource', 'deletedInitiativeResource']:
                        'disabledEnabledDeletedInitiativeUpdate'
                        ['disabledInitiativeUpdate', 'enabledInitiativeUpdate', 'deletedInitiativeUpdate']:
                        'disabledEnabledDeletedAdopted'
                        ['disabled', 'enabled', 'deleted', 'adopted']: -->
                    </div>
                </span>
                
            </div>
            
        </div>

    </div>

</%def>
