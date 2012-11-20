<%!
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.workshop import getWorkshopsByAccount
    from pylowiki.lib.db.user import isAdmin
    from pylowiki.lib.utils import urlify
%>

<%def name="accountSummary()">
    <% 
        workshops = getWorkshopsByAccount(c.account.id, 'all')
        numWorkshops = len(workshops) 
    %>
    <div class="well">
        <h3>Account Summary</h3>
        <br />
        <strong>Organization Name: </strong> ${c.account['orgName']}<br />
        <strong>Account Type:</strong> ${c.account['type']}<br />
        <strong>Account Workshops:</strong> ${c.account['numHost']}<br />
        <strong>Account Participants:</strong> ${c.account['numParticipants']}<br /><br />

        % if c.account['type'] != 'premium':
            <form action="/accountUpgradeHandler/${c.account['urlCode']}" enctype="multipart/form-data" method="post" class="form-horizontal">
            <button class="btn btn-warning" type="submit" name=doupgrade>Upgrade Your Account</button>
            </form>
            <br /><br />
        % endif

        % if workshops:
            <h3>Account Workshops</h3><br />
            <ul class="unstyled">
            % for w in workshops:
               <li><a href="/workshop/${w['urlCode']}/${w['url']}">${w['title']}</a></li>
            % endfor
            </ul>
        % endif
        % if len(workshops) < int(c.account['numHost']) and c.account['type'] != 'trial':
            <h3>Create a New Workshop</h3><br />
            <form action="/newWorkshop/${c.account['urlCode']}" enctype="multipart/form-data" method="post" class="form-horizontal">
                <div class="control-group">
                    <label for="workshopName" class="control-label">Workshop Name:</label>
                    <div class="controls">
                        <input type="text" id="workshopName" name="workshopName">
                        <button class="btn btn-warning" type="submit" name=newWorkshop>Create Workshop</button>
                    </div> <!-- /.controls -->
                </div> <!-- /.control-group -->

            </form>
        % endif
    </div>
</%def>

<%def name="accountOrg()">
    % if c.account['type'] != 'trial':
        <div class="well">
        <h3>Organization Information</h3>
        <br />
        This information is displayed on your host landing page, with a listing and linking to all of the published workshops under your account.<br />
        <form action="/accountAdminHandler/${c.account['urlCode']}" enctype="multipart/form-data" method="post" class="form-horizontal">
            <div class="control-group">
                <label for="orgName" class="control-label">Organization name:</label>
                <div class="controls">
                   <input type="text" id="orgName" name="orgName" value="${c.account['orgName']}">
                   <span class="help-inline"><span class="label label-important">Required</span></span>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            % if c.account['orgName'] != 'none':
                Your workshop host landing page URL:<br />
                <a href="/host/${urlify(c.account['orgName'])}">http://civinomics.com/host/${urlify(c.account['orgName'])}</a><br />
            % endif
            % if 'pictureHash' in c.account:
                <%
                   pictureHash = c.account['pictureHash']
                   directoryNumber = c.account['directoryNumber']
                %>
                <img src="/images/avatar/${directoryNumber}/profile/${pictureHash}.profile" alt="${c.account['orgName']}" title="${c.account['orgName']}" class="thumbnail" style="display: block; margin-left: auto; margin-right: auto;">
            % endif
            <div class="control-group">
                <label for="pictureFile" class="control-label">Organization logo image upload:</label>
                <div class="controls">
                        ${h.file("pictureFile")}
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->

            <div class="control-group">
                <label for="orgEmail" class="control-label">Organization contact email address:</label>
                <div class="controls">
                   <input type="text" id="orgEmail" name="orgEmail" value="${c.account['orgEmail']}">
                   <span class="help-inline"><span class="label label-important">Required</span></span>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group --> 
            <div class="control-group">
                <label for="orgLink" class="control-label">Organization web site:</label>
                <div class="controls">
                   <input type="text" id="orgLink" name="orgLink" value="${c.account['orgLink']}">
                </div> <!-- /.controls -->
            </div> <!-- /.control-group -->
            <div class="control-group">
                <label for="orgLink" class="control-label">Organization web site description:</label>
                <div class="controls">
                   <textarea rows="4" cols="50" id="orgLinkDesc" name="orgLinkDesc">${c.account['orgLinkDesc']}</textarea>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group --> 
            <div class="control-group">
                <label for="orgMessage" class="control-label">Welcome message:</label>
                <div class="controls">
                   <textarea rows="4" cols="40" id="orgMessage" name="orgMessage"">${c.account['orgMessage']}</textarea>
                </div> <!-- /.controls -->
            </div> <!-- /.control-group --> 
            <fieldset>
            <fieldset>
                <div>
                    <button class="btn btn-warning" type="submit">
                    Save changes
                    </button>
                </div>
            </fieldset>
            </form>
        </div><!-- well -->
        % endif
</%def>

<%def name="accountAdmin()">

    <div class="well">
        <h3>Account Administration</h3><br />

        <strong>Administrators</strong><br />
        <form action="/accountAdminHandler/${c.account['urlCode']}" enctype="multipart/form-data" method="post" class="form-horizontal">

        <% alen = len(c.admins) %> 
        % if c.authuser in c.admins:
            <div class="row">
            <div class="span1"></div><!-- span1 -->
            <div class="span3"><a href="/profile/${c.authuser['urlCode']}/${c.authuser['url']}">${c.authuser['name']}</a>  (You)</div><!-- span3 -->
            </div><!-- row -->
        % endif
        % for admin in c.admins:
            % if alen > 1 and c.authuser['email'] != admin['email']:
                <div class="row">
                <div class="span1"></div><!-- span1 -->
                <div class="span3"><a href="/profile/${admin['urlCode']}/${admin['url']}">${admin['name']}</a></div><!-- span3 -->
                <div class="span3"><button type="submit" class="btn btn-danger" name="deleteAdmin" value="${admin['email']}">Delete Admin</button> <input type=checkbox name="confirmAdmin|${admin['email']}"> confirm</div><!-- span3 -->
                </div><!-- row -->
            % endif
            
        % endfor
        % for email in c.emails:
            <div class="row">
            <div class="span1"></div><!-- span1 -->
            <div class="span3">${email}</div><!-- span3 -->
            <div class="span3"><button type="submit" class="btn btn-danger" name="deleteAdmin" value="${email}">Delete Admin</button> <input type=checkbox name="confirmAdmin|${email}"></div><!-- span3 -->      
            </div><!-- row -->
        % endfor
        </ul>
        % if c.account['type'] != 'trial':
            <br />
            <strong>Add a new administrator to this account</strong><br />
            <div class="control-group">
                <label for="orgName" class="control-label">Administrator email:</label>
                <div class="controls">
                <input type="text" id="adminEmail" name="adminEmail">
                <button class="btn btn-warning" name="addAdmin" type=submit>Add Admin</button>
            </div> <!-- /.control-group -->
        % endif
        </form>

        % if c.events:
            <br /><br />
            <strong>Account Event Log</strong><br />
            % for event in c.events:
                &nbsp; &nbsp; &nbsp; ${event['title']} ${event['data']} ${event.date}<br />
            % endfor
        % endif
    </div><!-- well -->
</%def>
  

<%def name="basicButton()">
    <strong>Civinomics Basic</strong><br>
    Up to 5 workshops, up to 100 contributors, Unlimited lurkers<br>
    <button class="btn btn-warning" name="upgrade" value="basic" type=submit>Upgrade to Civinomics Basic</button>
    <br /><br />
</%def>

<%def name="plusButton()">
    <strong>Civinomics Plus</strong><br>
    Up to 10 workshops, up to 500 contributors, Unlimited lurkers<br>
    <button class="btn btn-warning" name="upgrade" value="plus" type=submit>Upgrade to Civinomics Plus</button>
    <br /><br />
</%def>

<%def name="premiumButton()">
    <strong>Civinomics Premium</strong><br>
    Up to 20 workshops, up to 1000 contributors, Unlimited lurkers<br>
    <button class="btn btn-warning" name="upgrade" value="premium" type=submit>Upgrade to Civinomics Premium</button>
    <br /><br />
</%def>

<%def name="accountUpgrade()">
    <br /><br />
    <%
        workshops = getWorkshopsByAccount(c.account.id)
        numWorkshops = len(workshops)
    %>
    
    <form action="/accountUpgradeHandler/${c.account['urlCode']}" enctype="multipart/form-data" method="post" class="form-horizontal">
    Current account type:<br />
    % if c.account['type'] == 'trial':
        Trial account, 1 workshop, up to 10 private participants<br /><br />
        ${basicButton()}
        ${plusButton()}
        ${premiumButton()}
        
    % elif c.account['type'] == 'basic':
        Basic account, up to 5 workshops, up to 100 active contributors<br /><br />
        ${plusButton()}
        ${premiumButton()}
    % elif c.account['type'] == 'plus':
        Plus account, up to 10 workshops, up to 500 active contributors<br /><br />
        ${premiumButton()}
    % elif c.account['type'] == 'premium':
        Premium account, up to 20 workshops, up to 1000 active contributors<br /><br />
        Call for a custom account!<br /><br />
    % endif
    </form>
</%def>



