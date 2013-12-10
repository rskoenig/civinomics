function userLookupCtrl($scope, $http) {
	$scope.test = "testing testing 3 2 1 4";
	$scope.authorsURL = '/initiative/' + $scope.urlCode + '/' + $scope.url + '/getAuthors';
	$scope.userValue = '';
	$scope.userLookupURL = '/search/people/name/' + $scope.userValue;
	$http.get($scope.userLookupURL).success(function(data){
		if (data.statusCode == 1){
			$scope.noResult = true;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.users = data.result;
		}
	});
	$http.get($scope.authorsURL).success(function(data){
		if (data.statusCode == 1){
			$scope.noResult = true;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.authors = data.result;
		}
	});

	$scope.lookup = function() {
		$scope.userLookupURL = '/search/people/name/' + $scope.userValue;
		$http.get($scope.userLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.users = data.result;
			}
		});
	}

	$scope.removeCoA = function(removeAuthorCode) {
		$scope.removeAuthorCode = removeAuthorCode;
		$.post('/initiative/' + $scope.urlCode + '/' + $scope.url + '/' + $scope.removeAuthorCode + '/facilitate/resign/handler');
		$http.get($scope.authorsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.authors = data.result;
			}
		});
	}

	$scope.submitInvite = function(inviteAuthorCode){
		$scope.inviteAuthorCode = inviteAuthorCode;
		$.post('/initiative/' + $scope.urlCode + '/' + $scope.url + '/' + $scope.inviteAuthorCode + '/facilitate/invite/handler');
		$http.get($scope.authorsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.authors = data.result;
			}
		});
	}




}