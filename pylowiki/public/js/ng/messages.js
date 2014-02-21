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

	$scope.isRead= function(read) {
        if (read == '1') {
        	return true;
        } else {
        	return false;
        }
    }

    $scope.notRead = function(read) {
    	if (read != '1') {
        	return true;
        } else {
        	return false;
        }
    }

	$http.get($scope.messagesURL).success(function(data){
		console.log('got messages');
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
			console.log('there are results');
			console.log(data.result);
			$scope.noResult = false;
			$scope.messages = data.result;
			$scope.numAdopted = data.adopted;
			$scope.numMessages = data.numMessages;
			$scope.messagesLoading = false;
		}
	});

}