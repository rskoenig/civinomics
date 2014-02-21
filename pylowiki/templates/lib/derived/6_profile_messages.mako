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
<%namespace name="ng_messages" file="/lib/ng_messages.mako" />

<%def name="listProfileMessages()">
    <div ng-init="code = '${c.userCode}'; url = '${c.userUrl}'">
        <div class="browse" ng-controller="profileMessagesCtrl">

            <div class="row-fluid" ng-repeat="message in messages" ng-cloak>

                <div class="media-body object-in-listing {{message.rowClass}} border-bottom" data-code="{{message.messageCode}}">
                    
                    <div class="span2 message-avatar">
                        <img src="{{message.userImage}}" title="{{message.userName}}" alt="{{message.userName}}">
                    </div>
                    <div class="span8 message-content">
                        <!-- this init clause covers all varaiables that can possibly be used in the following cases -->
                        <div ng-init="action=message.action; combinedInfo=message.combinedInfo; commentData=message.commentData; eventAction=message.eventAction; eventReason=message.eventReason; extraInfo=message.extraInfo; formLink=message.formLink; fuzzyTime=message.fuzzyTime; itemCode=message.itemCode; itemImage=message.itemImage; itemLink=message.itemLink; itemTitle=message.itemTitle; itemUrl=message.itemUrl; messageCode=message.messageCode; messageDate=message.messageDate; messageText=message.messageText; messageTitle=message.messageTitle; read=message.read; rowClass=message.rowClass; responseAction=message.responseAction; userImage=message.userImage; userName=message.userName; userLink=message.userLink;">
                            <p>{{message.combinedInfo}}</p>
                            <p>{{message.extraInfo}}</p>
                            <div ng-switch on="combinedInfo">
                            <!-- handles these cases, not ng_messages.profileMessages() -->
                                <div ng-switch-when="listenerFacilitationInvite">
                                    ${ng_messages.listenerFacilitationInvite()}
                                </div>
                                <div ng-switch-when="listenerSuggestion">
                                    ${ng_messages.listenerSuggestion()}
                                </div>
                                <div ng-switch-when="authorInvite">
                                    ${ng_messages.authorInvite()}
                                </div>
                                <div ng-switch-when="authorResponse">
                                    ${ng_messages.authorResponse()}
                                </div>
                                <div ng-switch-when="commentResponse">
                                    ${ng_messages.commentResponse()}
                                </div>
                                <div ng-switch-when="commentOnPhotoOnInitiative">
                                    ${ng_messages.commentOnPhotoOnInitiative()}
                                </div>
                                <div ng-switch-when="commentOnResource">
                                    ${ng_messages.commentOnResource()}
                                </div>
                                <div ng-switch-when="commentOnUpdate">
                                    ${ng_messages.commentOnUpdate()}
                                </div>
                                <div ng-switch-when="disabledEnabledDeletedPhoto">
                                    ${ng_messages.disabledEnabledDeletedPhoto()}
                                </div>
                                <div ng-switch-when="disabledEnabledDeletedInitiative">
                                    ${ng_messages.disabledEnabledDeletedInitiative()}
                                </div>
                                <div ng-switch-when="disabledEnabledDeletedInitiativeResource">
                                    ${ng_messages.disabledEnabledDeletedInitiativeResource()}
                                </div>
                                <div ng-switch-when="disabledEnabledDeletedInitiativeUpdate">
                                    ${ng_messages.disabledEnabledDeletedInitiativeUpdate()}
                                </div>
                                <div ng-switch-when="disabledEnabledDeletedAdopted">
                                    ${ng_messages.disabledEnabledDeletedAdopted()}
                                </div>
                                <div ng-switch-default>
                                    <p>Default Message</p>
                                </div>
                            </div>
                            <!-- 
                            "listenerFacilitationInvite" == ["listenerInvite", "facilitationInvite"]:
                            
                            "listenerSuggestion" == ["listenerSuggestion"]:
                            
                            "authorInvite" == ["authorInvite"]:
                            
                            "authorResponse" == ["authorResponse"]:
                            
                            "commentResponse" == ["commentResponse"]:
                            
                            "commentOnPhotoOnInitiative" == ["commentOnPhoto", "commentOnInitiative"]:
                            
                            "commentOnResource" == ["commentOnResource"]:
                            
                            "commentOnUpdate" == ["commentOnUpdate"]:
                            
                            "disabledEnabledDeletedPhoto" == ["disabledPhoto", "enabledPhoto", "deletedPhoto"]:
                            
                            "disabledEnabledDeletedInitiative" == ["disabledInitiative", "enabledInitiative", "deletedInitiative"]:
                            
                            "disabledEnabledDeletedInitiativeResource" == ["disabledInitiativeResource", "enabledInitiativeResource", "deletedInitiativeResource"]:
                            
                            "disabledEnabledDeletedInitiativeUpdate" == ["disabledInitiativeUpdate", "enabledInitiativeUpdate", "deletedInitiativeUpdate"]:
                            
                            "disabledEnabledDeletedAdopted" == ["disabled", "enabled", "deleted", "adopted"]: -->
                        </div>
                    </span>
                    
                </div>
                
            </div>

        </div>

    </div>

</%def>
