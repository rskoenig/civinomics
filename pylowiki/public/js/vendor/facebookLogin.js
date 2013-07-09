function fbLogin(facebookAppId) {
//$('#fbLogin').on('click', function (e) {

 window.fbAsyncInit = function() {
    FB.init({
      appId      : facebookAppId, // ${facebookAppId}, '133971610029022', App ID
      channelUrl : 'http://www.civinomics.com/channel.html', // Channel File
      status     : true, // check login status
      cookie     : false, // enable cookies to allow the server to access the session
      xfbml      : true  // parse XFBML
    });

    // Here we subscribe to the auth.authResponseChange JavaScript event. This event is fired
    // for any authentication related change, such as login, logout or session refresh. This means that
    // whenever someone who was previously logged out tries to log in again, the correct case below 
    // will be handled. 
    console.log('window init');
    FB.Event.subscribe('auth.login', function(response1) {
      console.log('auth.login fired');
      authSignal();
    });
    FB.Event.subscribe('auth.authResponseChange', function(response) {
      // Here we specify what we do with the response anytime this event occurs. 
      
      console.log('above response tree');
      if (response.status === 'connected') {
        //  We're given the token and other info - good for makig calls to fb
        // locally, we've found that this person is logged into fb, and has given us 
        // permission to work with this auth.
        //  In order to preserve a standard login/signup experience, we will save this 
        // info in the user's session, including a stamp (if necessary) confirming this
        // person is auth'd for an fb-backed login.
        // * store the auth token and exp time in this person's session
        // * change the fb button into a button that will ask the server to 'log in'
        // by confirming it's ok with fb
        //console.log('token: ' + response.authResponse.accessToken);
        // we can use fb to login to the site. at this point store the token and exp
        console.log('calling fb connected');
        fbConnected(response.authResponse);
      } else if (response.status === 'not_authorized') {
        // In this case, the person is logged into Facebook, but not into the app, so we call
        // FB.login() to prompt them to do so. 
        // In real-life usage, you wouldn't want to immediately prompt someone to login 
        // like this, for two reasons:
        // (1) JavaScript created popup windows are blocked by most browsers unless they 
        // result from direct interaction from people using the app (such as a mouse click)
        // (2) it is a bad experience to be continually prompted to login upon page load.
        console.log('not authd');                
        FB.login();
        
        //FB.login(function(response) {
          // handle the response
        //}, {scope: 'name, email, user_location, user_hometown'});
      } else {
        // In this case, the person is not logged into Facebook, so we call the login() 
        // function to prompt them to do so. Note that at this stage there is no indication
        // of whether they are logged into the app. If they aren't then they'll see the Login
        // dialog right after they log in to Facebook. 
        // The same caveats as above apply to the FB.login() call here.
        console.log('else');
        FB.login();
        
        //FB.login(function(response) {
          // handle the response
        //}, {scope: 'name, email, user_location, user_hometown'});
      }
    });
 };

 // Load the SDK asynchronously
 (function(d){
  var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
  if (d.getElementById(id)) {return;}
  js = d.createElement('script'); js.id = id; js.async = true;
  js.src = "//connect.facebook.net/en_US/all.js";
  ref.parentNode.insertBefore(js, ref);
 }(document));

 // Here we run a very simple test of the Graph API after login is successful. 
 // This testAPI() function is only called in those cases. 
 function testAPI() {
   console.log('Welcome!  Fetching your information.... ');
   FB.api('/me', function(response) {
     console.log('name: ' + response.name + '.email: ' + response.email + '.username: ' + response.username + '.user_location' + response.user_location + '.user_hometown' +  response.user_hometown + '.');
   });
 }

 function authSignal() {
   console.log('in auth signal')
   var authSignal = '<div id="authSignal"></div>'
   $('#fbLoginButton1').append(authSignal);
   $('#fbLoginButton2').append(authSignal);
   console.log('should have added this: '+authSignal)
 }

 function fbConnected(authResponse) {
   FB.api('/me', function(response) {
     // the FQL query: Get the link of the image, that is the first in the album "Profile pictures" of this user.

     //var bigPicFql = FB.Data.query('select src_big from photo where pid in (select cover_pid from album where owner={0} and name="Profile Pictures")', response.id);
     var bigPicFql = FB.Data.query('SELECT url FROM profile_pic WHERE id = {0} AND width=200 AND height=200', response.id);
     var bigPic = '';
     bigPicFql.wait(function (rows) {
       // the big pic link
       bigPic = rows[0].url;
       console.log('big pic: ' + bigPic)
     });
     var smallPicFql = FB.Data.query('SELECT url FROM profile_pic WHERE id = {0}', response.id);
     var smallPic = '';
     var holder = 0;
     smallPicFql.wait(function (rows) {
       //the small pic link
       smallPic = rows[0].url;
       holder = 1;
     });
     var result = ''
     setTimeout(function(){
       // fbCheckAccount will verify a spoof is not happening then determine if there's
       // a matching account on site yet. if so, result will contain html for visiting a 
       // page that will log this user in.
       result = fbCheckAccount(response, authResponse, smallPic, bigPic);
       if (result == "not found") {
         console.log('no account on site yet')
         // no account on site yet.
         // this is a unique situation where the person has authorized us to use their
         // fb identity, but hasn't created an account yet. This assumes that's what they
         // want to do and redirects once this situation is recognized.
         if ($('#fbSignUp').length) {
           console.log('facebook signup')
         } else {
           window.location = '/signup/fbSignUp/';
         }
       } else {
         console.log('account found')
         if ($('#authSignal').length) {
           console.log('auth signal heard')
           // this triggers when a person has arrived but was not yet logged inot facebook or
           // had not yet given auth to our app
           var newButton = 'Logging In'
           $('#fbLoginButton1').html(newButton);
           $('#fbLoginButton2').html(newButton);
           window.location = '/fbLoggingIn/';
         
         } else if ($('#fbLoggingIn').length) {
           // this element is only found on a page meant to be used as a redirect when
           // the 'login with facebook' link has been clicked.
           window.location = '/fbLoggingIn/';
         } else {
           // this code is used when a person arrives and it is seen that they have 
           // auth'd our app and are logged into facebook 
           // replace current button with returned result
           var newButton = '<a href="/fbLogin"><img src="/images/fb_signin.png"></a>'
           $('#fbLoginButton1').html(newButton);
           $('#fbLoginButton2').html(newButton);
         }
       }
     },1000);
   });
 }
//})
}