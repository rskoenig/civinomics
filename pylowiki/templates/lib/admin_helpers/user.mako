<%!
    from pylowiki.lib.db.user import getUserByID
%>  

<%def name="user()">
    <div class="page-header">
        <h1><a href="/profile/${c.user['urlCode']}/${c.user['url']}">${c.title}</a></h1>
    </div>     
    <br /><br />
</%def>

<%def name="user_events()">
    % if c.events:
       <% numEvents = len(c.events) %>
       <% eString = "Events" %>
       % if numEvents == 1:
          <% eString = "Event" %>
       % endif
       <strong>${numEvents} ${eString}:</strong>
       <br /><br />
       % for event in c.events:
          <% user = getUserByID(event.owner) %>
          ${event['title']} ${event.date} by ${user['name']}<br />
          Reason: ${event['data']}
          <br /><br />
       %endfor
    % endif
</%def>

<%def name="user_admin()">
    <p>
    <strong class="gray">Administrate Member</strong>
    <br /><br />
    % if c.user['disabled'] == '1':
       <% eAction = 'Enable' %>
    % else:
       <% eAction = 'Disable' %>
    % endif
    <br /><br />
    <strong>${eAction} Member</strong><br /><br />
    <form method="post" name="enableUser" id="enableUser" action="/profile/${c.user['urlCode']}/${c.user['url']}/enable/">
       Reason for Member ${eAction}: <input type=text name=enableUserReason> <br /><br />
       <input type=radio name="verifyEnableUser" value="0"> Verify ${eAction}
       &nbsp;&nbsp;<button type="submit" class="btn btn-warning">${eAction} Member</button>
    </form>
    <br /><br />
    <strong>Change Access Level</strong><br /><br />
    Current Access Level: ${c.user['accessLevel']}
    <form method="post" name="userPrivs" id="userPrivs" action="/profile/${c.user['urlCode']}/${c.user['url']}/privs/">
     Reason for Member Access Level Change: <input type=text name=changeAccessReason><br /><br /> 
     % if c.user['accessLevel'] == '0':
        <input type=radio name="setPrivsFacil" value="100"> Facilitator &nbsp; &nbsp; &nbsp;
        <input type=radio name="setPrivsAdmin" value="200"> Admin
     % elif c.user['accessLevel'] == '100':
        <input type=radio name="setPrivsUser" value="0"> User &nbsp; &nbsp; &nbsp;
        <input type=radio name="setPrivsAdmin" value="200"> Admin
     % else:
        <input type=radio name="setPrivsUser" value="0"> User &nbsp; &nbsp; &nbsp;
        <input type=radio name="setPrivsFacil" value="100"> Facilitator
     % endif
     &nbsp;&nbsp;<button type="submit" name="setPrivs" class="btn btn-warning">Set Privs</button>
     </form>
    <br /><br />
    % if c.account:
       <strong>User Account</strong><br /><br />
       Total hosting for account: ${c.account['numHost']}<br /> 
       <% numWorkshops = len(c.workshops) %>
       Total workshops hosted for account: ${numWorkshops}<br /> 
       % if c.workshops:
          % for w in c.workshops:
             &nbsp; &nbsp; &nbsp; &bull; &nbsp;<a href="/workshop/${w['urlCode']}/${w['url']}">${w['title']}</a>
             <br />
          % endfor
       % endif
       Total hosted remaining for account: ${c.account['numRemaining']}<br /> 
       <br /><br /> 
       <form method="post" name="userAccount" id="userAccount" action="/profile/${c.user['urlCode']}/${c.user['url']}/account/">
       Change number of objects which may be hosted: 
       <select name="numHost">
         % for i in range(1, 11):
          <option>${i}</option>
         % endfor
       </select>
       <br /><br />
       <button type="submit" class="btn btn-warning">Update Account</button>
       </form> 
    % else:
       <strong>Create User Account</strong><br /><br />
       <form method="post" name="userAccount" id="userAccount" action="/profile/${c.user['urlCode']}/${c.user['url']}/account/">
       Number of objects which may be hosted: 
       <select name="numHost">
          % for i in range(1, 11):
            <option>${i}</option>
          % endfor
       </select>
       <br /><br />
       <button type="submit" class="btn btn-warning">Add Account</button>
       </form> 
    % endif
</%def>
