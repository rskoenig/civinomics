function userLookupCtrl($scope, $http) {
	$scope.test = "testing testing 3 2 1 4";
	// loading removed until asynchronous calls between coAuthor add/remove and coAuthor list generation are implemented
	// messages will have to work for time being
	//$scope.loading = true;
	$scope.authorsURL = '/initiative/' + $scope.urlCode + '/' + $scope.url + '/getAuthors';
	$scope.userValue = '';
	$scope.alertMsg = '';
	$scope.hidden = 'show'
	$scope.userLookupURL = '/search/people/name/' + $scope.userValue;

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

	$scope.getAuthors = function() {
		$http.get($scope.authorsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
				//$scope.loading = false;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.authors = data.result;
				//$scope.loading = false;
			}
		});
	}
	$scope.getAuthors()

	$scope.removeCoA = function(removeAuthorCode) {
		//$scope.loading = true;
		$scope.removeAuthorCode = removeAuthorCode;
		$http.get('/initiative/' + $scope.urlCode + '/' + $scope.url + '/' + $scope.removeAuthorCode + '/facilitate/resign/handler').success(function(data){
			if (data.statusCode == 0){
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
				$scope.hidden = 'show';
			}
		});
		$scope.getAuthors()
	}

	$scope.submitInvite = function(inviteAuthorCode){
		$scope.loading = true;
		$scope.inviteAuthorCode = inviteAuthorCode;
		$http.get('/initiative/' + $scope.urlCode + '/' + $scope.url + '/' + $scope.inviteAuthorCode + '/facilitate/invite/handler').success(function(data){
			if (data.statusCode == 0){
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
				$scope.hidden = 'show';
			}
		});
		$scope.getAuthors()
		$scope.userValue = ''
		$scope.users = ''
	}

	$scope.hideShow = function(){
		if ($scope.hidden == 'hidden'){
			$scope.hidden = 'show';
		}
		else if ($scope.hidden == 'show'){
			$scope.hidden = 'hidden';
		}
	}

}