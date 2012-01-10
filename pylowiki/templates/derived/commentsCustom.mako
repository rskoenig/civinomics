<%def name="comments( type )">
 % if type == "background":
    <% comments = c.p.comments %>
 % elif type == "suggestion":
    <% comments = c.s.comments %>
    <% issueID = c.i.id %>
 % endif
 %if c.conf['allow.comments'] == 'true':

  <%namespace file="/lib/mako_lib.mako" import="gravatar" />
  <% numComments = len([comment for comment in comments if not comment.disabled and not comment.pending]) %>
  <span class="gray"><a href="#">${numComments} comments</a> | Last edited on ${c.lastmoddate} by ${c.lastmoduser} | <a href="#">Suggest edits</a></span>
  
  <h3>Comments</h3>
    <div id="comments" class="left">
        ${ h.form( url( controller = 'comment', action ='index', id = c.url), method='put' ) }
            <input type="hidden" id="type" name="type" value=${type} />
            % if type == "suggestion":
                <input type="hidden" id="issueID" name="issueID" value=${issueID} />
                <input type="hidden" id="suggestionTitle" name="suggestionTitle" value="${c.s.title}" />
            % endif
            % if "user" in session:
            add a comment
            <br />
            
            <textarea rows="4" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup"></textarea>  
            <div id="comment-preview-div"></div>
            <div style="align:right;text-align:right;">${h.submit('submit', 'Comment')}</div>
            <br />
            % else:
            <h3 class="utility"> 
              Please <a href="/login">login</a> or <a href="/register">register</a> to leave a comment!
              </h3>
            %endif
        ${h.end_form()}
        
        <h4>Featured comments</h4>
        <ul id="featuredComments">
        <%doc>
        ${ h.form( url( controller = 'comment', action ='index', id = c.url), method='put' ) }
            <input type="hidden" id="type" name="type" value=${type} />
            % if type == "suggestion":
                <input type="hidden" id="issueID" name="issueID" value=${issueID} />
                <input type="hidden" id="suggestionTitle" name="suggestionTitle" value="${c.s.title}" />
            % endif
            % if "user" in session:
              <div id="comment-preview-div"></div>
              <textarea rows="4" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup"></textarea>  
              <input type="text" id="sremark"  name="sremark" class="text" />
              <div style="align:right;text-align:right;">${h.submit('submit', 'Comment')}</div>
            % else:
              <h3 class="utility"> 
              Please <a href="/login">login</a> or <a href="/register">register</a> to leave a comment!
              </h3>
            %endif
        ${h.end_form()}
        </%doc>
        
   %for comment in reversed(comments):
   % if not comment.disabled and not comment.pending:
   
     <li>
        <span><img src="/images/avatars/${comment.user.pictureHash}.thumbnail" /> <a href = "/account/${comment.user.name}">${comment.user.name}</a> says ...</span>
        <p>
        <br />
            ${h.literal(h.reST2HTML(comment.data))}
        </p>
        <br />
        <span class="time">${comment.events[-1].date.strftime("%I:%M %p   %m-%d-%Y")}</span><span class="gray"> </span>
     </li>
     
     <%doc>
     <div id="comment" name="comment">
       ${gravatar(comment.events[-1].user.email, 60, float='right')}
       <a href="/account/${comment.event.user.name}">${comment.events[-1].user.name}</a>
       ${comment.events[-1].date.strftime("%I:%M %p   %m-%d-%Y")}
       % try:
         % if session['user'] == comment.event.user.name:
           <a href="/comment/disable/${comment.id}">disable comment</a>
         % endif
       % except KeyError:
       % endtry
       <br>${h.literal(h.reST2HTML(comment.data))}
     </div>
     </%doc>
   % endif
  % endfor
  
  <%doc>
  <h2>Leave a comment</h2>

  ${ h.form( url( controller = 'comment', action ='index', id = c.url), method='put' ) }
    <input type="hidden" id="type" name="type" value=${type} />
    % if type == "suggestion":
        <input type="hidden" id="issueID" name="issueID" value=${issueID} />
        <input type="hidden" id="suggestionTitle" name="suggestionTitle" value="${c.s.title}" />
    % endif
    % if "user" in session:
      <div id="comment-preview-div"></div>
      <textarea rows="4" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup"></textarea>  
      <input type="text" id="sremark"  name="sremark" class="text" />
      <div style="align:right;text-align:right;">${h.submit('submit', 'Comment')}</div>
    % else:
      <h3 class="utility"> 
      Please <a href="/login">login</a> or <a href="/register">register</a> to leave a comment!
      </h3>
    %endif
  ${h.end_form()}
  </%doc>

  <div id="show-comment"><a href="javascript: toggle('comment-section', 'show-comment-link', 'Show all ${numComments} comments')" id="show-comment-link" style="font-size: 12px;">Show all ${numComments} comments</a></div>
 
 %endif

</%def>
