<%def name="comments( )">

 %if c.conf['allow.comments'] == 'true':

  <%namespace file="/lib/mako_lib.mako" import="gravatar" />

  <div id="comment-section" name="comment-section">
  <h2 id="comments">Comments</h2>
  %for comment in reversed(c.p.comments):
   % if not comment.disabled:
     <div id="comment" name="comment">
       ${gravatar(comment.event.user.email, 60, float='right')}
       <a href="/account/${comment.event.user.name}">${comment.event.user.name}</a>
       ${comment.event.date.strftime("%I:%M %p   %m-%d-%Y")}
       % try:
         % if session['user'] == comment.event.user.name:
           <a href="/comment/disable/${comment.id}">disable comment</a>
         % endif
       % except KeyError:
       % endtry
       <br>${h.literal(h.reST2HTML(comment.data))}
     </div>
   % endif
  % endfor

  <h2>Leave a comment</h2>

  ${ h.form( url( controller = 'comment', action ='index', id = c.url ), method='put' ) }
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

  </div>

  <div id="show-comment"><a href="javascript: toggle('comment-section', 'show-comment-link', 'Show all ${len(c.p.comments)} comments')" id="show-comment-link" style="font-size: 12px;">Show all ${len(c.p.comments)} comments</a></div>
 
 %endif

</%def>
