<%!
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.workshop import getWorkshopsByAccount
%>

<%def name="accountAdmin()">
    <br /><br />
    <% 
        workshops = getWorkshopsByAccount(c.account.id)
        numWorkshops = len(workshops) 
    %>
    <table class="table table-bordered">
    <tr><td>
    <h3>Account Information</h3>
    <br />
    <strong>Account Type:</strong> ${c.account['type']}<br />
    <strong>Account Workshops:</strong> ${c.account['numHost']}<br />
    <strong>Account Participants:</strong> ${c.account['numParticipants']}<br /><br />
    % if workshops:
        <strong>Workshops Under This Account</strong><br />
        <ul class="unstyled">
        % for w in workshops:
           <li><a href="/workshop/${w['urlCode']}/${w['url']}">${w['title']}</a></li>
        % endfor
        </ul>
    % endif
    </td></tr>
    </table>
    <br /><br />

    <table class="table table-bordered">
    <tr><td>
    <h3>Organization Information</h3>
    <br />
    <form action="/accountAdminHandler/${c.account['urlCode']}" enctype="multipart/form-data" method="post" class="form-horizontal">
        <div class="control-group">
            <label for="orgName" class="control-label">Organization name:</label>
            <div class="controls">
               <input type="text" id="orgName" name="orgName" value="${c.account['orgName']}">
               <span class="help-inline"><span class="label label-important">Required</span></span>
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
            <label for="orgMessage" class="control-label">Organization web site:</label>
            <div class="controls">
               <input type="text" id="orgLink" name="orgLink" value="${c.account['orgLink']}">
            </div> <!-- /.controls -->
        </div> <!-- /.control-group --> 
        <fieldset>
            <div>
                <button class="btn btn-warning" type="submit">
                Save changes
                </button>
            </div>
        </fieldset>
        </td></tr>
        </table>

        % if c.admins:
            <br />
            <strong>Account Admins</strong><br />
            <ul class="unstyled">
            % for admin in c.admins:
                <li><a href="/profile/${admin['urlCode']}/${admin['url']}">${admin['name']}</a></li>
            % endfor
            </ul>
        % endif
       
    </form>
</%def>
