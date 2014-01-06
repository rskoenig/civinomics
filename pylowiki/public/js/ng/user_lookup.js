function userLookupCtrl($scope, $http) {
	$scope.test = "testing testing 3 2 1 4";
	$scope.loading = true;
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
			$scope.loading = false;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.authors = data.result;
			$scope.loading = false;
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
		$scope.loading = true;
		$scope.removeAuthorCode = removeAuthorCode;
		$http.post('/initiative/' + $scope.urlCode + '/' + $scope.url + '/' + $scope.removeAuthorCode + '/facilitate/resign/handler');
		$http.get($scope.authorsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
				$scope.loading = false;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.authors = data.result;
				$scope.loading = false;
			}
		});
	}

	$scope.submitInvite = function(inviteAuthorCode){
		$scope.loading = true;
		$scope.inviteAuthorCode = inviteAuthorCode;
		$http.post('/initiative/' + $scope.urlCode + '/' + $scope.url + '/' + $scope.inviteAuthorCode + '/facilitate/invite/handler');
		$http.get($scope.authorsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
				$scope.loading = false;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.authors = data.result;
				$scope.loading = false;
			}
		});
		$scope.userValue = ''
		$scope.users = ''
	}




}