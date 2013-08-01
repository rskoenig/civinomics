function fbCheckAccount(response, authResponse, smallPic, bigPic){
    // check for a match by email on our server when a facebook user arrives
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

function postShared(response){
    // someone shared something. record this in the db
    // needing info to define the object that is being shared. could be a workshop, could be an 
    // object within a workshop
    // sending a post at a share url, can this be determined on the controller end?
    // var shareURL = '/workshop/' + $scope.code + '/' + $scope.url + '/share/' + $scope.user + 
    // '/email/handler';
    //  var postData = {'itemURL':$scope.itemURL, 'itemCode':$scope.itemCode, 
    //  'recipientName':$scope.recipientName, 'recipientEmail':$scope.recipientEmail, 
    // 'memberMessage':$scope.memberMessage};
}