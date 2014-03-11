<%!
    import logging, os
    log = logging.getLogger(__name__)
%> 

<%namespace name="lib_6" file="/lib/6_lib.mako" />
<%namespace name="ng_messages" file="/lib/ng_messages.mako" />

<%def name="listProfileMessages()">
    <!-- this init clause covers all varaiables that can possibly be used in the following cases -->
    <div ng-init="messageCode=message.messageCode; action=message.action; combinedInfo=message.combinedInfo; commentData=message.commentData; eventAction=message.eventAction; eventReason=message.eventReason; extraInfo=message.extraInfo; formLink=message.formLink;fuzzyTime=message.fuzzyTime; itemCode=message.itemCode; itemImage=message.itemImage; itemLink=message.itemLink; itemTitle=message.itemTitle; itemUrl=message.itemUrl; messageDate=message.messageDate; messageText=message.messageText; messageTitle=message.messageTitle; read=message.read; rowClass=message.rowClass; responseAction=message.responseAction; userImage=message.userImage; userName=message.userName; userLink=message.userLink;">
        <div ng-controller="messageDisplayCtrl">
            <div ng-click="updateReadStatus(false)" class="{{classUnread}}">
                <div class="{{classUnread}} border-top" style="padding: 10px;">
                    <table class="message-table " data-code="{{messageCode}}">
                        <tr>
                          <td class="avatar-cell" rowspan="3"><img class="avatar" src="{{userImage}}" title="{{userName}}" alt="{{userName}}"></td>
                          <td></td>
                        </tr>
                        <tr>
                          <td>
                            <div class="activity-item-content-header">
                                <a ng-href="{{userLink}}" class="green green-highlight"><strong>{{userName}}</strong></a>
                                <strong>{{messageTitle}}</strong> 
                                <span class="date pull-right">{{fuzzyTime}} ago</span>
                            </div>
                          </td>
                        </tr>
                        <tr ng-switch on="combinedInfo">
                            <td ng-switch-when="listenerFacilitationInvite">
                                ${ng_messages.listenerFacilitationInvite()}
                            </td>
                            <td ng-switch-when="listenerSuggestion">
                                ${ng_messages.listenerSuggestion()}
                            </td>
                            <td ng-switch-when="authorInvite">
                                ${ng_messages.authorInvite()}
                            </td>
                            <td ng-switch-when="authorResponse">
                                ${ng_messages.authorResponse()}
                            </td>
                            <td ng-switch-when="commentResponse">
                                ${ng_messages.commentResponse()}
                            </td>
                            <td ng-switch-when="commentOnPhotoOnInitiative">
                                ${ng_messages.commentOnPhotoOnInitiative()}
                            </td>
                            <td ng-switch-when="commentOnResource">
                                ${ng_messages.commentOnResource()}
                            </td>
                            <td ng-switch-when="commentOnUpdate">
                                ${ng_messages.commentOnUpdate()}
                            </td>
                            <td ng-switch-when="disabledEnabledDeletedPhoto">
                                ${ng_messages.disabledEnabledDeletedPhoto()}
                            </td>
                            <td ng-switch-when="disabledEnabledDeletedInitiative">
                                ${ng_messages.disabledEnabledDeletedInitiative()}
                            </td>
                            <td ng-switch-when="disabledEnabledDeletedInitiativeResource">
                                ${ng_messages.disabledEnabledDeletedInitiativeResource()}
                            </td>
                            <td ng-switch-when="disabledEnabledDeletedInitiativeUpdate">
                                ${ng_messages.disabledEnabledDeletedInitiativeUpdate()}
                            </td>
                            <td ng-switch-when="disabledEnabledDeletedAdopted">
                                ${ng_messages.disabledEnabledDeletedAdopted()}
                            </td>
                            <td ng-switch-default>
                                <p>Default Message</p>
                            </td>

                        </tr>
                    </table>
                </div>
            </div>
        </div>

    </div>

</%def>