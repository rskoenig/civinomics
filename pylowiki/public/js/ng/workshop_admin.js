function adminController($scope, $http, $location) {
  $scope.showResponse = false;
  
  $scope.setDemo = function() {
    var setDemoURL = '/demo/set/' + $scope.code;
    var postData = '';
    $http.post(setDemoURL, postData).success(function(data){
        $scope.response = data;
        $scope.showResponse = true;
    });
  };
};
