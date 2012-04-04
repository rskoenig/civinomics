# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
  <head>
  <meta charset="UTF-8"/>
  <title>
    Greenocracy | 
    ${c.title.capitalize()}
  </title>
  <!-- This resets the browser defauls and formats print screen -->
  <link href="/styles/format.css" rel="stylesheet" type="text/css" media="screen" />
  <!-- 960 CSS -->
  <link href="/styles/960.css" rel="stylesheet" type="text/css" media="screen" />
  <!-- Font -->
  <link href='http://fonts.googleapis.com/css?family=Questrial' rel='stylesheet' type='text/css'>
  <!-- common css -->
  <link href="/styles/common.css" rel="stylesheet" type="text/css" media="screen" />
  <!-- page specific css -->
      ${self.page_specific_css()}
  </head>
  <body>
  ${self.header()}
  <div id="body_container" class="container_12">
  <div id="body_wrapper">
    <div id="body_header" class="grid_3">
        <h3>
            ${body_header}
        </h3>
    </div>
    <div id="body_top_half">
        <div id="left_navigbar" class="grid_2">
            ${self.display_navigbarfn()}
        </div>
        <div id="right_content" class="grid_9">
            ${self.display_body_right_content()}
        </div>
    </div>
    <div id="body_bottom_half" class="grid_12">
            ${self.display_body_bottom_content()}
    </div>
  </div>
  </div>
  ${self.footer()}
  </body>
</html>

<%def name="header()">
<div id ="header_wrapper">
  <div id="header_container" class="container_12">
     <div id="login_form" class="grid_6">
     % if c.user==None :
          ${self.login_form()}
     % else :
          #${self.greet_user()}
     % endif
     </div>
  </div>
</div>
</%def>
<!-- Login Form -->
<%def name="login_form()">
<form id="sign_in" method="post" action="/login">
<div class="grid_2">
<label class="form_label"> Email: </label>
<input type="text" id="email" name="email" class="form_input">
<input type="checkbox" class="form_check" name="remember_me_checkbox">
<label class="form_label" style="width:60%;margin-left:5px;margin-top:4px"> Remember me </label>
</div>
<div class="grid_2">
<label class="form_label"> Password: </label>
<input type="password" id="password" name="password" class="form_input">
<a href="/login/forgot" class="forgot_password">Forgot your password?</a>
</div>
<input type="submit" value="Login" name="login" class="formsubmit">
</form>
</%def>
<!-- Greet user -->
<%def name="greet_user()">
<h3> Welcome
</h3>
</%def>
<%def name="footer()">
<div id ="footer_wrapper">
  <div id="footer_container" class="container_12">
      <div id="footer_block" class="grid_4">
          <div id = "footer_block_header">
          <h3> 
                GREENOCRACY
          </h3>
          </div>
          <div id  = "footer_block_content" class="grid_1">
          <a href="/corp/about"> About </a>
          <a href="/corp/careers"> Careers </a>
          <a href="/corp/blog"> Blog </a>
          </div>
          <div id  = "footer_block_content" class="grid_1">
          <a href="/corp/features"> Features </a>
          <a href="/corp/services"> Services </a>
          </div>
          <div id  = "footer_block_content" style="padding-left:10px;" class="grid_2">
          <a href="/corp/terms" style="width:80%; margin-left:10px";> Terms of Use </a>
          <a href="/corp/privacy" style="width:80%; margin-left:10px";> Privacy Policy</a>
          </div>
      </div>
      <div id="footer_block" class="grid_2">
          <div id = "footer_block_header">
          <h3> 
                FOLLOW
          </h3>
          </div>
          <div id  = "footer_block_content" class="grid_1">
          <a href="http://www.facebook.com/pages/Greenocracy/121523694586958"> Facebook </a>
          <a href="https://twitter.com/#!/Greenocracy"> Twitter </a>
          </div>
     </div>
     <div id="footer_block" class="grid_2">
         <div id = "footer_block_header">
         <h3> 
               CONTACT
         </h3>
         </div>
         <div id  = "footer_block_content" class="grid_1">
         <a href="/corp/about"> info@greenocracy.org </a>
         </div>
     </div>
  </div>
</div>
</%def>

<%def name="display_navigbarfn()">
    % if display_navigbar == True:
          <a href="/corp/about"
          % if highlight_name == "about":
               class ="navig_highlight"
          %endif
          > About Us </a>
          <a href="/corp/features"
          % if highlight_name == "features":
               class ="navig_highlight"
          %endif
          > Features </a>
          <a href="/corp/services"
          % if highlight_name == "services":
               class ="navig_highlight"
          %endif
          > Services </a>
          <a href="/corp/careers"
          % if highlight_name == "careers":
               class ="navig_highlight"
          %endif
          > Careers </a>
          <a href="http://greenocracydevelopmentblog.wordpress.com/"
          % if highlight_name == "blog":
               class ="navig_highlight"
          %endif
          > Blog </a>
          <a href="/corp/contact"
          % if highlight_name == "contact":
               class ="navig_highlight"
          %endif
          > Contact </a>
    % endif
</%def>


