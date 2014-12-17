
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
    $scope.showRevisions = false;
	$scope.commentsHidden = true;
	$scope.newCommentLoading = false;
	$scope.commentText = "";
	$scope.textArea = 1;
    $scope.limitComments = 0;
    $scope.showMore = false;

    $scope.getTextAreaRows = function() {
       var newRows = Math.ceil($scope.commentText.length/58);
       if (newRows > 1) 
            return newRows;
        else
            return $scope.textArea;
    }
    
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
					$scope.updateLimit();
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
				$scope.updateLimit();
				$scope.commentsHidden = false;
				$scope.showNewComment = true;
				$scope.$apply();
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
		$scope.newCommentLoading = true;
		$scope.commentData = 
        		{'type':$scope.type, 
        		'thingCode': $scope.thingCode, 
        		'discussionCode': $scope.discussionCode, 
        		'parentCode': $scope.parentCode, 
        		'comment-textarea': $scope.commentText, 
        		'commentRole': $scope.commentRole, 
        		'submit': $scope.submit};
		$scope.newCommentURL = '/comment/add/handler';
		$http.post($scope.newCommentURL, $scope.commentData).success(function(data){
			$scope.numComments = Number($scope.numComments) + 1;
            $scope.getUpdatedComments();
            $scope.commentRole = '';
            $scope.commentText = '';
            $scope.commented = true;
        });
	};
	
	
	$scope.$on('editDone', function() {
	    $scope.getUpdatedComments();
    });
    
    $scope.updateLimit = function() {
        if ($scope.numComments > 3){
            $scope.limitComments = 3;
            $scope.showMore = true;
        } else {
            $scope.limitComments = $scope.numComments;
            $scope.showMore = false;
        };
    };
    
    $scope.removeLimit = function() {
        $scope.limitComments = $scope.numComments;
        $scope.showMore = false;
    };
    
    if ($scope.numComments > 0){
        $scope.getComments();
        $scope.updateLimit();
    };
}

function commentEditController($rootScope, $scope, $http, editService) {
        $scope.submitEditComment = function() {
    		$scope.newCommentLoading = true;
    		$scope.$parent.editing = !$scope.$parent.editing;
    		$scope.comment.html = $scope.commentEditText;
    		var commentData = {'commentCode': $scope.urlCode, 'commentText': $scope.commentEditText, 'commentRole': $scope.commentEditRole, 'submit': $scope.submit};
    		$scope.editCommentURL = '/comment/edit/handler';
    		$http.post($scope.editCommentURL, commentData).success(function(data){
                editService.prepBroadcast();
            });
    	};
    	
    	$scope.editing = false;
    	
    	$scope.submitListingEditComment = function() {
            var commentData = {'commentCode': $scope.urlCode, 'commentText': $scope.commentEditText, 'commentRole': $scope.commentEditRole, 'submit': $scope.submit};
    		$scope.editCommentURL = '/comment/edit/handler';
    		$scope.item.html = $scope.commentEditText;
    		$scope.item.position = $scope.commentEditRole;
    		$http.post($scope.editCommentURL, commentData).success(function(data){
                $scope.editing = false;
            });
    	};
    	
    	$scope.changeEditing = function() {
        	$scope.editing = !$scope.editing;
    	};

}

commentEditController.$inject = ['$rootScope', '$scope', '$http', 'editService'];
commentsController.$inject = ['$rootScope', '$scope', '$http', 'editService'];
