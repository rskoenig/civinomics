function initiativeCtrl($scope) {
	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };

    $scope.showingText = true;
    $scope.showingResources = false;
    $scope.showingUpdates = false;


    $scope.showText = function(){
    	// http.get initiative text controller function
    	$scope.showingText = true;
    	$scope.showingResources = false;
    	$scope.showingUpdates = false;
    };

    $scope.showResources = function(){
    	// http.get initiative resources controller function
    	$scope.showingText = false;
    	$scope.showingResources = true;
    	$scope.showingUpdates = false;
    };

     $scope.showUpdates = function(){
    	// http.get initiative updates controller function
    	$scope.showingText = false;
    	$scope.showingResources = false;
    	$scope.showingUpdates = true;
    };
}
