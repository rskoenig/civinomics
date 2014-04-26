function meetingsController($scope, $http) {
    /*
    * submitStatus: 0   ->  Successfully submitted, like with Unix status codes
    *               1   ->  Error
    *               -1  ->  Not yet submitted
    */

    $scope.submitStatus = '-1';
    $scope.getActivityURL = '/getMeetingAgendaItems/4TMd/the-meeting-of-the-c';

    $scope.getActivity = function() {
		$scope.loading = true;
		$http.get($scope.getActivityURL).success(function(data){
			if (data.statusCode == 1){
				$scope.activity = [];
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.items = data.result;
			}
			$scope.loading = false;
		})
	};
	
	$scope.getActivity()
    
}
