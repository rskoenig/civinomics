
var app = angular.module('civ', ['ngSanitize', 'infinite-scroll']);

app.factory('editService', function ($rootScope) {
    var commentEdit = {};
 
    commentEdit.prepBroadcast = function() {
        this.sendBroadcast();
    };   
    commentEdit.sendBroadcast = function() {
        $rootScope.$broadcast('editDone');
    };
    
    return commentEdit;
});

function commentsController($rootScope, $scope, $http, editService) {
	$scope.commentsLoading = false;
	$scope.commentsHidden = true;
	$scope.newCommentLoading = false;

	$scope.getComments = function(){
		if ($scope.commentsHidden == true){
			$scope.commentsLoading = true	
			$http.get('/getComments/' + $scope.discussionCode ).success(function(data){
				if (data.statusCode == 1){
					$scope.commentsResult = false;
				} 
				else if (data.statusCode === 0){
					$scope.commentsResult = true;
					$scope.comments = data.result;
				}
				$scope.commentsLoading = false;
				$scope.commentsHidden = false;
				$scope.showNewComment = true;
			})
		} else {
			$scope.commentsHidden = true;
			$scope.showNewComment = false;
		}
	};

	$scope.getUpdatedComments = function(){
		$http.get('/getComments/' + $scope.discussionCode ).success(function(data){
			if (data.statusCode == 1){
				$scope.commentsResult = false;
			} 
			else if (data.statusCode === 0){
				$scope.commentsResult = true;
				$scope.comments = data.result;
				$scope.commentsHidden = false;
				$scope.showNewComment = true;
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

	$scope.showNewComment = false;
	$scope.toggleNewComment = function(){
		if ($scope.showNewComment == true){
			$scope.showNewComment = false;
			$scope.commentsHidden = true;
		} else{
			$scope.showNewComment = true;
		}
	}

	$scope.submitComment = function(){
		$scope.newCommentLoading = true
		$scope.commentData = {'type':$scope.type, 'thingCode': $scope.thingCode, 'discussionCode': $scope.discussionCode, 'parentCode': $scope.parentCode, 'comment-textarea': $scope.commentText, 'commentRole': $scope.commentRole, 'submit': $scope.submit};
		$scope.newCommentURL = '/comment/add/handler';
		$http.post($scope.newCommentURL, $scope.commentData).success(function(data){
			$scope.numComments = Number($scope.numComments) + 1;
            $scope.getUpdatedComments();
            $scope.commentRole = '';
            $scope.commentText = '';
            $scope.commented = true
        });
	};
	
	$scope.$on('editDone', function() {
	    $scope.getUpdatedComments();
    });
}

function commentEditController($rootScope, $scope, $http, editService) {
        $scope.submitEditComment = function() {
    		$scope.newCommentLoading = true;
    		var commentData = {'commentCode': $scope.urlCode, 'commentText': $scope.commentEditText, 'commentRole': $scope.commentEditRole, 'submit': $scope.submit};
    		$scope.editCommentURL = '/comment/edit/handler';
    		$http.post($scope.editCommentURL, commentData).success(function(data){
                editService.prepBroadcast();
            });
    	};
    	
    	$scope.editing = true;
    	
    	$scope.submitListingEditComment = function() {
            var commentData = {'commentCode': $scope.urlCode, 'commentText': $scope.commentEditText, 'commentRole': $scope.commentEditRole, 'submit': $scope.submit};
    		$scope.editCommentURL = '/comment/edit/handler';
    		$scope.editing = false;
    		$scope.item.html = $scope.commentEditText;
    		$http.post($scope.editCommentURL, commentData).success(function(data){
                
            });
    	};

}

commentEditController.$inject = ['$rootScope', '$scope', '$http', 'editService'];
commentsController.$inject = ['$rootScope', '$scope', '$http', 'editService'];
