function facilitatorController($scope, $http, $location) {
  $scope.emailOnFlaggedShow   = false;
  $scope.emailOnAddedShow     = false;
  
  $scope.emailOnFlagged = function() {
    var flaggedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/facilitate/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'flags'};
    $http.post(flaggedURL, postData).success(function(data){
      $scope.emailOnFlaggedShow = true;
      $scope.emailOnFlaggedResponse = data;
    })
  }
  
  $scope.emailOnAdded = function() {
    var addedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/facilitate/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'items'};
    $http.post(addedURL, postData).success(function(data){
      $scope.emailOnAddedShow = true;
      $scope.emailOnAddedResponse = data;
    })
  }
}

function listenerController($scope, $http, $location) {
  $scope.emailOnAddedShow     = false;
  
  $scope.emailOnAdded = function() {
    var addedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listen/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'items'};
    $http.post(addedURL, postData).success(function(data){
      $scope.emailOnAddedShow = true;
      $scope.emailOnAddedResponse = data;
    })
  }
}

function followerController($scope, $http, $location) {
  $scope.emailOnAddedShow     = false;
  
  $scope.emailOnAdded = function() {
    var addedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/follow/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'items'};
    $http.post(addedURL, postData).success(function(data){
      $scope.emailOnAddedShow = true;
      $scope.emailOnAddedResponse = data;
    })
  }
}

function pmemberController($scope, $http, $location) {
  $scope.emailOnAddedShow     = false;
  
  $scope.emailOnAdded = function() {
    var addedURL = '/workshop/' + $scope.code + '/' + $scope.url + '/private/' + $scope.user+ '/notifications/handler';
    var postData = {'user':$scope.user, 'alert':'items'};
    $http.post(addedURL, postData).success(function(data){
      $scope.emailOnAddedShow = true;
      $scope.emailOnAddedResponse = data;
    })
  }
}
