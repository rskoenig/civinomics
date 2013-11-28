<%def name="helpCenter()">
    <ul class="thumbnails">
        <li class="span4 well help">
            <a href="${c.tutorialURL}">
                <span class="link-span"></span><!-- used to make entire div a link -->
                <h3><i class="icon-book"></i> Tutorial 101</h3>
                <p>Takes you through a guided tour of the workshop layout. A good place to begin if you are entirely new to Civinomics.</p>
            </a>
        </li>
         <li class="span4 well help">
            <a href="/help/facilitatorGuide">
                <span class="link-span"></span><!-- used to make entire div a link -->
                <h3><i class="icon-gear"></i>  How to start a workshop</h3>
                <p>Ready to start a workshop of your own? Here are some things you'll need to keep in mind as a facilitator.</p>
            </a>
         </li>
        <li class="span4 well help"> 
            <a href="/help/faq">
                <span class="link-span"></span><!-- used to make entire div a link -->
                <h3><i class="icon-question-sign"></i>  FAQ</h3>   
                <p>Answers to such questions as...</p>    
                <ul>
                    <li>How do I vote?</li>
                    <li>How do I submit an idea to vote on?</li>
                    <li>What makes a good Idea?</li>
                </ul>
            </a>
        </li>
        <li class="span4 well help">
            <a id="helpCenter_bugReporter">
                <span class="link-span"></span><!-- used to make entire div a link -->
                <h3><i class="icon-bug"></i>  Something's not working</h3>
                <p>Can't login, missing objects, load failures, can't edit your workshop...</p>
            </a>
        </li>
        <li class="span4 well help">
            <a href="/help/reportAbuse">
                <span class="link-span"></span><!-- used to make entire div a link -->
                <h3><i class="icon-flag"></i>  Report abuse or policy violations</h3>
                <p>Is someone misbehaving? Here's what you can do.</p>
            </a>
        </li>
        <li class="span4 well help">
            <a href="/help/feedbackWorkshop">
                <span class="link-span"></span><!-- used to make entire div a link -->
                <h3><i class="icon-lightbulb"></i>  Suggest new features</h3>
                <p>Yup, we're in beta. So help us get the Civinomics engine purring.</p>
            </a>
        </li>
        <li class="span4 well help">
            <a href="#" onclick="window.open('/help/markdown.html','popUpWindow','height=500,width=500,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');">
                <span class="link-span"></span>
                <h3><i class="icon-picture"></i> <i class="icon-list"></i>  Formatting Guide</h3>
                <p>Civinomics uses markdown for most text throughout the site. This quick guide will show you the syntax for bold, italic, links and adding pictures to text fields.</p>
            </a>
        </li>
    </ul><!-- thumbnails -->
</%def>

<%def name="reportAbuse()">
    <div class="span10">
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
        <h2>Report abuse or policy violations</h2>
        </br>
        <p class="lead">Hi, we're here to help.</p>
        <p>Before you submit a report of abusive behavior, keep in mind that most all objects on Civinomics (comments, ideas, resources, conversations) can be flagged and that this should be your first recourse for any content that you feel is inappropriate. Facilitators and Site Administrators will be notified of flagged objects and can take action as necessary.</p>
        </br>
        <div class="offset1"
            <p><strong>Example of flagging a comment:</strong></p>
            <img src="/images/helpCenter/flagEx.png">
        </div>
        </br>
        </br>
        <p>If you have already taken this step, or if the problem extends to your personal well being and prviate information, please fill out the fields below so we can assist you as quickly as possible.</p>
        </br>
        <form name="reportAbuse" id="reportAbuse" action="/help/abuseHandler" enctype="multipart/form-data" method="post" ng-controller="helpForm" ng-submit="submitForm()">
            <fieldset>
                <legend><strong>File an abuse report</strong></legend>
                <label><strong>Which of the following best describes the problem?</strong></label>
                <label class="radio">
                    <input type="radio" name="problemType" id="problemType1" value="someone is posting my private information" ng-model="problemType" required>
                    Someone on Civinomics is posting my private information.
                </label>
                <label class="radio">
                    <input type="radio" name="problemType" id="problemType2" value="someone is pretending to be me" ng-model="problemType" required>
                    Someone on Civinomics is pretending to be me.
                </label>
                <label class="radio">
                    <input type="radio" name="problemType" id="problemType3" value="someone is sending me abusive messages" ng-model="problemType" required>
                    Someone on Civinomics is sending me abusive messages or threats.
                </label>
                <label class="radio">
                    <input type="radio" name="problemType" id="problemType4" value="other Civinomics policy violation" ng-model="problemType" required>
                    Other violation of Civinomics <a href="/corp/terms"> policy</a>.
                </label>
                </br>
                <label><strong>Have you already flagged objects (comments, conversations, ideas or resources) authored by this user?</strong></label>
                <label class="radio">
                    <input type="radio" name="alreadyFlagged" id="alreadyFlagged1" value="YES" ng-model="alreadyFlagged" required>
                    Yes
                </label>
                <label class="radio">
                    <input type="radio" name="alreadyFlagged" id="alreadyFlagged2" value="NO" ng-model="alreadyFlagged" required>
                    No
                </label>
                </br>
                <label><strong>What username is causing the problem?</strong></label>
                <div class="form-inline">
                    <input type="text" class="input-xlarge" name="offendingUser" ng-model="offendingUser" placeholder="" required>
                    <span class="label label-important" ng-show="offendingUser == ''">Required</span>
                </div>
                </br>
                <label><strong>How long ago did this begin?</strong></label>
                <label class="radio">
                    <input type="radio" name="startTime" id="startTime1" value="24 hours ago" ng-model="startTime" required>
                    24 hours ago
                </label>
                <label class="radio">
                    <input type="radio" name="startTime" id="startTime2" value="Few days ago" ng-model="startTime" required>
                    Few days ago
                </label>
                <label class="radio">
                    <input type="radio" name="startTime" id="startTime3" value="About a week ago" ng-model="startTime" required>
                    About a week ago
                </label>
                <label class="radio">
                    <input type="radio" name="startTime" id="startTime4" value="About a month ago" ng-model="startTime" required>
                    About a month ago
                </label>
                <label class="radio">
                    <input type="radio" name="startTime" id="startTime5" value="More than a month ago" ng-model="startTime" required>
                    More than a month ago
                </label>
                </br>
                <label><strong>Describe the problem in detail.</strong></label>
                <textarea rows="5" name="problem" class="input-xxlarge" ng-model="problemDescription" required></textarea>
                <span class="label label-important" ng-show="problemDescription == ''">Required</span>
                <label><strong>Your name:</strong></label>
                <div class="form-inline">
                    <input type="text" class="input-xlarge" name="reporterName" id="reporterName" ng-model="reporterName" required>
                    <span class="label label-important" ng-show="reporterName == ''">Required</span>
                </div>
                </br>
                <label><strong>What is the best email to reach you at?</strong></label>
                <div class="form-inline">
                    <input type="email" class="input-xlarge" name="reporterEmail" id="reporterEmail" ng-model="reporterEmail" required>
                    <span class="label label-important" ng-show="reporterEmail == ''">Required</span>
                </div>
                <span class="error help-block" ng-show="reportAbuse.reporterEmail.$error.email">Not a valid email!</span>


                </br>
                <div class="form-actions">
                    <button class="btn btn-success disabled" ng-show="reportAbuse.$invalid">Send Report</button>
                    <button type="submit" class="btn btn-success" ng-show="reportAbuse.$valid">Send Report</button>
                    <button type="button" onclick="formReset()" value="Reset form" class="btn">Cancel</button>
                </div>
            </fieldset>
        </form>
    </div>
</%def>

<%def name="facilitatorGuide()">
    <div class="span10">
        <h2>How to Start A Workshop</h2>   
        <div class="longText">
            <p class="lead">A few tips to help you change the world.</p>
            <p>Civinomics allows anyone to create a workshop on something that could be improved. It may be improving public safety in your city, creating a better work environment in the office, or just having the best family vacation ever. However, the success of your workshop is up to you. To that end, here are a few tips to help you make it work.</p> 
            <hr>
            <ol>
                <li>
                    <strong id="title">Use a detailed and descriptive title.</strong>
                    <p>Which of these workshops sounds more likely to be successful: "Saving Marriage" or "Reforming Civil Marriage Law in the US"? The second one sets a much clearer purpose simply in its title. Aim for a title that is descriptive rather than snappy or catchy in your own workshops.</p>
                </li>
                <li>
                    <strong id="goals">Break down the challenge in the goals.</strong>
                    <p>Let’s say your workshop is about improving your local school. What are some general metrics that everyone can agree would demonstrate improvement? "Raise test scores to a B average schoolwide,” "Provide after-school activities for all students" or "Reduce campus crime rates below 10 a year" are examples of goals that you can track through observable metrics. This is generally better than intangible goals such as "Create a healthy and safe school atmosphere." Of course, topics that require an empathetic answer like this are good too, but they are better placed in the "Talk" section than listed as goals because their answer is subjective, whereas the former can be measured.</p>
                </li>
                <li>
                    <strong id="scope">When a workshop should be private...</strong>
                    <ul>
                        <li>Do you want people you don't know to participate in your workshop?</li>
                        <li>Do you want people with opposing political views to participate in your workshop?</li>
                        <li>Do you want people who aren't aren't credentialed to participate in your workshop?</li>
                        <li>Do you want your workshop to be able to claim it shows outcomes that are representative of public opinion?</li>
                        <li>Do you want people with tenuous or uncertain ties to your organization participating in your workshop?</li>
                    </ul>
                    <p>If the answer to one or more of these questions is yes, then you should start a public workshop instead of a private one.</p>
                </li>
                <li>
                    <strong id="slideshow">The logos and pathos of the slideshow</strong>
                    <p>A picture is worth a thousand words. Use the slideshow to communicate why your workshop is important. Find pictures that encapsulate the key problems. Remember how your teacher taught you to use logos (logic), pathos (sympathy) and ethos (credibility) to prove your point? This is a great opportunity to use logos in key graphs and figures or pathos in striking images that show why things must be improved.</p>
                </li>
                <li>
                    <strong id="captions">Use slide captions to impart key facts.</strong>
                    <p>There's a reason they call it surfing the internet. People cruise along looking for tantalizing bytes of information. Not everyone is going to read through your eloquent background information (just as not everyone is going to read this Help section). Use slide captions to convey the key bullet points for your workshop and you'll reach a greater range of participants.</p>
                </li>
                <li>
                    <strong id="information">Treat the information section as a work in progress.</strong>
                    <p>In Civinomics beta release, only facilitators can edit the information section. Future releases may provide the option for any workshop participant to edit this information, much as Wikipedia allows anyone to contribute to an article. For now, it's you and your fellow facilitators’ responsibility. But that doesn't mean you have to write a masterpiece the first time. The essence of your workshop will be in the participation. You can improve the background information as time goes on and important or critical pieces of information are identified. You may even promote some participants to co-facilitators so they can help you with this process. Even if your background information isn't perfect, publish anyway. You can always come back.</p>
                </li>
                <li>
                    <strong id="objects">Vote, Talk, Learn—you got thoughts, so share them!</strong>
                    <p>One of the most important elements in getting any workshop rolling is populating the dance floor. Let’s face it, you started this workshop because you're passionate about the topic. What do you think should be voted on? What key facts do you want to share? What conversations do you want to have? Add them! Your passion will help make the workshop a success. As a facilitator you do need to remember that it's your job to find solutions, even if they aren't your own. So make sure all ideas are evaluated equally and discourse remains civil. Just remember, you’re not excluded from participating in your workshop.</p>
                </li>
            </ol>
        </div><!-- longText -->
    </div>
</%def>

<%def name="faq()">
    <div id="sidebar" class="span3">
        <ul id="inner-sidebar" class="nav nav-tabs nav-stacked">
            <li><a href="#basics">The Basics<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#howDoI">How do I...<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#mgProfile">Managing Your Profile<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#moreWorkshops">More on Workshops<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#createWorkshops">Creating Workshops<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#adminWorkshops">Administrating Workshops<i class="icon-chevron-right pull-right"></i></a></li>
            <li><a href="#mgAccount">Managing Your Account<i class="icon-chevron-right pull-right"></i></a></li>
        </ul>      
    </div>
    <div class="span8">
        <h2>FAQ</h2>       
        <div class="longText">
            <div id="basics">
                <hr>
                <h3>The Basics</h3>
                <em>Definitions and other fundamentals.</em>
                </br>
                </br>
                <strong>What’s a workshop?</strong>
                <p>A Civinomics workshop is an online forum where people can exchange information about community issues, suggest solutions to problems and vote on the best ideas.</p>
                <strong>So it’s not a meeting, with people gathered in a room?</strong>
                <p>That’s right. It’s a virtual meeting rather than a face-to-face meeting. One key difference is that a Civinomics workshop can last as long as the facilitator wants it to—from a few days to a few months. Or it can run continuously, as a way for an organization to gather feedback.</p>
                <strong>What’s a facilitator?</strong>
                <p>The facilitator is the person who creates and manages the workshop. The facilitator gathers background information, assembles the informational slideshow, sets the goals and monitors the workshop to make sure comments and ideas remain civil and productive. A workshop can have a single facilitator or several co-facilitators.</p><p>Facilitators are listed in the “Notables” box.</p>
                <strong>What are the place names at the top of the page?</strong>
                <p>They’re “breadcrumbs,” and they were generated when you entered your postal code during signup. They represent the public spheres you inhabit. You should see the name of your city, your county, your state, your country and yes, even your planet (!) across the top. Clicking on your city will show you all the Civinomics workshops that are specific to your city; clicking on your state will show you workshops that pertain to statewide issues. Clicking on Earth will show you workshops that affect us all, no matter where we live.</p>
                <p>Conversely, when you’re in a workshop, only one breadcrumb will be highlighted: that’s the jurisdiction to which the workshop has been scoped. </p>
                <strong>What’s a listener?</strong>
                <p>A listener is a person who wields influence in the topic area covered by a workshop; he or she is invited by the facilitator. For example, a facilitator might invite a city councilmember to be a listener on a workshop about beautifying city streets. The listener’s role is not to moderate but to observe, and of course participate if s/he wishes. It’s another way for a Civinomics workshop to have real-world impact. </p><p>You can find listeners in the Notables box.</p>
                <strong>Can I be anonymous or use a pseudonym?</strong>
                <p>No. It’s in the Terms of Use that all users identify themselves truthfully. Civinomics supports anonymous speech in the appropriate context, but not on this site.</p>
                <strong>Will everyone be able to see my comments and ideas?</strong>
                <p>If you are commenting on a public workshop—one any visitor to Civinomics can see—then yes, everything you contribute will be visible to all users.</p>
                <strong>Will everyone be able to see how I voted?</strong>
                <p>No. Your votes are always confidential. However, if you try to vote twice on an item it won’t work. </p>
                <strong>Is it free?</strong>
                <p>Yes. Civinomics is free. Voting, commenting and adding resources—all free. Even creating a workshop is free, be it public or private.</p>
                <p>When you create a public workshop you are able to set the geographic scope of that workshop, in order to specify the area it applies to. A private workshop will only be visible to you and anyone you invite to participate in it.</p>
                <strong>Can anyone join?</strong>
                <p>Yes! The more the merrier, and the better for the civic process.</p>
            </div>
            <div id="howDoI">
                <hr>
                <h3>How do I...</h3>
                <em>Answers to the most common questions. </em>
                </br>
                </br>
                <strong>How do I find a workshop?</strong>
                <p>In one of two ways: 1) use the search tool in the top navigation bar; or 2) click on the green Civinomics icon in the top navigation bar, then choose the appropriate geographic breadcrumb from the place names at the top. (For example, click on your city name to find a workshop about keeping city parks clean.) Once the page refreshes, you should be able to locate your workshop. (Note: This process only works for public workshops.)</p>
                <strong>I was invited to a private workshop, but I can’t find it on the site. What do I do?</strong>
                <p>Go back to the email inviting you to the workshop and click on the link. It will take you to the private workshop. Click “Follow” in the upper right hand corner. (If you are not already a Civinomics member, you’ll need to sign up to do this; if you are a Civinomics member, you’ll need to log in.) </p>
                <p>From this point on your private workshop will be listed under the “My Workshops” tab on your Profile page.</p>
                <strong>How do I vote on an idea?</strong>
                <p>Once you’re in the workshop you want, click on the “Vote” tab under the workshop name. You’ll see a list of ideas and, to the left of each one, a numeral with chevrons above and below it. Click the top chevron to vote for that idea; click the bottom chevron to vote against it. The numeral will change to register your vote (it shows the total number of up votes minus down votes).</p>
                <strong>How do I submit an idea to vote on?</strong>
                <p>Click on the “Vote” tab, then click on the green “Add an idea” button. When you’ve finished adding your idea, click “Submit.” Your idea should appear immediately.</p>
                <strong>What else can I vote on?</strong>
                <p>You can vote for or against all comments, conversation topics (listed under the “Talk” tab) and resources (listed under the “Learn” tab).</p>
                <strong>How can I upload a photo, Word doc or PDF as a Resource?</strong>
                <p>Currently Civinomics only supports resources that originate on the web. All resources must have URLs.</p>
                <strong>I just signed up and I keep seeing this funny-looking graphic. What is it and how do I get rid of it?</strong>
                <p>In the beta release, Civinomics uses your Gravatar profile photo. Gravatar lets you set one profile picture that is used by lots of different sites. If you don’t have a Gravatar account, you’ll be assigned a default graphic. That’s what you’re seeing.</p>
                <p>To change it to your photo, or to update your photo, click on “profile” on the top toolbar, then click on the orange “Edit Profile” link. Select “Update your profile info” on the Edit Profile menu. Find the item called “Image” in the main box.Here you will link to Gravatar, where you can create an account and upload a picture.</p>
                <strong>How can I participate in workshops outside of my area?</strong>
                <p>Just search for a workshop in the search field on the top navigation bar.</p>
                <strong>How do I search for different categories of workshop?</strong>
                <p>Browsing workshop tags will be added soon.</p>
                <strong>How do I start a workshop of my own?</strong>
                <p>Click on “workshops” on the top navigation bar; a short drop-down menu will show you the option “create.” Click it and you’re off!  The Help page includes a How to Start A Workshop section you may find helpful.</p>
            </div>

            <div id="mgProfile">
                <hr>
                <h3>Manage Your Profile</h3>
                <em>The profile page contains information about you and keeps a record of all of the objects (comments, ideas, resources, etc.) you have authored. It is also where you keep track of the workshops and people that interest you.</em>
                </br>
                </br>
                <strong>How do I access my Profile page?</strong>
                <p>Click on the word “profile” in the top navigation bar. You can also access it by clicking on your photo thumbnail (the small image) wherever you see it on the site. You can view other members’ profiles by clicking on their thumbnails as well. Your Profile page shows your photo and your Civinomics stats on the right hand side of the page.</p>
                <strong>How do I edit my profile?</strong>
                <p>Go to your Profile page and click the orange “Edit Profile” link found to the left of your profile picture.</p>
                <strong>How do I change my password?</strong>
                <p>Go to your Edit Profile page and select “Change Your Password” from the Edit Profile menu. You’ll be prompted to enter your old password, then enter and re-enter your new password.</p>
                <strong>How do I change my postal code?</strong>
                <p>This is not currently supported.</p>
                <strong>What is a greeting message?</strong>
                <p>A greeting message is a short description of yourself to display to the public. It could be a job title, a few adjectives, or anything else you want it to be.</p>
                <strong>Where does it list my greeting and website on my profile?</strong>
                <p>These appear under the boxed section beneath your profile photo, directly after your location and the date you joined.</p>
                <strong>I see the word “Followers” on my Profile page. What’s that about?</strong>
                <p>Followers are other members who have elected to receive updates about your actions on Civinomics and have a direct link to your profile via their own.</p>
                <strong>How do I get followers?</strong>
                <p>There is no single way to gain followers. However, we encourage contributing a lot of really valuable and constructive content.</p>
                <strong>How do I follow other people?</strong>
                <p>Find someone you want to follow, click on that person’s name or thumbnail to access his or her profile, then click the button labeled “Follow” in the top row on the profile page.</p>
                <strong>How do I find a particular person?</strong>
                <p>Use the search tool in the top navigation bar to enter that person’s name. When the results come up, be sure to click on the “People” bracket.</p>
                <strong>How do I access my messages?</strong>
                <p>Go to your Profile page, then click on “Messages,” just to the left of the “Edit Profile” link.</p>
                <strong>Why do I need to check my messages?</strong>
                <p>Your messages may include invitations to be a workshop co-facilitator or listener. They may also include invitations to private workshops.</p>
                <strong>Can I follow private workshops?</strong>
                <p>Yes! Just click the “Bookmark” button in the top right hand corner of the workshop. The workshop will show up under the “My Workshops” tab on your Profile page.</p>
                <strong>Will people be able to see that I am in private workshops?</strong>
                <p>No. The private workshops listed under your “My Workshops” tab will be visible to you alone. Other people coming to your profile page won’t be able to see them. Nor will they be able to see your contributions to private workshops on the “Activity” tab of your Profile page.</p>
            </div>

            <div id="moreWorkshops">
                <hr>
                <h3>More on Workshops</h3>
                <em>Workshops are a space to develop solutions around a particular topic. The workshop page houses all of the objects (conversations, ideas, resources, and comments) for a particular topic.</em>
                </br>
                </br>
                <strong>What are workshop goals?</strong>

                <p>Workshop goals define what ideas and points of discussion should be the focus of member contributions. The goals articulate the purpose of the workshop.</p>

                <strong>Why are some of the workshop goals crossed off, or have a percentage next to them?</strong>

                <p>Once a goal has been addressed, the facilitator may cross it off to signify that the goal is complete. If a goal has a percentage next to it, that is how much of the goal has been addressed. For instance, if the goal is “build 10 houses” and five have been built, then that goal would be 50 percent complete.</p>

                <strong>What is the difference between a conversation and an idea?</strong>

                <p>Conversations are meant to answer questions or explore topics, whereas ideas are the first step in a more concrete proposal (i.e., they are actionable items).</p>

                <strong>Why can I only use 160 characters for my idea?</strong>

                <p>Ideas should be short and sweet; hence the limitation. In the future, we will add more developed proposal objects that can accommodate more text and have some additional properties.</p>

                <strong>What happens if someone posts a similar idea to mine?</strong>

                <p>It is fine for multiple variations of the same idea to be posted. Ideas with better wording and authored by members with more friends are likely to get more votes. These will lead to better proposals in the long run.</p>

                <strong>Can I use the same idea for multiple workshops?</strong>

                <p>Yes, but currently you would have to submit the idea separately to both workshops. Proposals that span multiple workshops are in development.</p>

                <strong>Can I edit an idea I submitted?</strong>

                <p>Yes. Go to the workshop where you submitted the idea, click on “Vote” and find the item in question. Beneath your thumbnail image, you should see a small button marked Edit. Click it and follow the prompts. (Note: You must be logged in for this to work.)</p>

                <strong>Can I edit a conversation topic I submitted?</strong>

                <p>Yes. The process is the same as for editing an idea.</p>

                <strong>How about editing a resource I submitted?</strong>

                <p>Go to the workshop where you submitted the resource and click on “Learn.” Locate the item you want to edit and click on the word “comments” below. Beneath your thumbnail photo you should see a small button marked Edit. Click it and follow the prompts. (Note: You must be logged in for this to work.)</p>

                <strong>What is a resource?</strong>

                <p>Resources are articles, videos or other items that help provide information on a workshop topic or suggest ways to meet the workshop goals. At present, all Resources must have URLs. Resources are listed under “Learn” in the navigation bar above the workshop name.</p>

                <strong>What are the rules about posting copyrighted materials to the resources section?</strong>

                <p>Because these materials are not being hosted directly on the Civinomics.com site, there are no copyright infringement issues.</p>

                <strong>What do the workshop icons on the homepage mean?</strong>

                <p>Each workshop listed on the homepage shows two icons: a person, signifying the number of people who have bookmarked the workshop; and a pencil, signifying the number of actions (suggestions, comments, etc.) people have taken in the workshop.</p>

                <strong>How do I follow workshops?</strong>

                <p>Click on the “Bookmark” button located in the upper right hand corner of a given workshop’s home page. Doing this will automatically add the workshop to the “Activity” and “My Workshops” listings on your Profile page.</p>

                <strong>How can I access the workshops that I have bookmarked?</strong>

                <p>Go to your Profile page and click the “My Workshops” tab next to “Activity.” This will display all the workshops you are following and those you are facilitating.</p>

                <strong>What is listed in the activity stream on the homepage?</strong>

                <p>The “Activity” column, found on the far right side of the homepage, documents the most recent activity of other members on the site. Each listing shows a thumbnail of the person who made the contribution, the type of contribution (idea, resource, etc.) and the title. The most recent activity appears at the top.</p>

                <strong>How come the activity stream doesn’t list my activity in private workshops?</strong>

                <p>Private workshops are meant to be just that: private! So those comments won’t show up in the public activity stream.</p>

                <strong>How do I flag something as inappropriate?</strong>

                <p>You can flag any user-submitted contribution by clicking the flag button inside the contribution listing. All members can flag all suggestions, resources, discussion topics and comments. Flagging will signal a moderator to review the contribution for content relevance and terms of use violations.</p>

                <strong>What if an object has already been flagged? Will flagging it again help?</strong>
                <p><em>coming soon</em></p>

            </div>

            <div id="createWorkshops">
                <hr>
                <h3>Creating Workshops</h3>
                <em>Improve something important to you.</em>
                </br>
                </br>
                <strong>What is the difference between a public and private workshop?</strong>

                <p>Public workshops can be viewed by anyone. Private workshops can only be viewed by the people you invite.</p>

                <strong>What is the difference between a professional and a personal workshop?</strong>

                <p>Professional workshops can be either public (imagine a citywide initiative) or private (imagine a company soliciting input on its vacation policy). All personal workshops are automatically private and can have a maximum of 20 participants.</p>

                <strong>When are the invites for my private workshop sent out?</strong>

                <p>As soon as you hit the invite button — this may be before you actually publish the workshop. The point of this is to allow you to invite people to view your workshop before you actually publish it and make it public.</p>

                <strong>Why did I get a message saying “not valid email address” when I tried to invite friends to my personal or private workshop?</strong>

                <p>Re-enter their email addresses, one per line. (Separating them with commas won’t work.)</p>

                <strong>How do I invite people to my public workshop?</strong>

                <p>This functionality is coming soon.</p>

                <strong>What is a facilitator message?</strong>

                <p>In addition to the workshop goals, the facilitator message is a comment left by the workshop facilitator to help guide how and what members should contribute.</p>

                <strong>Where can members see my facilitator message?</strong>

                <p><em>coming soon</em></p>

                <strong>How do I invite someone to be a co-facilitator or a listener?</strong>

               <p>Go to the person’s Profile page and click on “My Workshops.” The invitation buttons are at the top. Currently Civinomics only supports facilitation or listening invitations for members, so if the person is not yet a Civinomics member, ask him or her to become one.</p>

                <strong>How do I upload multiple images at once?</strong>

                <p>When you’re asked to add images, highlight the images you want from your hard drive or cloud file. Then click the blue Start button on top. (Note: Don’t use the blue Start button to the far right of the individual photos to upload multiple images.)</p>

                <strong>Why does my caption keeps disappearing after I type it?</strong>

                <p>When you type a caption, make sure you hit the Return or Enter key when you are done, or use the OK button (tab and arrow keys will delete the caption, as will navigating to another page or window).</p>

                <strong>How do I delete a slide?</strong>

                <p>Drag it to "Unpublished Slides."</p>

                <strong>What is “Unpublished Slides”?</strong>

                <p>It’s Purgatory for images you have uploaded. You can pull them back into the slideshow at any time, or you can just leave them there. Images in “Unpublished Slides” don’t show.</p>

                <strong>How do I find workshops I have created?</strong>

                <p>Two ways: If the workshop you created is public, you should be able to find it on the Civinomics homepage under the geographic area you selected for that workshop. It will also be on your Profile page under “My Workshops.”</p>

                <p>If the workshop is private, you will only be able to find it on your Profile page under “My Workshops.” It will be marked to indicate that you are “Facilitating.”</p>

                <strong>Can I save my workshop after it ends so that others can see what happened?</strong>

                <p>Yes, your workshop will still be accessible from your Profile page.</p>

                <strong>What happens to my professional workshop if I stop paying?</strong>

                <p>Your workshop will be automatically unpublished if you stop paying for it.</p>

                <strong>If I stop paying for a workshop, but later decide that I want to start it up again, will the information be lost?</strong>

                <p>No, your information will not be deleted. All workshop information is retained.</p>

                <strong>Are there any cancellation fees?</strong>

                <p>There are no cancellation fees.</p>

                <strong>Is there a guide to creating a workshop?</strong>
                <p>Yes! Go to the Help page and click on How to Start A Workshop.</p>

            </div>

            <div id="adminWorkshops">
                <hr>
                <h3>Administrating Workshops</h3>
                <em>Use the Administrate/Configure menus to manage a workshop that has already started. This could include moderating content, posting daily messages, or updating the workshop goals.</em>
                </br>
                </br>
               <strong>How do I get to the Administrate and Configure menus?</strong>

                <p>Any workshop for which you are a facilitator will have a green “Admin” button in the top right hand corner. Click it to get to the Administrate and Configure panels.</p>

                <strong>What is a flagged object?</strong>

                <p>Anyone can flag any user-created object, including resources, ideas, conversations, comments and more. This allows the community to self-regulate to a large extent. A flagged object that shows up in your facilitator pane is an object that another user has flagged as inappropriate or needing attention.</p>

                <strong>Do flagged objects get deleted?</strong>

                <p>Not automatically. They are marked for review by the workshop facilitators and site admins. If the content is indeed inappropriate, it may be disabled—meaning that it is collapsed and no one is able to add additional comments to it—or deleted entirely.</p>

                <strong>Can I, as facilitator, disable an item?</strong>

                <p>Yes. In the Manage Workshop window, under each item that has been flagged, there is a “Disable” button.</p>

                <strong>Can I, as facilitator, delete an item?</strong>

                <p>No. Only a Civinomics admin can delete an item.</p>

                <strong>How do I reach a Civinomics admin to request a deletion?</strong>

                <p>Go to the Help Center and file an abuse report.</p>

                <strong>How will I know if an item has been flagged?</strong>

                <p>Facilitators automatically receive email updates every time an item is flagged and every time someone contributes to one of your workshops. You can disable these, or elect to receive a simple daily digest of activity, under the “My Workshops” tab of your Profile page.</p>

                <strong>What if someone flags an object that is perfectly fine? Can I tell them why I chose not to disable something?</strong>

                <p>If someone has flagged an object that you feel should not be disabled, you can “immunify” it by going to “admin” at the bottom of the object and then clicking “immunify.” This will remove the flag and prevent it from being flagged in the future.</p>

                <strong>How do I unpublish a workshop?</strong>
                <p>At the top of the Manage Workshop window (on the Administrate menu) is an orange Unpublish Workshop button.</p>
            </div> 
            <div id="mgAccount">
                <hr>
                <h3>Managing Your Account</h3>
                <em>The Manage Account page lets you handle payment information related to the facilitation of workshops. </em>
                </br>
                </br>
                <strong>Where do I find the Manage Account page?</strong>

                <p>Click the “Admin” button from a workshop you are facilitating to get to the workshop administration dashboard. At the bottom of the left hand menu is the link for “Account Management.”</p>

                <strong>How do I pay overdue invoices?</strong>
                <p><em>coming soon</em></p>

            </div>
        </div><!-- longText -->
    </div><!-- span9 -->
</%def>

<%def name="markdownGuide()">
    <div class="span12">
        <textarea rows="10" id="data" name="data" class="span12">${c.guide}</textarea>
        <div class="preview-information-wrapper" id="live_preview">
           hi
        </div>
    </div>

</%def>



