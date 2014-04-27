function meetingsController($scope, $http) {
    $scope.getAgendaItemsURL = '/getMeetingAgendaItems/' + $scope.code + '/' + $scope.url;

    $scope.getAgendaItems = function() {
		$scope.loading = true;
		$http.get($scope.getAgendaItemsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.activity = [];
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activity = data.result;
			}
			$scope.loading = false;
		});
	};
	$scope.getAgendaItems();
}
