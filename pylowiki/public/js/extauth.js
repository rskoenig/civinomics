function fbCheckAccount(response, authResponse){
    // console.log('email in extauth: ' + email);
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