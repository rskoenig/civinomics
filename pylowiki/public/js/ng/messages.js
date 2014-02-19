function profileMessagesCtrl($scope, $http) {
	// '/workshop/' + $scope.code + '/' + $scope.url + '/ideas/get'
	$scope.messagesURL = '/messages/get/' + $scope.code + '/' + $scope.url
	$scope.orderProp = '-date';
	$scope.filterProp = '!disabled';
	$scope.numAdopted = '0';
	$scope.numMessages = '0';
	$scope.messagesLoading = true;

	$scope.switchAdopted = function(){
		if ($scope.filterProp == 'adopted'){
			$scope.filterProp = 'proposed';	
		}
		else{
			$scope.filterProp = 'adopted';
		}
	}

	$http.get($scope.messagesURL).success(function(data){
		$scope.messagesLoading = true;
		if (data.statusCode === 1){
			$scope.noResult = true;
			$scope.messagesLoading = false;
		}
		else if (data.statusCode === 2){
			$scope.noResult = true;
			$scope.messagesLoading = false;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.messages = data.result;
			$scope.numAdopted = data.adopted;
			$scope.numMessages = data.numMessages;
			$scope.messagesLoading = false;
		}
	});

}