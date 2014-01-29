function workshopIdeasCtrl($scope, $http) {
	$scope.ideasURL = '/workshop/' + $scope.code + '/' + $scope.url + '/ideas/get'
	$scope.orderProp = '-date';
	$scope.filterProp = '!disabled';
	$scope.numAdopted = '0';
	$scope.numIdeas = '0';

	$scope.switchAdopted = function(){
		if ($scope.filterProp == 'adopted'){
			$scope.filterProp = 'proposed';	
		}
		else{
			$scope.filterProp = 'adopted';
		}
	}

	$http.get($scope.ideasURL).success(function(data){
		if (data.statusCode == 1){
			$scope.noResult = true;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.ideas = data.result;
			$scope.numAdopted = data.adopted;
			$scope.numIdeas = data.numIdeas;
		}
	});

}