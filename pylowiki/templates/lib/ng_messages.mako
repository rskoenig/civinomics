<%def name="listenerFacilitationInvite()">
    <div ng-if="isRead(read)">
        <div class="media">
            <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left message-workshop-image">
            <div class="media-body">
                <h5 class="media-heading">
                    {{messageTitle}}
                </h5>
                <p>
                    <a ng-href="{{userLink}}">{{userName}}</a>
                    invites you to facilitate 
                    <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                </p>
                <p>
                    {{messageText}}
                </p>
                <p>
                    (You have already responded by 
                    {{responseAction}})
                </p>
                <p class="pull-right"><small>
                    {{fuzzyTime}} ago
                </small></p>
            </div>
        </div>
    </div> <!-- end if read -->
    <div ng-if="notRead(read)">
        <form method="post" name="inviteListener" id="inviteListener" action="{{formLink}}">
            <input type="hidden" name="workshopCode" value="{{itemCode}}">
            <input type="hidden" name="workshopURL" value="{{itemUrl}}">
            <input type="hidden" name="messageCode" value="{{messageCode}}">
            <div class="media">
                <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left message-workshop-image">
                <div class="media-body">
                    <h5 class="media-heading">
                        {{messageTitle}}
                    </h5>
                    <p>
                        <a ng-href="{{userLink}}">{{userName}}</a>
                        invites you to 
                        {{action}}
                        <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                    </p>
                    <p>
                        {{messageText}}
                    </p>
                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{action}} the workshop">Accept</button>
                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{action}} the workshop">Decline</button>
                    <p class="pull-right"><small>
                        {{fuzzyTime}} ago
                    </small></p>
                </div>
            </div>
        </form>
    </div> <!-- end if not read -->
</%def>

<%def name="listenerSuggestion()">
    <div class="media">
        <div class="media-body">
            <h5 class="media-heading">
                {{messageTitle}}
            </h5>
            <p>
                Member 
                <a ng-href="{{userLink}}">{{userName}}</a>
                has a listener suggestion for workshop 
                <a ng-href="{{itemLink}}">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="authorInvite()">
    <div ng-if="isRead(read)">
        <div class="media">
            <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left message-workshop-image">
            <div class="media-body">
                <h5 class="media-heading">
                    {{messageTitle}}
                </h5>
                <p>
                    <a ng-href="{{userLink}}">{{userName}}</a>
                    invites you to facilitate 
                    <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                </p>
                <p>
                    {{messageText}}
                </p>
                <p>
                    (You have already responded by 
                    {{responseAction}})
                </p>
                <p class="pull-right"><small>
                    {{fuzzyTime}} ago 
                    
                </small></p>
            </div>
        </div>
    </div> <!-- end if read -->
    <div ng-if="notRead(read)">
        {{formStr}}
            <input type="hidden" name="initiativeCode" value="{{itemCode}}">
            <input type="hidden" name="initiativeURL" value="{{itemUrl}}">
            <input type="hidden" name="messageCode" value="{{messageCode}}">
            <div class="media">
                <img ng-src="{{itemImage}}" alt="{{itemTitle}}" title="{{itemTitle}}" class="pull-left message-workshop-image">
                <div class="media-body">
                    <h5 class="media-heading">
                        {{messageTitle}}
                    </h5>
                    <p>
                        <a ng-href="{{userLink}}">{{userName}}</a>
                        invites you to 
                        {{action}} 
                        <a ng-href="{{itemLink}}">{{itemTitle}}</a>
                    </p>
                    <p>
                        {{messageText}}
                    </p>
                    <button type="submit" name="acceptInvite" class="btn btn-mini btn-civ" title="Accept the invitation to {{action}} the initiative">Accept</button>
                    <button type="submit" name="declineInvite" class="btn btn-mini btn-danger" title="Decline the invitation to {{action}} the initiative">Decline</button>
                    <p class="pull-right"><small>
                        {{fuzzyTime}} ago
                    </small></p>
                </div>
            </div>
        </form>
    </div> <!-- end if not read -->
</%def>

<%def name="authorResponse()">
    <div class="media">
        <div class="media-body">
            <h5 class="media-heading">
                {{messageTitle}}
            </h5>
            <p>
                <a ng-href="{{userLink}}">{{userName}}</a>
                {{messageText}} 
                <a ng-href="{{itemLink}}">{{itemTitle}}</a>
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="commentResponse()">
    <div class="media">
        <div class="media-body">
            <h5 class="media-heading">
                <a ng-href="{{userLink}}">{{userName}}</a>
                {{messageTitle}}
            </h5>
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="commentOnPhotoOnInitiative()">
    <div class="media">
        <div class="media-body">
            <h5 class="media-heading">
                <a ng-href="{{userLink}}">{{userName}}</a>
                {{messageTitle}}
            </h5>
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{commentData}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="commentOnResource()">
    <div class="media">
        <div class="media-body">
            <h5 class="media-heading">
                <a ng-href="{{userLink}}">{{userName}}</a>
                {{messageTitle}}
            </h5>
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="commentOnUpdate()">
    <div class="media">
        <div class="media-body">
            <h5 class="media-heading">
                <a ng-href="{{userLink}}">{{userName}}</a>
                {{messageTitle}}
            </h5>
            <p>
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedPhoto()">
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading centered">
                {{messageTitle}}
            </h4>
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your photo:
                <!-- note: photo needs a link to the unpublished page, link to src of image and title -->
                <img ng-src="{{itemLink}}" class="green green-hover" title="{{itemTitle}}" alt="{{itemTitle}}">
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedInitiative()">
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading centered">
                {{messageTitle}}
            </h4>
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your initiative:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedInitiativeResource()">
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading centered">
                {{messageTitle}}
            </h4>
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your initiative resource:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedInitiativeUpdate()">
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading centered">
                {{messageTitle}}
            </h4>
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                Your initiative update:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>

<%def name="disabledEnabledDeletedAdopted()">
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading centered">
                {{messageTitle}}
            </h4>
            <p>
                It was 
                {{eventAction}} 
                because: 
                {{eventReason}}
            </p>
            <p>
                You posted:
                <a ng-href="{{itemLink}}" class="green green-hover">{{itemTitle}}</a>
            </p>
            <p>
                {{messageText}}
            </p>
            <p class="pull-right"><small>
                {{fuzzyTime}} ago 
                
            </small></p>
        </div>
    </div>
</%def>