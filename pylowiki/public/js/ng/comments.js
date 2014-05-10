
var commentApp = angular.module('civ', ['ngSanitize', 'infinite-scroll']);

commentApp.factory('editService', function ($rootScope) {
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
	
	$scope.$on('editDone', function() {
	    $scope.getUpdatedComments();
    });
}

function commentEditController($rootScope, $scope, $http, editService) {
        $scope.submitEditComment = function(){
		$scope.newCommentLoading = true;
		var commentData = {'commentCode': $scope.urlCode, 'commentText': $scope.commentEditText, 'commentRole': $scope.commentEditRole, 'submit': $scope.submit};
		$scope.editCommentURL = '/comment/edit/handler';
		$http.post($scope.editCommentURL, commentData).success(function(data){
            editService.prepBroadcast();
        });
	};
    
}

commentEditController.$inject = ['$rootScope', '$scope', '$http', 'editService'];
commentsController.$inject = ['$rootScope', '$scope', '$http', 'editService'];
