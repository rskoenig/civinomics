<%inherit file="/base/base_corp.mako"/>
<%def name="page_specific_css()">
    <!-- None -->
</%def>
<%def name="display_body_right_content()">
<h1>
    <b>Facilitate public discourse, generate new ideas, and collect valuable data.</b>
    <br>
</h1>
<p>
Save your planning budget and streamline development by incorporating community feedback from the get-go.  Civinomics’s platform allows you to connect with a persistent community of thoughtful, engaged citizens.  Or, build your own community.
</p>

<h7>features overview</h7>
<br /> <br />
<a href="#inform"
        onmouseover="document.inform.src='/images/inform_norm.gif'"
        onmouseout ="document.inform.src='/images/inform_hover.gif'">
  <img name='inform' src='/images/inform_hover.gif'>
</a>

<a href="#discuss"
        onmouseover="document.discuss.src='/images/discuss_norm.gif'"
        onmouseout ="document.discuss.src='/images/discuss_hover.gif'">
  <img name='discuss' src='/images/discuss_hover.gif'>
</a>

<a href="#ideate"
        onmouseover="document.ideate.src='/images/ideate_norm.gif'"
        onmouseout ="document.ideate.src='/images/ideate_hover.gif'">
  <img name='ideate' src='/images/ideate_hover.gif'>
</a>

<a href="#reward"
        onmouseover="document.reward.src='/images/reward_norm.gif'"
        onmouseout ="document.reward.src='/images/reward_hover.gif'">
  <img name='reward' src='/images/reward_hover.gif'>
</a>

<a href="#mobilize"
        onmouseover="document.mobilize.src='/images/mobilize_norm.gif'"
        onmouseout ="document.mobilize.src='/images/mobilize_hover.gif'">
  <img name='mobilize' src='/images/mobilize_hover.gif'>
</a>

</%def>

## INFORM
<%def name="display_body_bottom_content()">
<div id="body_header" class="grid_3" style="background:#e3eac9">
<h3 id = "inform"> INFORM </h3>
</div>
<div id="body_bottom_capsule" class="grid_12">
    <div id="left_content" class="grid_1">
    </div>
    <div id="right_content" class="grid_10">
        <div id="features" class="grid_9">
            <img class="features_img" src="/images/features_1.png">

            <div id="features_text">
                <br/> <br/><br/>
                <h4> Multimedia content allows people to learn about your issue and make meaningful contributions. </h4>
            
                <p>The first step to engagement is understanding.  Civinomics creates a rich educational space that includes slideshows, video, a background wiki, charts, and graphs.</p>

            </div>
        </div>
    </div>
</div>

## DISCUSS
<div id="body_header" class="grid_3" style="background:#e3eac9">
<h3 id = "discuss"> DISCUSS</h3>
</div>

<div id="body_bottom_capsule" class = "grid_12">
    <div id = "left_content" class = "grid_1">
    </div>

    <div id = "right_content" class = "grid_10">
        <div id="features" class="grid_9">
            <img class="features_img" src="/images/features_2.png">

            <div id="features_text">
                <br/><br/><br/>
                <h4> Comment ratings and 24/7 moderation ensure that discussion is constructive, relevant, and intelligent. </h4>
            
                <p>Users that establish a good reputation for themselves on the site have their comments featured more often.</p>

            </div>
        </div>
    </div>
</div>


## IDEATE
<div id="body_header" class="grid_3" style="background:#e3eac9">
<h3 id = "ideate"> IDEATE</h3>
</div>
<div id="body_bottom_capsule" class = "grid_12">
    <div id = "left_content" class = "grid_1">
    </div>

    <div id = "right_content" class = "grid_10">
        <div id="features" class="grid_9">
            <img class="features_img" src="/images/features_3.png">

            <div id="features_text">
                <br/><br/><br/>
                <h4> Solution generation and voting is a multi-step process that allows detailed plans to be compared and selected. </h4>
            
                <p>Civinomics allows you to manage the process of finding solutions from the brainstorming phase, all the way up to finalizing your plans.</p>

            </div>
        </div>
    </div>
</div>

## REWARD
<div id="body_header" class="grid_3" style="background:#e3eac9">
<h3 id = "reward"> REWARD</h3>
</div>
<div id="body_bottom_capsule" class = "grid_12">
    <div id = "left_content" class = "grid_1">
    </div>

    <div id = "right_content" class = "grid_10">
        <div id="features" class="grid_9">
            <img class="features_img" src="/images/features_4.png">

            <div id="features_text">
                <br/><br/><br/>
                <h4> Users earn points and badges as they develop a civic identity. </h4>
            
                <p>Game mechanics reward reading, making suggestions, high-ranking comments, adding news articles, and voting.</p>

            </div>
        </div>
    </div>
</div>

## MOBILIZE
<div id="body_header" class="grid_3" style="background:#e3eac9">
<h3 id = "mobilize"> MOBILIZE</h3>
</div>
<div id="body_bottom_capsule" class = "grid_12">
    <div id = "left_content" class = "grid_1">
    </div>

    <div id = "right_content" class = "grid_10">
        <div id="features" class="grid_9">
            <img class="features_img" src="/images/features_5.png">

            <div id="features_text">
                <br/><br/><br/>
                <h4> iPad-based outreach brings the suggestion box to your audience. </h4>
            
                <p>Whether polling or sharing information, our mobile app gets more people involved with your issue, spreading positive branding and building your followers.</p>

            </div>
        </div>
    </div>
</div>

</%def>
