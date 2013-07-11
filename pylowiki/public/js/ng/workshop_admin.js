function adminController($scope, $http, $location) {
  $scope.showResponse         = false;
  
  $scope.setDemo = function() {
    var setDemoURL = '/demo/set/' + $scope.code;
    var postData = '';
    $http.post(setDemoURL, postData).success(function(data){
        $scope.response = data;
        $scope.showResponse = true;
    });
  };
}

function facilitatorController($scope, $http, $location) {
  $scope.emailOnFlaggedShow   = false;
  $scope.emailOnAddedShow     = false;
  
  $scope.emailOnFlagged = function() {
    var flaggedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/facilitate/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'flags'};
    $http.post(flaggedURL, postData).success(function(data){
      $scope.emailOnFlaggedShow = true;
      $scope.emailOnFlaggedResponse = data;
    });
  };
  $scope.emailOnAdded = function() {
    var addedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/facilitate/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'items'};
    $http.post(addedURL, postData).success(function(data){
      $scope.emailOnAddedShow = true;
      $scope.emailOnAddedResponse = data;
    });
  };
}

function listenerController($scope, $http, $location) {
    $scope.addListenerShow     = false;
    $scope.disableListenerShow     = false;
    $scope.emailListenerShow     = false
    
    $scope.saveListener = function() {
        var addURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/add/handler';
        var postData = {'userCode':$scope.user, 'lName': $scope.lName, 'lTitle': $scope.lTitle, 'lEmail': $scope.lEmail};
        $http.post(addURL, postData).success(function(data){
            $scope.addListenerShow = true;
            $scope.addListenerResponse = data;
            $scope.lName = '';
            $scope.lTitle = '';
            $scope.lEmail = '';
        });
    };  
    $scope.toggleListener = function() {
        var disableURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/disable/handler';
        var postData = {'urlCode':$scope.listener, 'lReason':$scope.lReason};
        $http.post(disableURL, postData).success(function(data){
            $scope.disableListenerShow = true;
            $scope.disableListenerResponse = data;
            $scope.lReason = '';
        });
    };
    $scope.emailListener = function() {
        var emailURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/email/handler';
        var postData = {'urlCode':$scope.listener};
        $http.post(emailURL, postData).success(function(data){
            $scope.emailListenerShow = true;
            $scope.emailListenerResponse = data;
        });
    };
}
  