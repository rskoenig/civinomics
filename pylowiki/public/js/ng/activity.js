function activityController($scope, $http) {
	$scope.listingType = 'activity';
	$scope.activityType = '/all'
	$scope.activityLoading = true

	$scope.getActivity = function() {
		$scope.alertMsg = ''
		$scope.activityLoading = true;
		$http.get('/getSiteActivity' + $scope.activityType).success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
				$scope.activity = []
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.activity = data.result;
			}
			$scope.activityLoading = false;
		})
	};

	$scope.getActivity()


	$scope.getAllActivity = function(){
		$scope.activityType = '/all'
		$scope.getActivity()
	};

	$scope.getFollowingActivity = function(){
		$scope.activityType = '/following'
		$scope.getActivity()
	};

	$scope.getGeoActivity = function(){
		$scope.activityType = '/geo'
		$scope.getActivity()
	};

}

function commentsController($scope, $http) {
	$scope.commentsLoading = false;
	$scope.commentsHidden = true;
	$scope.newCommentLoading = false;

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

	$scope.getUpdatedComments = function(){
		$scope.newCommentLoading = true
		$http.get('/getComments/' + $scope.discussionCode ).success(function(data){
			if (data.statusCode == 1){
				$scope.commentsResult = true;
			} 
			else if (data.statusCode === 0){
				$scope.commentsResult = false;
				$scope.comments = data.result;
			}
			$scope.newCommentLoading = false
		})
	};

	$scope.showAddComments = function(){
		if ($scope.commentsHidden == true){
			$scope.commentsHidden = false;
		} else{
			$scope.commentsHidden = true;
		}
	};

	$scope.submitComment = function(){
		var commentData = {'type':$scope.type, 'thingCode': $scope.thingCode, 'discussionCode': $scope.discussionCode, 'parentCode': $scope.parentCode, 'comment-textarea': $scope.commentText, 'commentRole': $scope.commentRole, 'submit': $scope.submit};
		$scope.newCommentURL = '/comment/add/handler';
		$http.post($scope.newCommentURL, commentData).success(function(data){
			$scope.numComments = Number($scope.numComments) + 1;
            $scope.getUpdatedComments();
            $scope.commentRole = '';
            $scope.commentText = '';
        });
	};
}