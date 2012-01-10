<%def name="comments( type )">
 % if type == "background":
    <% comments = c.p.comments %>
 % elif type == "suggestion":
    <% comments = c.s.comments %>
    <% issueID = c.i.id %>
    <%! from pylowiki.model import getRatingForComment %>
 % endif
 %if c.conf["allow.comments"] == "true":

  <% numComments = len([comment for comment in comments if not comment.disabled and not comment.pending]) %>
  
  <h3 class="clr">Comments</h3>
    <div id="comments" class="left">
        % if "user" in session:
            <form class="left" id="add_comment" action = "/comment/index/${c.url}">
            <input type="hidden" id="type" name="type" value=${type} />
            
            % if type == "suggestion":
                <input type="hidden" id="issueID" name="issueID" value=${issueID} />
                <input type="hidden" id="suggestionTitle" name="suggestionTitle" value="${c.s.title}" />
            % endif
            
            add a comment
            <br />
            ##<textarea id="comment"></textarea>
            <textarea rows="4" id="comment-textarea" name="comment-textarea" onkeyup="previewAjax( 'comment-textarea', 'comment-preview-div' )" class="markitup"></textarea>  
            ##<div style="align:right;text-align:right;">${h.submit("submit", "Comment")}</div>
            <div id="comment-preview-div"></div>
            <br />
            <button type="submit" class="right green" value = "comment">Submit</button>
        </form>
        % else:
            <h3 class="utility"> 
                Please <a href="/login">login</a> or <a href="/register">register</a> to leave a comment!
            </h3>
        % endif
    
        <h4>Featured comments</h4>
        <ul id="featuredComments">
        % if numComments == 0:
            No Comments!
        % else:
            <% counter = 1 %>
            % for comment in reversed(comments):
                
                % if not comment.disabled and not comment.pending:
                    <li>
                        <span><img src="/images/avatars/${comment.user.pictureHash}.thumbnail" /> <a href="/account/${comment.user.name}">${comment.user.name}</a> says ...</span>
                        <br />
                            ${h.literal(h.reST2HTML(comment.data))}     
                        <br />
                        <div class="gray comment_data left">
                            <p class="time">${comment.events[-1].date.strftime("%I:%M %p   %m-%d-%Y")}</p>
                            <%doc>
                            <p>
                                <a href="#" class="gray flag">Flag comment</a>
                                <a href="#" class="gray reply">Reply</a>
                            </p>
                            </%doc>
                            
                            % if "user" in session:
                                <% userRating = getRatingForComment(comment.id, c.authuser.id) %>
                                % if not userRating:
                                    <% userRating = 0 %>
                                % endif
                                <div class="comment_${counter} star-rating" data="${comment.avgRating}_${comment.id}_${userRating.rating}"></div> 
                                <script type="text/javascript">
                                $(document).ready(function(){
                                    $(".comment_${counter}").jRating({
                                        type:'small',
                                        ratingType: 'comment'
                                    });
                                });
                                </script>
                                <br/>
                                % if not comment.avgRating:
                                    <div class = "avgCRating_${comment.id} right">Average rating: unrated!</div>
                                    <br/>
                                % else:
                                    <div class = "avgCRating_${comment.id} right">Average rating: ${comment.avgRating}</div>
                                    <br/>
                                % endif
                                % if not getRatingForComment(comment.id, c.authuser.id):
                                    <div class = "yourCRating_${comment.id} right">Your rating: unrated! </div>
                                    <br/>
                                % else:
                                    <div class = "yourCRating_${comment.id} right">Your rating: ${getRatingForComment(comment.id, c.authuser.id).rating} </div>
                                    <br/>
                                % endif
                            % else:
                                <div class = "gray rating wide">
                                    <div class="comment_${counter}" data="0_${c.s.id}_${comment.id}_0"></div> 
                                    <script type="text/javascript">
                                    $(document).ready(function(){
                                        $(".comment_${counter}").jRating({
                                             type:'small',
                                            ratingType: 'comment'
                                        });
                                    });
                                    </script>
                                </div>
                            % endif
                            
                        </div><!-- comment_data -->
                        <%doc>
                        <div class="flag content left">
                            <form action="" class="left wide">
                                <span class="dark-text">Please explain why you are flagging this content:</span>
                                <br />
                                <textarea name="flag" class="content_feedback"></textarea>
                                <button type="submit" class="green">Submit</button>
                            </form>
                        </div><!-- flag_content -->
                        <div class="reply content left">
                            <form action="">
                                <textarea name="reply" class="content_feedback"></textarea>
                                <button type="submit" class="green">Submit</button>
                            </form>
                        </div>
                        </%doc>
                    </li>
                % endif
                <% counter += 1 %>
            % endfor
        % endif
        </ul>
        <%doc>
            <li>
                <span><img src="images/Monster_icon_25x25.jpg" /> <a href="profile.html">Monster</a> says ...</span>
                <br />
                <p>
                    Magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip
                </p>
                <br />
                <div class="gray comment_data left">
                    <p class="time">Posted 15 minutes ago</p>
                    <p>
                        <a href="#" class="gray flag">Flag comment</a>
                        <a href="#" class="gray reply">Reply</a>
                    </p>
                    <p class="thumbs up">
                        <span class="dark-text"> 14 </span>
                        <a href="#">thumbs up</a>
                    </p><!-- thumbs up -->
                    <p class="thumbs down">
                        <span class="dark-text"> 7 </span>
                        <a href="#">thumbs down</a>
                    </p><!-- thumbs down -->
                </div><!-- comment_data -->
                <div class="flag content left">
                    <form action="" class="left wide">
                        <span class="dark-text">Please explain why you are flagging this content:</span>
                        <br />
                        <textarea name="flag" class="content_feedback"></textarea>
                        <button type="submit" class="green">Submit</button>
                    </form>
                </div><!-- flag_content -->
                <div class="reply content left">
                    <form action="">
                        <textarea name="reply" class="content_feedback"></textarea>
                        <button type="submit" class="green">Submit</button>
                    </form>
                </div>
            </li>
            <li>
                <span><img src="img/Monster_icon_25x25.jpg" /> <a href="profile.html">Monster</a> says ...</span>
                <br />
                <p>
                    Dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui
                </p>
                <br />
                <div class="gray comment_data left">
                    <p class="time">Posted 15 minutes ago</p>
                    <p>
                        <a href="#" class="gray flag">Flag comment</a>
                        <a href="#" class="gray reply">Reply</a>
                    </p>
                    <p class="thumbs up">
                        <span class="dark-text"> 14 </span>
                        <a href="#">thumbs up</a>
                    </p><!-- thumbs up -->
                    <p class="thumbs down">
                        <span class="dark-text"> 7 </span>
                        <a href="#">thumbs down</a>
                    </p><!-- thumbs down -->
                </div><!-- comment_data -->
                <div class="flag content left">
                    <form action="" class="left wide">
                        <span class="dark-text">Please explain why you are flagging this content:</span>
                        <br />
                        <textarea name="flag" class="content_feedback"></textarea>
                        <button type="submit" class="green">Submit</button>
                    </form>
                </div><!-- flag_content -->
                <div class="reply content left">
                    <form action="">
                        <textarea name="reply" class="content_feedback"></textarea>
                        <button type="submit" class="green">Submit</button>
                    </form>
                </div><!-- reply content -->
            
                <div class="comment_reply left clr">
                    <span><img src="img/Monster_icon_25x25.jpg" /> <a href="profile.html">Monster</a> says ...</span>
                    <br />
                    <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit sed do eiusmod tempor incididunt ut laboreAliqua ut enim ad minim veniam
                    </p>
                    <br />
                    <div class="gray comment_data left">
                        <p class="time">Posted 15 minutes ago</p>
                        <p>
                            <a href="#" class="gray flag">Flag comment</a>
                            <a href="#" class="gray reply">Reply</a>
                        </p>
                        <p class="thumbs up">
                            <span class="dark-text"> 14 </span>
                            <a href="#">thumbs up</a>
                        </p><!-- thumbs up -->
                        <p class="thumbs down">
                            <span class="dark-text"> 7 </span>
                            <a href="#">thumbs down</a>
                        </p><!-- thumbs down -->
                    </div><!-- comment_data -->
                    <div class="flag content left">
                        <form action="" class="left wide">
                            <span class="dark-text">Please explain why you are flagging this content:</span>
                            <br />
                            <textarea name="flag" class="content_feedback"></textarea>
                            <button type="submit" class="green">Submit</button>
                        </form>
                    </div><!-- flag_content -->
                    <div class="reply content left">
                        <form action="">
                            <textarea name="reply" class="content_feedback"></textarea>
                            <button type="submit" class="green">Submit</button>
                        </form>
                    </div><!-- reply content -->
                </div><!-- comment_reply -->
            </li>
        </ul>
        </%doc>
    </div><!-- comments -->
 %endif

</%def>
