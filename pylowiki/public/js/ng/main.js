var myApp = angular.module('myApp', ['ngSanitize', 'infinite-scroll', 'ui.bootstrap']);
myApp.factory('ThingData', function(){
	return {message:"I'm data from a service"}
});

function showThingCtrl($scope, $http, ThingData) {

	$scope.item = ThingData

	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };

    $scope.getUrl = '/' + $scope.objType + '/' + $scope.thingCode + '/' + $scope.thingUrl + '/json';

    $scope.getThingData = function(){
    	$http.get($scope.getUrl).success(function(data){
			if (data.statusCode === 0){
				$scope.noResult = true;
			}
			else if (data.statusCode == 1){
				$scope.noResult = false;
				$scope.item = data.thing;
				ThingData = $scope.item

				$scope.urlCode= $scope.item.urlCode;
				$scope.url= $scope.item.url;
				$scope.totalVotes= $scope.item.voteCount;
				$scope.yesVotes= $scope.item.ups;
				$scope.noVotes= $scope.item.downs;
				$scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
        		$scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
				$scope.objType= $scope.item.objType;
				$scope.rated= $scope.item.rated;
				$scope.goal= $scope.item.goal;
				if ($scope.rated == 0) {
			        $scope.voted = '';
			    }
			    else if ($scope.rated == 1){
			        $scope.voted = 'yesVoted';
			    }
			    else if ($scope.rated == -1){
			        $scope.voted = 'noVoted';
			    }

			}
			$scope.loading = false;
		});
    };

    $scope.getThingData();

}

function commentsController($scope, $http, ThingData) {

	$scope.thing = ThingData

	$scope.commentsLoading = false;
	$scope.commentsHidden = true;
	$scope.newCommentLoading = false;

	$scope.getComments = function(){
		if ($scope.commentsHidden == true){
			$scope.commentsLoading = true	
			$http.get('/getComments/' + $scope.thing.discussion ).success(function(data){
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
		$http.get('/getComments/' + $scope.thing.discussion ).success(function(data){
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
		var commentData = {'type':$scope.type, 'thingCode': $scope.thing.urlCode, 'discussionCode': $scope.thing.discussion, 'parentCode': $scope.thing.parentCode, 'comment-textarea': $scope.commentText, 'commentRole': $scope.commentRole, 'submit': $scope.submit};
		$scope.newCommentURL = '/comment/add/handler';
		$http.post($scope.newCommentURL, commentData).success(function(data){
			$scope.numComments = Number($scope.numComments) + 1;
            $scope.getUpdatedComments();
            $scope.commentRole = '';
            $scope.commentText = '';
        });
	};
}


function yesNoVoteCtrl($scope) {
    // initialize the yes/no percentages
    if ($scope.totalVotes == 0){
        $scope.yesPercent = 0;
        $scope.noPercent = 0;
    }
    else if(!($scope.inPage)){
        $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
        $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
    }

    // set the appropriate voting icon
    if ($scope.rated == 0) {
        $scope.voted = '';
    }
    else if ($scope.rated == 1){
        $scope.voted = 'yesVoted';
    }
    else if ($scope.rated == -1){
        $scope.voted = 'noVoted';
    }

    $scope.updateYesVote = function(){

        if ($scope.voted == ''){
            // the user is voting yes from a neutral vote; the score goes up by one
            $scope.totalVotes += 1;
            $scope.netVotes += 1;
            $scope.yesVotes += 1;
            $scope.voted = 'yesVoted';
            $scope.rated = 1;
        } else if ($scope.voted == 'noVoted'){
            // the user is switching a no vote to a yes vote; the score goes up by two
            $scope.netVotes += 2;
            $scope.yesVotes += 1;
            $scope.noVotes -= 1; 
            $scope.voted = 'yesVoted';
            $scope.rated = 1;
        } else if ($scope.voted = 'yesVoted'){
            // the user is undoing their yes vote
            $scope.totalVotes -= 1;
            $scope.netVotes -= 1;
            $scope.yesVotes -= 1;
            $scope.voted = '';
            $scope.rated = 0;
        }

        // recalculate the yes/no percentages
        if ($scope.totalVotes == 0){
            $scope.yesPercent = 0;
            $scope.noPercent = 0;
        }
        else{
            $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
            $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
        }

        $.post('/rate/' + $scope.objType + '/' + $scope.urlCode + '/' + $scope.url + '/1');
    }

    $scope.updateNoVote = function(){
        if ($scope.voted == ''){
            // the user is voting no from a neutral vote; the score goes down by one
            $scope.totalVotes += 1;
            $scope.netVotes -= 1;
            $scope.noVotes += 1;
            $scope.voted = 'noVoted';
            $scope.rated = -1;
        }else if ($scope.voted == 'yesVoted'){
            // if the user had previously placed a yes vote, the score goes down by two
            $scope.netVotes -= 2;
            $scope.yesVotes -= 1;
            $scope.noVotes += 1;
            $scope.voted = 'noVoted';
            $scope.rated = -1;
        }else if ($scope.voted = 'noVoted'){
            // the user is undoing a no vote
            $scope.totalVotes -= 1
            $scope.netVotes += 1
            $scope.noVotes -=1
            $scope.voted = '';
            $scope.rated = 0;
        }

        // recalculate the yes/no percentages
        if ($scope.totalVotes == 0){
            $scope.yesPercent = 0;
            $scope.noPercent = 0;
        }
        else{
            $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
            $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
        }

        $.post('/rate/' + $scope.objType + '/' + $scope.urlCode + '/' + $scope.url + '/-1');
    }
};
