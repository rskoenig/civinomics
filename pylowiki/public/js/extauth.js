function fbCheckAccount(response, authResponse){
    console.log('in extauth fbCheckAccount: ' + response.name);
    //var newstring = 'email in extauth: ' + email;
    //return newstring;
    var checkURL = "/extauth/fbEmail/" + response.name + "&" + response.email + "&" + authResponse.accessToken + "&" + authResponse.expiresIn + "&" + authResponse.signedRequest + "&" + authResponse.userID
    //var checkURL = "/geo/cityStateCountry/" + postalCode
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;
    return checkResult;
    //var gobj = jQuery.parseJSON(checkResult);
    //return gobj.result
    //document.getElementById("postalCodeResult").innerText = document.getElementById("postalCodeResult").textContent = gobj.result;
}

function fbSetProfilePicSmall(picLink){
    console.log('in extauth small pic: ' + picLink);
    var encodedLink = encodeURIComponent(picLink)
    console.log('in extauth small pic end: ' + encodedLink);
    var setURL = "/extauth/fbProfSm/" + encodedLink
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : setURL
    }).responseText;
}