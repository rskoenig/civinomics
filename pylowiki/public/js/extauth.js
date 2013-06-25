function fbCheckAccount(response, authResponse, smallPic){
    console.log('in extauth fbCheckAccount: ' + response.name);
    //var newstring = 'email in extauth: ' + email;
    //return newstring;
    var encodedLink = encodeURIComponent(smallPic)
    encodedLink = encodedLink.replace(/\%/g, ",")
    var checkURL = "/extauth/fbEmail/" + response.name + "&" + response.email + "&" + authResponse.accessToken + "&" + authResponse.expiresIn + "&" + authResponse.signedRequest + "&" + authResponse.userID + "&" + encodedLink
    
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;
    console.log('cr ' + checkResult)
    return checkResult;
    //var gobj = jQuery.parseJSON(checkResult);
    //return gobj.result
    //document.getElementById("postalCodeResult").innerText = document.getElementById("postalCodeResult").textContent = gobj.result;
}

function fbSetProfilePicSmall(picLink){
    console.log('in extauth small pic: ' + picLink);
    var encodedLink = encodeURIComponent(picLink)
    console.log('in extauth small pic end: ' + encodedLink);
    var setURL = "/extauth/fbProfilePicSmall/" + encodedLink
    //var setURL = "/extauth/fbProfilePicSmall/" + 'testing'
    //var setURL = "/extauth/fbEmail/" + encodedLink
    console.log('posting to: ' + setURL)
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : setURL
    }).responseText;
    return checkResult;
}