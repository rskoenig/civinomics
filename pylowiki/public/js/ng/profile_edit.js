function profileController($scope, $http) {
    /*
    * submitStatus: 0   ->  Successfully submitted, like with Unix status codes
    *               1   ->  Error
    *               -1  ->  Not yet submitted
    */
    $scope.fullNameRegex = /^([A-Za-z0-9-_\s])+$/;
    $scope.postalCodeRegex = /^\d*$/;
    $scope.submitStatus = '-1';
    
    $scope.submitProfileEdit = function(){
        if (!$scope.infoEdit.$dirty){
            return false;
        }
        var submitURL = location.pathname + "/info/handler";
        var thisForm = {member_name:$scope.fullName, email:$scope.email, postalCode:$scope.postalCode, greetingMsg:$scope.greetingMsg, websiteLink:$scope.websiteLink, websiteDesc:$scope.websiteDesc};
        $http.post(submitURL, thisForm).success(function(data){
            var alertClass = 'alert-success';
            if(data.statusCode == '1') {
                alertClass = 'alert-error';
                $scope.submitStatus = 1;
            }
            else{
                $scope.submitStatus = 0;
            }
            $scope.dashboardFullName = $scope.fullName;
            $scope.dashboardGreetingMsg = $scope.greetingMsg;
            $scope.dashboardWebsiteLink = $scope.websiteLink;
            $scope.dashboardWebsiteDesc = $scope.websiteDesc;
            if(data.statusCode == '2') {
                $scope.updateGeoLinks();
            }
      });
    };
    $scope.updateGeoLinks = function(){
        var submitURL = "/geo/cityStateCountryLink/" + $scope.postalCode;
        $http.get(submitURL).success(function(data){
            if(data.statusCode == '0'){
                $scope.cityTitle = data.cityTitle;
                $scope.cityURL = data.cityURL;
                $scope.stateTitle = data.stateTitle;
                $scope.stateURL = data.stateURL;
                $scope.countryTitle = data.countryTitle;
                $scope.countryURL = data.countryURL;
            }
      });
    };

    $scope.emailOnComments = function() {
        $scope.emailOnCommentsShow     = false;
        var addedURL = '/profile/preferences/' + $scope.code + '/' + $scope.url + '/comments/handler';
        var postData = {'user':$scope.userCode, 'alert':'comments'};
        $http.post(addedURL, postData).success(function(data){
            $scope.emailOnCommentsShow = true;
            $scope.emailOnCommentsResponse = data;
        });
    }
    
    
    $scope.getActivityURL = '/getActivity/' + $scope.code + '/' + $scope.url;
    $scope.getTrashURL = '/getTrash/' + $scope.code + '/' + $scope.url;
    $scope.getMeetingsURL = '/getMeetings/' + $scope.code + '/' + $scope.url;
    $scope.getElectionsURL = '/getElections/' + $scope.code + '/' + $scope.url;
    $scope.getBallotsURL = '/getBallots/' + $scope.code + '/' + $scope.url;
    if ($scope.trash){
        $scope.getActivityURL = $scope.getTrashURL;
    }
    if ($scope.meetings){
        $scope.getActivityURL = $scope.getMeetingsURL;
    }
    if ($scope.ballots){
        $scope.getActivityURL = $scope.getBallotsURL;
    }
    if ($scope.elections){
        $scope.getActivityURL = $scope.getElectionsURL;
    }

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
