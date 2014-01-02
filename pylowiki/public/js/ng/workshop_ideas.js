function workshopIdeasCtrl($scope, $http) {
	$scope.ideasURL = '/workshop/' + $scope.code + '/' + $scope.url + '/ideas/get'
	$scope.orderProp = '-date';

	$http.get($scope.ideasURL).success(function(data){
		if (data.statusCode == 1){
			$scope.noResult = true;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.ideas = data.result;
		}
	});
}