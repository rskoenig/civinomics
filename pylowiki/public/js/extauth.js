function fbCheckAccount(response, authResponse, smallPic, bigPic){
    //console.log('in /public/js/extauth.js fbCheckAccount: ' + response.name);
    //var newstring = 'email in extauth: ' + email;
    //return newstring;
    //console.log('hello')
    var encodedSmall = encodeURIComponent(smallPic)
    encodedSmall = encodedSmall.replace(/\%/g, ",")
    var encodedBig = encodeURIComponent(bigPic)
    encodedBig = encodedBig.replace(/\%/g, ",")
    var checkURL = "/extauth/fbEmail/" + response.name + "&" + response.email + "&" + authResponse.accessToken + "&" + authResponse.expiresIn + "&" + authResponse.signedRequest + "&" + authResponse.userID + "&" + encodedSmall + "&" + encodedBig 
    //console.log('urlcheck: '+checkURL)
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;
    //console.log('cr ' + checkResult)
    return checkResult;
    //var gobj = jQuery.parseJSON(checkResult);
    //return gobj.result
    //document.getElementById("postalCodeResult").innerText = document.getElementById("postalCodeResult").textContent = gobj.result;
}

function postShared(response, itemCode, itemURL, postId, userCode, workshopCode, shareType){
    // someone shared something. record this in the db
    // needing info to define the object that is being shared. could be a workshop, could be an 
    // object within a workshop
    // ! determine this here, then send the message to the corresponding route
    var encodedUrl = encodeURIComponent(itemURL)
    encodedUrl = encodedUrl.replace(/\%/g, ",")
    
    var checkURL = "/share/facebook/" + userCode + "/" + workshopCode + "/" + itemCode + "/" + encodedUrl + "/" + postId + "/" + shareType
    //var checkURL = "/share/facebook"
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;

    return checkResult
}

function fPrintObject(o) {
    var out = '';
    for (var p in o) {
        out += p + ': ' + o[p] + '\n';
    }
    //console.log(out);
}

function facebookLogin() {
    FB.login(function(response) {
        if (response.authResponse) {
            //console.log('Welcome!  Fetching your information.... ');
            //console.log("response status: " + response.status)
            //fPrintObject(response);
            //console.log("response email: " + response.email)
            fPrintObject(response.authResponse);
            //fbConnected(response.authResponse);
            facebookConnected(response.authResponse);
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: 'email'});
}

function facebookConnected(authResponse) {
    console.log('facebookConnected'); 
    FB.api('/me', function(response) {
        //console.log('in fbapi'); 
        // grab the url to a 200x200 photo of this user
        var bigPicFql = FB.Data.query('SELECT url FROM profile_pic WHERE id = {0} AND width=200 AND height=200', response.id);
        var bigPic = '';
        bigPicFql.wait(function (rows) {
            // the big pic link
            bigPic = rows[0].url;
        });
        // grab the url to a 50x50 photo of this user
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
            //console.log('setTimeout(function');
            // check account status on our site for this user
            result = fbCheckAccount(response, authResponse, smallPic, bigPic);
            if (result == "not found") {
                //console.log('not found');
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
                //console.log('found');
                //window.location = '/fbLoggingIn/';
                // found a matching account on our site
                if ($('#authSignal').length) {
                    //console.log('no auth signal');
                    // this triggers when a person has arrived but was not yet logged into facebook,
                    // or had not yet given auth to our app
                    var newButton = 'Logging In'
                    $('#fbLoginButton1').html(newButton);
                    $('#fbLoginButton2').html(newButton);
                    window.location = '/fbLoggingIn/';
                } else if ($('#fbLoggingIn').length) {
                    //console.log('fbLoggingIn');
                    // this element is only found on a page meant to be used as a redirect when
                    // the 'login with facebook' link has been clicked.
                    window.location = '/fbLoggingIn/';
                } else {
                    //console.log('new buttons');
                    // this code is used when a person arrives and it is seen that they have 
                    // auth'd our app and are logged into facebook 
                    // replace current button with returned result
                    var newButton = '<a href="/fbLogin"><img src="/images/f-login.png"></a>'
                    $('#fbLoginButton1').html(newButton);
                    $('#fbLoginButton2').html(newButton);
                }
            }
        },1000);
    });
}