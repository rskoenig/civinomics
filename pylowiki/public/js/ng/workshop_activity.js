var workshopApp = angular.module('workshopApp', ['ngSanitize', 'infinite-scroll']);
workshopApp.factory( 'Data', function(){
	return {message:"Im data from the workshopApp factory"}
})

function activityWorkshopController($scope, $http) {
	$scope.listingType = 'activity';
	$scope.activityType = '/all';
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.offset = $scope.sliceSize;
	$scope.numAdopted = 0
	$scope.numIdeas = 0
	$scope.numDiscussions = 0
	$scope.numResources = 0;

	$scope.getActivity = function() {
		$scope.alertMsg = ''
		$scope.activityLoading = true;
		$http.get('/workshop/' + $scope.code + '/' + $scope.url + '/getActivity').success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
				$scope.activity = []
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.noMoreSlices = false;
				$scope.activity = data.result;
				$scope.numAdopted = data.numAdopted;
				$scope.numIdeas = data.numIdeas;
				$scope.numDiscussions = data.numDiscussions;
				$scope.numResources = data.numResources;

				
			}
			$scope.activityLoading = false;
		})
	};

	$scope.getActivity();


	$scope.getAllActivity = function(){
		$scope.activityType = '/all';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getFollowingActivity = function(){
		$scope.activityType = '/following';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getGeoActivity = function(){
		$scope.activityType = '/geo';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getActivitySlice = function() {
		if ($scope.busy || $scope.noMoreSlices) return;
		$scope.busy = true;
		$scope.alertMsg = ''
		$scope.activitySliceLoading = true;
		$http.get('/getActivitySlice/0' + $scope.activityType + '/' + $scope.offset).success(function(data){
			if (data.statusCode == 1){
				$scope.noMoreSlices = true;
			} 
			else if (data.statusCode === 0){
				activitySlice = data.result;
				for (var i = 0; i < activitySlice.length; i++) {
				    $scope.activity.push(activitySlice[i]);
				}
				$scope.noMoreSlices = false;
			}
			$scope.activitySliceLoading = false;
			$scope.busy = false;
			$scope.offset += $scope.sliceSize;
		})
	};


	// Add a new object
	$scope.newObjType = 'idea'
	$scope.submitNewObj = function(){
		var newObjData = {'submit':'submit', 'title': $scope.newObjTitle, 'text': $scope.newObjText, 'link': $scope.newObjLink};
		$scope.newObjURL = '/workshop/' + $scope.code + '/' + $scope.url + '/add/' + $scope.newObjType + '/handler';
		$http.post($scope.newObjURL, newObjData).success(function(data){
			//$scope.numComments = Number($scope.numComments) + 1;
            $scope.getActivity();
            $scope.newObjTitle = '';
            $scope.newObjText = '';
            $scope.newObjLink = '';
        });
	};


	// Menu Items
	$scope.showSummary = true;
	$scope.showInfoPreview = true;
	$scope.showStats = false;

	$scope.toggleSummary= function(){
		$scope.showSummary = true;
		$scope.showInfoPreview = true;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = false;
		$scope.showDiscussions = false;
		$scope.showResources = false;
		$scope.query = '';
	}

	$scope.toggleInfo= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = true;
		$scope.showInfo = true;
		$scope.showStats = false;
		$scope.showIdeas = false;
		$scope.showDiscussions = false;
		$scope.showResources = false;
		$scope.query = '';
	}

	$scope.toggleStats= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = true;
		$scope.showIdeas = false;
		$scope.showDiscussions = false;
		$scope.showResources = false;
		$scope.query = '';
	}

	$scope.toggleIdeas= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = true;
		$scope.showDiscussions = false;
		$scope.showResources = false;
		$scope.query = {objType:'idea'};
	}
	$scope.toggleAdopted= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = true;
		$scope.showDiscussions = false;
		$scope.showResources = false;
		$scope.query = {status:'adopted', };
	}

	$scope.toggleDiscussions= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = false;
		$scope.showDiscussions = true;
		$scope.showResources = false;
		$scope.query = {objType:'discussion'};
	};

	$scope.toggleResources= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = false;
		$scope.showDiscussions = false;
		$scope.showResources = true;
		$scope.query = {objType:'resource'};
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


function workshopMenuController($scope, Data) {
	$scope.data = Data
}

