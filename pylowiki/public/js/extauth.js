function fbCheckAccount(response, authResponse, smallPic, bigPic){
    console.log('in /public/js/extauth.js fbCheckAccount: ' + response.name);
    //var newstring = 'email in extauth: ' + email;
    //return newstring;
    var encodedSmall = encodeURIComponent(smallPic)
    encodedSmall = encodedSmall.replace(/\%/g, ",")
    var encodedBig = encodeURIComponent(bigPic)
    encodedBig = encodedBig.replace(/\%/g, ",")
    var checkURL = "/extauth/fbEmail/" + response.name + "&" + response.email + "&" + authResponse.accessToken + "&" + authResponse.expiresIn + "&" + authResponse.signedRequest + "&" + authResponse.userID + "&" + encodedSmall + "&" + encodedBig 
    
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

function postShared(response, itemCode, itemURL, postId, userCode, workshopCode){
    // someone shared something. record this in the db
    // needing info to define the object that is being shared. could be a workshop, could be an 
    // object within a workshop
    // ! determine this here, then send the message to the corresponding route
    var encodedUrl = encodeURIComponent(itemURL)
    encodedUrl = encodedUrl.replace(/\%/g, ",")
    //var checkURL = "/share/facebook/" + itemCode + "&" + postId + "&" + encodedUrl
    var checkURL = "/share/facebook/" + userCode + "/" + workshopCode + "/" + itemCode + "/" + postId + "/" + encodedUrl
    //var checkURL = "/share/facebook"
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;

    return checkResult
    // ! determine this in the controller, creating the correct share object
    //  - in the controller, depending on the parameters seen, create a share of a workshop,
    // or a share of an object
    // sending a post at a share url, can this be determined on the controller end?
    // var shareURL = '/workshop/' + $scope.code + '/' + $scope.url + '/share/' + $scope.user + 
    // '/email/handler';
    //  var postData = {'itemURL':$scope.itemURL, 'itemCode':$scope.itemCode, 
    //  'recipientName':$scope.recipientName, 'recipientEmail':$scope.recipientEmail, 
    // 'memberMessage':$scope.memberMessage};
}

function postTest(){
    var checkURL = "/share/test"
    
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url : checkURL
    }).responseText;

    return checkResult    
}