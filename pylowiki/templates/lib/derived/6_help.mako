<%def name="helpCenter()">
    <div class="row-fluid">
            <div class="span4 well help">
                <a href="#">
                    <span class="link-span"></span><!-- used to make entire div a link -->
                    <h3><img src="images/glyphicons_pro/glyphicons/png/glyphicons_071_book.png">  Tutorial 101</h3>
                    <p>Where to begin if you are entirely new to Civinomics and just don't get it.</p>
                </a>
            </div>
             <div class="span4 well help">
                <a href="#">
                    <span class="link-span"></span><!-- used to make entire div a link -->
                    <h3><img src="images/glyphicons_pro/glyphicons/png/glyphicons_043_group.png">  How to start a workshop</h3>
                    <p>Ready to start a workshop of your own? Here are some things you'll need to keep in mind as a facilitator.</p>
                </a>
             </div>
            <div class="span4 well help"> 
                <a href="/help/faq">
                    <span class="link-span"></span><!-- used to make entire div a link -->
                    <h3><img src="images/glyphicons_pro/glyphicons/png/glyphicons_194_circle_question_mark.png">  FAQ</h3>   
                    <p>Answers to such questions as...</p>    
                    <ul>
                        <li>How do I vote?</li>
                        <li>How do I submit an idea to vote on?</li>
                        <li>What makes a good Idea?</li>
                    </ul>
                </a>
            </div>
        </div>
        <div class="row-fluid">
            <div class="span4 well help">
                <a href="#">
                    <span class="link-span"></span><!-- used to make entire div a link -->
                    <h3><img src="images/glyphicons_pro/glyphicons/png/glyphicons_360_bug.png">  Something's not working</h3>
                    <p>Can't login, missing objects, load failures, can't edit your workshop...</p>
                </a>
            </div>
            <div class="span4 well help">
                <a href="/help/reportAbuse">
                    <span class="link-span"></span><!-- used to make entire div a link -->
                    <h3><img src="images/glyphicons_pro/glyphicons/png/glyphicons_266_flag.png">  Report abuse or policy violoations</h3>
                    <p>Is someone misbehaving? Here's what you can do.</p>
                </a>
            </div>
            <div class="span4 well help">
                <a href="#">
                    <span class="link-span"></span><!-- used to make entire div a link -->
                    <h3><img src="images/glyphicons_pro/glyphicons/png/glyphicons_374_claw_hammer.png">  Suggest new features</h3>
                    <p>Help make Civinomics more effective.</p>
                </a>
            </div>
        </div><!-- row-fluid -->
</%def>

<%def name="reportAbuse()">
    % if 'alert' in session:
        <% alert = session['alert'] %> 
        <div class="alert alert-${alert['type']}">
            ## bad char: ×
            ## good char: x
            <button data-dismiss="alert" class="close">x</button>
            <strong>${alert['title']}</strong> ${alert['body']}
        </div>
        <% 
           session.pop('alert')
           session.save()
        %>
    % endif
    </br>
    <h2>Report abuse or policy violations</h2>
    </br>
    <p class="lead">Hi, we're here to help. Before you submit a report, keep in mind that most all objects on Civinomics (comments, ideas, resources, conversations) can be flagged and that this should be your first recourse for any content that you feel is inappropriate. Facilitators and Site Administrators will be notified of flagged objects and can take action as necessary.</p>
    <p>Example of flagging a comment:</p>
    <img src="/images/helpCenter/flagEx.png">
    </br>
    </br>
    <p class="lead">If you have already taken this step, or if the problem extends to your personal well being and prviate information, please fill out the fields below so we can assist you as quickly as possible.</p>
    <form name="reportAbuse" action="/help/abuseHandler" enctype="multipart/form-data" method="post">
        <fieldset>
            <legend><strong>Report an abusive user</strong></legend>
            <label><strong>Which of the following best describes the problem?</strong></label>
            <label class="radio">
                <input type="radio" name="problemType" id="problemType1" value="someone is posting my private information" checked>
                Someone on Civinomics is posting my private information.
            </label>
            <label class="radio">
                <input type="radio" name="problemType" id="problemType2" value="someone is pretending to be me">
                Someone on Civinomics is pretending to be me.
            </label>
            <label class="radio">
                <input type="radio" name="problemType" id="problemType3" value="someone is sending me abusive messages">
                Someone on Civinomics is sending me abusive messages or threats.
            </label>
            <label class="radio">
                <input type="radio" name="problemType" id="problemType4" value="other Civinomics policy violation">
                Other violoation of Civinomics <a href="/corp/terms"> policy</a>.
            </label>
            </br>
            <label><strong>Have you already flagged objects (comments, conversations, ideas or resources) authored by this user?</strong></label>
            <label class="radio">
                <input type="radio" name="alreadyFlagged" id="alreadyFlagged1" value="YES" checked>
                Yes
            </label>
            <label class="radio">
                <input type="radio" name="alreadyFlagged" id="alreadyFlagged2" value="NO">
                No
            </label>
            </br>
            <label><strong>What username is causing the problem?</strong></label>
            <input type="text" class="input-xlarge" name="offendingUser" placeholder="">
            </br>
            </br>
            <label><strong>How long ago did this begin?</strong></label>
            <label class="radio">
                <input type="radio" name="startTime" id="startTime1" value="24 hours ago" checked>
                24 hours ago
            </label>
            <label class="radio">
                <input type="radio" name="startTime" id="startTime2" value="Few days ago">
                Few days ago
            </label>
            <label class="radio">
                <input type="radio" name="startTime" id="startTime3" value="About a week ago">
                About a week ago
            </label>
            <label class="radio">
                <input type="radio" name="startTime" id="startTime4" value="About a month ago">
                About a month ago
            </label>
            <label class="radio">
                <input type="radio" name="startTime" id="startTime5" value="More than a month ago">
                More than a month ago
            </label>
            </br>
            <label><strong>Describe the problem in detail.</strong></label>
            <textarea rows="5" name="problem" class="input-xxlarge"></textarea>
            <div class="form-actions">
                <button type="submit" class="btn btn-success">Send Report</button>
                <button type="button" class="btn">Cancel</button>
            </div>
        </fieldset>
    </form>
</%def>

<%def name="faq()">
    <div id="sidebar" class="span3">
        <ul id="inner-sidebar" class="nav nav-tabs nav-stacked">
            <li><a href="#howDoI">How do I...<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#home">Homepage<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#profile">Profile<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#mgAccount">Manage Account<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#workshops">Workshops<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#configWorkshop">Configure Workshop<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#adminWorkshop">Administrate Workshop<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#conversations">Conversations<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#ideas">Ideas<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#resources">Resources<i class="icon-chevron-right pull-right"></i></a></li>
        </ul>      
    </div>
    <div class="span9">
        <h3>FAQ</h3>       
        <div class="longText">
            <div id="howDoI">
                <hr>
                <h4>How do I...</h4>
                <em>Answers to the most common questions.</em>
                </br>
                </br>
                <strong>How do I vote?</strong>
                <p>You vote on specific ideas and proposals - the homepage displays workshops, which contain the objects to vote on. To vote, click into a workshop, go to the Ideas tab and vote for an idea by clicking the up arrow or vote against an idea by clicking the down arrow.</p>
                <strong>How do I submit an idea to vote on?</strong>
                <p>To submit an idea, go to a workshop on the topic you would like to make a proposal for, click on the Ideas tab, then click on the green “Add an idea” button.</p>
                <strong>What is a workshop?</strong>
                <p>A Civinomics workshop is an online space where a group of people of any size can make decisions by suggesting ideas, voting on other people’s proposals, posting resources and discussing the issues.</p>
                <strong>How do I start a workshop of my own?</strong>
                <p>Click on Workshops on the top navigation bar; a short drop-down menu will show you the option “Create.” Click it and you’re off!</p>
                <strong>How do I edit my profile?</strong>
                <p>First, click on “Profile” on the top navigation bar. It will take you to a screen with your photo on the right hand side. Now click the orange “Edit” button found to the left of your profile picture. Click on the link to Gravatar.com, create an account and upload a photo. This will change your picture for all sites that use Gravatar, including all Wordpress sites and blogs.</p>
                <strong>How do I access my messages?</strong>
                <p>Click on “Profile” on the top navigation bar, then click on “Edit,” just to the left of your profile picture. Under the Edit Profile menu bar on the left hand side of that page, you wil see an item that says “Invitations and Notifications.” Click on it to get your messages.</p>
                <strong>How do  I invite people to my public workshop?</strong>
                <p>This functionality is coming soon.</p>
                <strong>How do I delete a slide?</strong>
                <p>Drag it to "Unpublished Slides."</p>
                <strong>How do I change my profile picture?</strong>
                <p>In the alpha release, Civinomics uses your Gravatar profile photo. Gravatar lets you set one profile picture that is used by lots of different sites, including Wordpress. To change your picture, go to your Edit Profile page and select “Update your profile info” on the Edit Profile menu. Find the item called “Image” in the main box.Here you will link to Gravatar where you can create an account and upload a picture.</p>
            </div>

            <div id="home">
                <hr>
                <h4>Homepage</h4>
                <em>The homepage lists all of the workshops on Civinomics.</em>
                </br>
                </br>
                <strong>What do the icons on the homepage mean?</strong>
                <p>Each workshop listed shows two icons: an eye, signifying the number of people who have bookmarked the workshop; and a pencil, signifying the number of actions (suggestions, comments, etc.) people have taken in the workshop.</p>
                <strong>What are the geographic regions listed at the top of the page?</strong>
                <p>The regions at the top of the page represent the “public spheres” you inhabit based on the postal code information you submitted during the signup process. You should see the name of your city, your county, your state, your country and yes, even your planet (!) across the top. Clicking on your city will show you all the Civinomics workshops that are specific to your city; clicking on your state will show you workshops that pertain to statewide issues. And clicking on Earth will show you workshops that affect us all, no matter where we live.</p>
                <strong>How can I participate in workshops outside of my area?</strong>
                <p><em>coming soon</em></p>
                <strong>How do I look for different categories of workshops?</strong>
                <p><em>coming soon</em></p>
                <strong>What kind of activity is listed in the activity stream on the homepage?</strong>
                <p>The “Activity” column, found on the far right side of the homepage, documents the most recent activity of other members on the site. Each listing shows a thumbnail of the person who made the contribution, the type of the contribution it is (idea, resource, etc.) and the title. The most recent activity appears at the top.</p>
            </div>

            <div id="profile">
                <hr>
                <h4>Profile</h4>
                <em>The profile page keeps a record of all of the objects (comments, ideas, resources, etc.) that you have authored.</em>
                </br>
                </br>
                <strong>How do I access my profile?</strong>
                <p>You can access your Profile page at any time by clicking on the word “Profile” in the top navigation bar. You can also access it by clicking on your photo thumbnail (small image) wherever you see it on the site. You can view other members’ profiles by clicking on their thumbnails as well.</p>
                <strong>What is a greeting message?</strong>
                <p>A greeting message is a short description of yourself to display to the public. It could be a job title, a few adjectives, or anything else.</p>
                <strong>Where does it list my greeting and website on my profile?</strong>
                <p>These appear under the boxed section beneath your profile photo, directly after your location and the date that you joined.</p>
                <strong>Can I bookmark private workshops?</strong>
                <p>Yes! Just click the “Bookmark” button in the top right-hand corner of the workshop.</p>
                <strong>How come it doesn’t list my activity in private workshops?</strong>
                <p>Private workshops are meant to be just that, private! In order to prevent people from linking to private workshops from your profile they are not displayed to the public. However, you can  see any activity from private workshops when viewing your profile with your own account. </p>
                <strong>Can I edit an idea I submitted?</strong>
                <p>Yes. You can do that by going to the workshop where you submitted the idea and clicking on the Ideas tab. Find the item you want to edit. Beneath your thumbnail you should see a small button marked Edit. Click it and follow the prompts. (Note: You must be logged in for this to work.)</p>
                <strong>Can I edit a conversation topic I submitted?</strong>
                <p>Yes. Go to the workshop where you submitted the topic and click on Conversations. Locate the item you want to edit and click on it. You should see, beneath your thumbnail photo, a small button marked Edit. Click it and follow the prompts. (Note: You must be logged in for this to work.)</p>
                <strong>Can I edit a resource I submitted?</strong>
                <p>Yes. Go to the workshop where you submitted the resource and click on Resources. Locate the item you want to edit and click on the word “comments” below. Beneath your thumbnail photo you should see a small button marked Edit. Click it and follow the prompts. (Note: You must be logged in for this to work.)</p>
                <strong>What does it mean to facilitate a workshop?</strong>
                <p>Workshop facilitators create workshops, establish the workshop goals, draft the initial slideshow content and background information and provide content moderation (for example disabling offensive comments or deleting illegal ones). Facilitators safeguard against Terms of Use violations. </p>
                <strong>How do I facilitate a workshop of my own?</strong>
                <p>Click on Workshops on the top navigation bar; a short drop-down menu will show you the option “Create.” Click it and you’re off! </p>
                <strong>What are followers?</strong>
                <p>Followers are other members who have elected to receive updates about your actions on Civinomics and have a direct link to your profile via their own.</p>
                <strong>How do I get followers?</strong>
                <p>There is no single way to gain followers. However, we encourage contributing a lot of really valuable and constructive content.</p>
                <strong>How do I follow other people?</strong>
                <p>To follow another member, click on that person’s name or thumbnail to access his or her profile, then click the blue button labeled “follow” in the top row on the profile page.</p>
                <strong>What is a listener?</strong>
                <p>A listener is someone who wields influence in the topic area covered by the workshop. Usually this person has been invited by the facilitator to witness what members of the public say or think about a given issue. For example, a facilitator might invite a city councilmember to be a listener on a workshop about beautifying city streets. It’s another way for a Civinomics workshop to have real-world impact.</p>
                <strong>How do I bookmark workshops?</strong>
                <p>To follow a workshop, click on the Bookmark button located in the upper right hand corner of that workshop’s home page. Doing this will automatically add the workshop to the “Activity” and “My Workshops” listings on your Profile page.</p>
                <strong>How can I access the workshops that I have bookmarked?</strong>
                <p>To access your bookmarked workshops, click to your profile in the top right section of the navigation bar. Once inside of your profile, click the “my workshops” tab next to “activity”. This will display all of the workshops you have bookmarked and those you are facilitating.</p>
                <strong>How do I access my messages?</strong>
                <p>Click on “Profile” on the top navigation bar, then click on “Edit,” just to the left of your profile picture. Under the Edit Profile menu bar on the left hand side of that page, you wil see an item that says “Invitations and Notifications.” Click on it to get your messages.</p>
                <strong>How do I edit my profile?</strong>
                <p>First, click on “Profile” on the top navigation bar. It will take you to a screen with your photo on the right hand side. Now click the orange “Edit” button found to the left of your profile picture. The next screen will show two boxes on the page. The smaller one, on the left, should say Edit Profile at the top. This is your Edit Profile menu.</p>
                <strong>How do I change my profile picture?</strong>
                <p>In the alpha release, Civinomics uses your Gravatar profile photo. Gravatar lets you set one profile picture that is used by lots of different sites, including Wordpress. To change your picture, go to your Edit Profile page and select “Update your profile info” on the Edit Profile menu. Find the item called “Image” in the main box.Here you will link to Gravatar where you can create an account and upload a picture.</p>
                <strong>How do I set or change my greeting message?</strong>
                <p>Go to your Edit Profile page and select “Update your profile info” from the Edit Profile menu. You can edit your greeting message by entering a new one into the field found four rows from the top of the main box.</p>
                <strong>How do I change my postal code?</strong>
                <p>This is not currently supported.</p>
                <strong>How do I change my password?</strong>
                <p>Go to your Edit Profile page and select “Change Your Password” from the Edit Profile menu. You’ll be prompted to enter your old password, then enter and re-enter your new password.</p>
            </div>

            <div id="mgAccount">
                <hr>
                <h4>Manage Account</h4>
                <em>The Manage Account page lets you handle payment information related to the facilitation of workshops.</em>
                </br>
                </br>
                <strong>Where do I find the manage account page?</strong>
                <p>Click the gears icon from a workshop that you are facilitating to get to the workshop configuration dashboard. At the bottom of the left-hand menu is the link for “Account Management”</p>
                <strong>How do I pay overdue invoices?</strong>
                <p><em>coming soon</em></p>
            </div>

            <div id="workshops">
                <hr>
                <h4>Workshops</h4>
                <em>Workshops are a space to develop solutions around a particular topic. The workshop page houses all of the objects (conversations, ideas, resources, and comments) for a particular topic.</em>
                </br>
                </br>
                <strong>How do I see the workshops that I have bookmarked?</strong>
                <p>All of the workshops that you are currently following can be seen on your profile page under the heading “My Workshops.”</p>
                <strong>How do I find workshops that I have created?</strong>
                <p>If the workshop you created is public, you should be able to find it on the Civinomics home page, under the geographic area you selected for that workshop or on your Profile page under “My Workshops.” If the workshop is private, you will only be able to find it on your Profile page under “My Workshops.” It will be marked to indicate that you are “Facilitating.”</p>
                <strong>What are workshop goals?</strong>
                <p>Workshop goals define what ideas and points of discussion should be the focus of member contributions. The goals articulate the purpose of the workshop.</p>
                <strong>Why are some of the workshop goals crossed off, or have a percentage next to them?</strong>
                <p>Once a goal has been addressed, the facilitator may cross it off to signify that the goal is complete. If a goal has a percentage next to it, that is how much of the goal has been addressed. For instance, if the goal is “build 10 houses” and 5 have been built, then that goal would be 50% complete.</p>
                <strong>What is the difference between a conversation and an idea?</strong>
                <p>Conversations are meant to answer questions or explore topics, whereas ideas are the first step in a more concrete proposal (i.e. they are actionable items).</p>
            </div>

            <div id="configWorkshop">
                <hr>
                <h4>Configure Workshop</h4>
                <em>The configure workshop pages help you set up a new workshop or edit basic information for one of your existing workshops.</em>
                </br>
                </br>
                <strong>What is the difference between a public and private workshop?</strong>
                <p>Public workshops can be viewed by anyone, private workshops can only be viewed by the people you invite.</p>
                <strong>What is the difference between a professional and a personal workshop?</strong>
                <p>Professional workshops can be either public (imagine a citywide initiative) or private (imagine a company soliciting input on its vacation policy). All personal workshops are private and may include a maximum of 10 participants.</p>
                <strong>When are the invites for my workshop sent out?</strong>
                <p>As soon as you hit the invite button — this may be before you actually publish the workshop. The point of this is to allow you to invite people to view your workshop before you actually publish it and make it public.</p>
                <strong>How do  I invite people to my public workshop?</strong>
                <p><em>coming soon</em></p>
                <strong>Whey does my caption keeps disappearing after I type it?</strong>
                <p>When you type a caption make sure you hit the Return or Enter key when you are done (tab and arrow keys will delete the caption, as will navigating to another page or window).</p>
                <strong> Why did I get a message saying “not valid email address” when I tried to invite friends to my personal or private workshop?</strong>
                <p>Re-enter their email addresses, one per line. (Separating them with commas won’t work.)</p>
                <strong>What are unpublished slides?</strong>
                <p>If you decide you don’t want to use a slide you’ve uploaded but think you may want to use it later, you can move it under “Unpublished Slides” and it won’t show up in your slideshow.  You can move it back to “Published Slides” at any time and it will be visible again.</p>
                <strong>How do I delete a slide?</strong>
                <p>Move it to Unpublished Slides.</p>
                <strong>How do I unpublish a workshop?</strong>
                <p><em>coming soon</em></p>
                <strong>Can I save my workshop after it ends so that others can see what happened?</strong>
                <p>Yes, your workshop will still be accessible from your profile page.</p>
                <strong>What happens to my professional workshop if I stop paying?</strong>
                <p>Your workhsop will be automatically un-published if you stop paying for it.</p>
                <strong>If I stop paying for a workshop, but later decide that I want to start it up again, will be information be lost?</strong>
                <p>No, your information will not be deleted. All workshop information is retained</p>
                <strong>Are there any cancellation fees?</strong>
                <p>There are no cancellation fees.</p>

            <div id="adminWorkshop">
                <hr>
                <h4>Administrate Workshop</h4>
                <em>Use the Administrate Workshop pages to facilitate a workshop that has already started. This could include moderating content, posting daily messages, or updating the workshop goals.</em>
                </br>
                </br>
                <strong>What is a facilitator message?</strong>
                <p>In addition to the workshop goals, the facilitator message is a comment left by the workshop facilitator to help guide how and what members should contribute.</p>
                <strong>Where can members see my facilitator message?</strong>
                <p><em>coming soon</em></p>
                <strong>What is a flagged object?</strong>
                <p>Anyone can flag any user created object, including resources, ideas, conversations, comments and more. This allows the community to self-regulate to a large extent. A flagged object that shows up in your facilitator pane is an object that another user has flagged as inappropriate or needing attention. You can choose to disable it or request that an admin delete it.</p>
                <strong>How do I flag something?</strong>
                <p>You can flag any user submitted contribution by clicking the flag button inside the contribution listing. All members can flag all suggestions, resources, discussion topics and comments. Flagging will signal a moderator to review the contribution for content relevance and terms of use violations.</p>
                <strong>What if an object has already been flagged, will flagging it again help?</strong>
                <p><em>coming soon</em></p>
                <strong>What if someone flags an object that is perfectly fine? Can I tell them why I chose to not flag something?</strong>
                <p>If someone has flagged an object that you feel should not be disabled you can “immunify” it by going to “admin” at the bottom of the object and then clicking “immunify” Remove the flag and prevent it from being flagged in the future. </p>
                <strong>Do flagged objects get deleted?</strong>
                <p>Not automatically. They are marked for review by the workshop facilitators and site admins - if the content is indeed in-appropriate it may be disabled, meaning that it is collapsed, put at the bottom of the listing page and no one is able to add additional comments to it, or deleted entirely. </p>
            </div>

            <div id="conversations">
                <hr>
                <h4>Conversations</h4>
                <em>Conversations are for answering questions and exploring topics.</em>
                </br>
                </br>
                <strong>What are conversations?</strong>
                <p>Conversations are member-initiated points of conversation, much like a forum. Discussion topics can be in the form of questions, op-eds, statements, pictures, etc. All discussion topics can be rated up and down with the arrows on the left side of the discussion heading. Discussions can also be edited by their original creators.</p>
                <strong>Can I disable comments on conversations I start?</strong>
                <p>No, it wouldn’t be much of a conversation then, would it? If someone is being inappropriate you can flag that person’s comment for the workshop facilitator or an administrator to remove.</p>
            </div> 

            <div id="ideas">
                <hr>
                <h4>Ideas</h4>
                <em>Ideas are the first step in developing a comprehensive way to meet the workshop goals.</em>
                </br>
                </br>
                <strong>Can I disable comments on my idea?</strong>
                <p>No, if we allowed people to censor replies to their own ideas or discussion topics, it would limit free speech on the site. If someone has made an inappropriate comment in reply to your idea, you can flag it.</p>
                <strong>Why can I only use 160 characters for my idea?</strong>
                <p>Ideas should be short and sweet hence the limitation. In the future, we will add more developed proposal objects that can accommodate more text and have some additional properties. </p>
                <strong>Can I use the same idea for multiple workshops?</strong>
                <p>Yes, but currently you would have to submit the idea separately to both workshops. Proposals that span multiple workshops are in development. </p>
                <strong>What happens if someone posts a similar idea to mine?</strong>
                <p>This is in-fact frequently the case - their are no new ideas and people tend to make similar observations. It is fine for multiple variations of the same idea to be posted. Ideas with better wording and authored by members with more friends are likely to get more votes. These will lead to better proposals in the long run. </p>
                <strong>Can I let some people submit ideas and not others if I am the facilitator?</strong>
                <p><em>coming soon</em></p>
            </div> 

            <div id="resources">
                <hr>
                <h4>Resources</h4>
                <em>Resouces are articles, videos, pdfs, or other items that help provide information on a workshop topic or suggest ways to meet the workshop goals.</em>
                </br>
                </br>
                <strong>How can I see a resource?</strong>
                <p>To view a resource click on the resource’s title. This will bring up the resource’s link such as an article on nytimes.com, a video on youtube.com, or the page where an organization has posted a PDF for download. To view member comments about a resource, click on the “comments” link at the bottom of the resource listing on the “Resources” page.</p>
                <strong>How can I see  the comments on a resource?</strong>
                <p>Click on the "comments" link underneath the resource title.</p>
                <strong>How do I rate a resource?</strong>
                <p>You can rate resources by clicking the up or down arrows to the left of the resource title. You can do this inside the resource’s page, where comments are listed, or from the “Resources” page where all the resources for a workshop are listed. The numerical display in between the arrows shows the total number of up votes minus down votes for that resource.</p>
                <strong>What are the rules about posting copyrighted materials to the resources section?</strong>
                <p>Because these materials are not being hosted directly on the Civinomics.com site, there are no copyright infringement issues.</p>
            </div> 
        </div><!-- longText -->
    </div><!-- span9 -->
</%def>
