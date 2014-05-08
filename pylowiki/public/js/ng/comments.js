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
		$scope.newCommentLoading = true
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

function commentEditController($scope, $http) {
    
}
