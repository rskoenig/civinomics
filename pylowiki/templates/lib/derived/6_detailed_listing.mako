<%!
   from pylowiki.lib.db.user import getUserByID
%>

<%namespace name="lib_6" file="/lib/6_lib.mako" />

<%def name="showListing(thing)">
   <%
      if c.paginator != '':
         renderList = c.paginator
      else:
         if thing == 'discussion':
            renderList = c.discussions
   %>
   <ul class="unstyled">
      % for item in renderList:
         <% author = getUserByID(item.owner) %>
         <li>
            <div class="row-fluid list-item">
               <div class="span1 voteBlock">
                  ${lib_6.upDownVote(item)}
               </div>
               <div class="span2">
                  ${lib_6.userImage(author, className = 'avatar')}
               </div> <!--/.span2-->
               <div class="span9 list-item-text">
                  <% itemTitle = '<h5><a %s>%s</a></h5>' %(lib_6.discussionLink(item, c.w, embed=True), item['title']) %>
                  ${itemTitle | n}
               </div><!--/.span9-->
            </div><!--/.row-fluid-->
         </li>
      % endfor
   </ul>
</%def>

<%doc>
<%def name="listDiscussions()">
    % if c.discussions:
        % if c.paginator:
            <% dList = c.paginator %>
        % else:
            <% dList = c.discussions %>
        % endif
        <ul class="unstyled civ-col-list">
            % for discussion in dList:
                <li>
                    <div class="row-fluid">
                        <div class="span1 civ-votey">
                            ${displayDiscussionRating(discussion)}
                        </div> <!-- /.civ-votey -->
                        <div class="span1">
                            ${userphoto(discussion)}
                        </div> <!-- /.civ-votey -->    
                        <div class="span8">        
                                <h4>${displayDiscussionTitle(discussion)}</h4>
                                ${discussionMetaData(discussion)}
                        </div><!-- span8 -->
                    </div> <!-- /.row-fluid -->
                    <div class="row-fluid">
                        <div class="span1">
                        </div>
                        <div class="span8">
                            ${discussionPostedDate(discussion)}
                        </div><!-- span9 -->
                    </div><!-- row-fluid -->
                </li>
            % endfor
        </ul>
    % else:
        <div class="alert alert-warning">No discussions to show.</div>
    % endif
</%def>
</%doc>