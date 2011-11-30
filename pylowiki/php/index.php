<?php
session_start();
/**
 * Copyright 2011 Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

require 'lib/loginlib.php';

function addPermissions($loginStr) {
    $permissions = array(
                  'email',
                  );
    $loginStr = $loginStr."&perms=";
    $count = count($permissions);
    for ($i = 0; $i < $count; $i++) {
        $loginStr = $loginStr.$permissions[$i];
        if ($i != $count-1) {
            $loginStr = $loginStr.",";
        }
    }
    
    return $loginStr;
}
// Create our Application instance (replace this with your appId and secret).
$facebook = new Facebook(array(
  'appId'  => APPID,
  'secret' => SECRET,
));

// Get User ID
$user = $facebook->getUser();

// We may or may not have this data based on whether the user is logged in.
//
// If we have a $user id here, it means we know the user is logged into
// Facebook, but we don't know if the access token is valid. An access
// token is invalid if the user logged out of Facebook.

if ($user) {
  try {
    // Proceed knowing you have a logged in user who's authenticated.
    $user_profile = $facebook->api('/me');
  } catch (FacebookApiException $e) {
    error_log($e);
    $user = null;
  }
}

// Login or logout url will be needed depending on current user state.
if ($user) {
  $logoutUrl = $facebook->getLogoutUrl();
} else {
  $state = $facebook->getState();
  //$loginUrl =
  //$loginUrl."&display=page&response_type=code&fbconnect=1&perms=email";
  //echo "$loginUrl\n";
  $loginUrl =
  "https://www.facebook.com/dialog/permissions.request?app_id=".APPID."
  &display=page&next=".ROOT."&response_type=code&fbconnect=1&state=".$state;
  $loginUrl = addPermissions($loginUrl);
}
?>
<?php
    function PrintLogout() {
        global $logoutUrl;
        echo "<a href=\"".$logoutUrl."\" class=\"fconnect\">";
        echo "</a>";
    }
    function PrintLogin() {
        global $loginUrl;

        //echo $loginUrl;
        echo "<a href=\"".$loginUrl."\" class=\"fconnect\">";
        echo "</a>";
    }
?>
<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <title>Greenocracy</title>
    <link href="fconnect.css" rel="stylesheet" type="text/css" media="screen"/>
  </head>
  <body>
    <?php 
          if ($user) {
              PrintLogout();
              SetSessionAndRedir($user_profile);
          } else {
              PrintLogin();
          }
    ?>
  </body>
</html>
