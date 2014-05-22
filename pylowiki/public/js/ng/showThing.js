function showThingCtrl($scope, $http) {
	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };

    
    $scope.test = "ya voll herr commandant"

    $scope.getUrl = '/' + $scope.objType + '/' + $scope.thingCode + '/' + $scope.thingUrl + '/json';

    $scope.getThingData = function(){
    	$http.get($scope.getUrl).success(function(data){
			if (data.statusCode === 0){
				$scope.noResult = true;
			}
			else if (data.statusCode == 1){
				$scope.noResult = false;
				$scope.item = data.thing;

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
