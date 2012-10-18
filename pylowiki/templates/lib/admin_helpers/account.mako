<%!
    from pylowiki.lib.db.user import getUserByID
    from pylowiki.lib.db.flag import getFlags
%>

<%def name="accountAdmin()">
    <form action="/account/editSumbit" enctype="multipart/form-data" method="post" class="form-horizontal">
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
               <span class="help-inline"><span class="label label-important">Required</span></span>
            </div> <!-- /.controls -->
        </div> <!-- /.control-group --> 
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
