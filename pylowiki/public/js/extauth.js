function fbCheckAccount(responseName, authResponse, smallPic, bigPic){
    // NOTE: response.email not working, can't retrieve email at this point

    var encodedSmall = encodeURIComponent(smallPic)
    encodedSmall = encodedSmall.replace(/\%/g, ",")
    var encodedBig = encodeURIComponent(bigPic)
    encodedBig = encodedBig.replace(/\%/g, ",")
    var checkURL = "/extauth/fbEmail/" + responseName + "&" + 'emailNotAvailable' + "&" + authResponse.accessToken + "&" + authResponse.expiresIn + "&" + authResponse.signedRequest + "&" + authResponse.userID + "&" + encodedSmall + "&" + encodedBig 
    //console.log('urlcheck: '+checkURL)
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;
    //console.log('cr ' + checkResult)
    return checkResult;
}

// *************************************************
// function postShared
// *** called by facebook javascript sdk code when an item is shared on a wall or in a message
// e.g. wallpost: postShared(response, thingCode, link, response.post_id, userCode, parentCode, 'facebook-wall')
// e.g. message: postShared("no response", thingCode, link, '0', userCode, parentCode, 'facebook-message')
// *************************************************
function postShared(response, itemCode, itemURL, postId, userCode, parentCode, shareType){
    itemCode = itemCode || "noitemCode";
    itemURL = itemURL || "noitemURL";
    postId = postId || "nopostId";
    userCode = userCode || "nouserCode";
    parentCode = parentCode || "noParentCode";
    shareType = shareType || "noshareType";
    // someone shared something. record this in the db
    // needing info to define the object that is being shared. could be a workshop, could be an 
    // object within a workshop
    // ! determine this here, then send the message to the corresponding route
    var encodedUrl = encodeURIComponent(itemURL)
    encodedUrl = encodedUrl.replace(/\%/g, ",")
    console.log('ext auth postshared itemcode: '+itemCode);
    //console.log('ea wc: '+parentCode);
    var checkURL = "/share/facebook/" + userCode + "/" + parentCode + "/" + itemCode + "/" + encodedUrl + "/" + postId + "/" + shareType
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