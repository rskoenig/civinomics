function activityController($scope, $http) {
	$scope.activityLoading = true
	$scope.testing = '1 2 3 4'

	$scope.getActivity = function() {
		$scope.activityLoading = true;
		$http.get('/getSiteActivity').success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.activity = data.result;
			}
			$scope.activityLoading = false;
		})
	};

	$scope.getActivity()

}

function commentsController($scope, $http) {
	$scope.commentsLoading = false
	$scope.commentsHidden = true
	$scope.testing = '1 2 3 4';

	$scope.getComments = function(){
		if ($scope.commentsHidden == true){
			$scope.commentsLoading = true	
			$http.get('/getComments/' + $scope.discussionCode ).success(function(data){
				if (data.statusCode == 1){
					$scope.commentsResult = true;
				} 
				else if (data.statusCode === 0){
					$scope.commentsResult = false;
					$scope.comments = data.result;
				}
				$scope.commentsLoading = false;
				$scope.commentsHidden = false;
			})
		} else {
			$scope.commentsHidden = true
		}
	};
}