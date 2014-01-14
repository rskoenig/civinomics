function initiativeCtrl($scope, $http, $location, $timeout) {
	$scope.testing = 'testing 2 4 3 1'
	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };

    $scope.resourcesURL = '/initiative/' + $scope.rurlCode + '/' + $scope.rurl + '/getResources';
    $scope.updatesURL = '/initiative/' + $scope.rurlCode + '/' + $scope.rurl + '/getUpdates';

    $scope.addUpdateTitleResponse='';
    $scope.addUpdateTextResponse='';
    $scope.addUpdateResponse=''; 
    $scope.updateCode = "new";

    if ($scope.thingType == "initiative"){
    	$scope.showingText = true;
	    $scope.showingResources = false;
	    $scope.showingUpdates = false;
	    $scope.showingChild = false;
	    $scope.showingAddResource = false;
	    $scope.showingAddUpdate = false;
    } else if ($scope.thingType == "resource"){
    	$scope.showingText = false;
	    $scope.showingResources = false;
	    $scope.showingUpdates = false;
	    $scope.showingChild = true
	    $scope.showingAddResource = false;
	    $scope.showingAddUpdate = false;
    }
    

    $scope.getResources = function() {
		$http.get($scope.resourcesURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
				//$scope.loading = false;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.resources = data.result;
				//$scope.loading = false;
			}
		});
	}

	$scope.getUpdates = function() {
		$http.get($scope.updatesURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
				//$scope.loading = false;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.updates = data.result;
				//$scope.loading = false;
			}
		});
	}

    $scope.showText = function(){
    	// http.get initiative text controller function
    	$scope.showingText = true;
    	$scope.showingResources = false;
    	$scope.showingUpdates = false;
    	$scope.showingChild = false;
    	$scope.showingAddResource = false;
    	$scope.showingAddUpdate = false;
    };

    $scope.showResources = function(){
    	$scope.getResources()
    	$scope.showingText = false;
    	$scope.showingResources = true;
    	$scope.showingUpdates = false;
    	$scope.showingChild = false;
    	$scope.showingAddResource = false;
    	$scope.showingAddUpdate = false;
    };

     $scope.showUpdates = function(){
    	$scope.getUpdates()
    	$scope.showingText = false;
    	$scope.showingResources = false;
    	$scope.showingUpdates = true;
    	$scope.showingChild = false;
    	$scope.showingAddResource = false;
    	$scope.showingAddUpdate = false;
    };

    $scope.showAddResource = function(){
    	$scope.showingText = false;
    	$scope.showingResources = false;
    	$scope.showingUpdates = false;
    	$scope.showingChild = false;
    	$scope.showingAddResource = true;
    	$scope.showingAddUpdate = false;
    };

    $scope.showAddUpdate = function(){
    	$scope.showingText = false;
    	$scope.showingResources = false;
    	$scope.showingUpdates = false;
    	$scope.showingChild = false;
    	$scope.showingAddResource = false;
    	$scope.showingAddUpdate = true;
    };


    // add a resource - copied from resource.js file
    $scope.addResourceTitleShow = false;
    $scope.addResourceURLShow = false;
    
    $scope.submitResourceForm = function(addResourceForm) {

        if(addResourceForm.title.$invalid) {
            $scope.addResourceTitleShow = true;
            $scope.addResourceTitleResponse =  "Title is required.";
        } else {
            $scope.addResourceTitleShow = false;
            $scope.addResourceTitleResponse =  "";  
        }
        if(addResourceForm.link.$invalid) {
            $scope.addResourceURLShow = true;
            $scope.addResourceURLResponse =  "A valid link URL is required.";
        } else {
            $scope.addResourceURLShow = false;
            $scope.addResourceURLResponse =  "";
        }
        if(addResourceForm.$valid) {
            $scope.addResourceShow = true;
            $scope.addResourceResponse = "Submitting resource...";
            var addURL = '/initiative/' + $scope.rurlCode + '/' + $scope.rURL + '/add/resource/handler';

            var postData = {'title':$scope.title, 'link': $scope.link, 'text': $scope.text};
            $http.post(addURL, postData).success(function(data){
                if(data.state == 'Error'){
                    $scope.addResourceShow = true;
                    $scope.addResourceResponse = data.errorMessage;
                } else {
                    var resourceCode = data.resourceCode;
                    var resourceURL = data.resourceURL;

                    var newResourceURL = '/' + $scope.rType + '/' + $scope.parentCode + '/' + $scope.parentURL + '/resource/' + resourceCode + '/' + resourceURL;
                    window.location = newResourceURL;
                }
            });
        }
        
    };



    // add a resource - copied from update.js file
    $scope.submitUpdateForm = function(addUpdateForm) {


        if(addUpdateForm.title.$invalid) {
            $scope.addUpdateTitleShow = true;
            $scope.addUpdateTitleResponse =  "Title is required.";
        } else {
            $scope.addUpdateTitleShow = false;
            $scope.addUpdateTitleResponse =  "";  
        }
        if(addUpdateForm.text.$invalid) {
            $scope.addUpdateTextShow = true;
            $scope.addUpdateTextResponse =  "Title is required.";
        } else {
            $scope.addUpdateTextShow = false;
            $scope.addUpdateTextResponse =  "";  
        }

        if(addUpdateForm.$valid) {
            $scope.addUpdateShow = true;
            $scope.addUpdateResponse = "Submitting progress report...";
            var addURL = '/initiative/' + $scope.rurlCode + '/' + $scope.rurl + '/updateEditHandler/' + $scope.updateCode;

            var postData = {'title':$scope.title, 'text': $scope.text};
            $http.post(addURL, postData).success(function(data){
                if(data.state == 'Error'){
                    $scope.addUpdateShow = true;
                    $scope.addUpdateResponse = data.errorMessage;
                } else {
                    var updateCode = data.updateCode;
                    var updateURL = data.updateURL;

                    var newUpdateURL = '/initiative/' + $scope.parentCode + '/' + $scope.parentURL + '/updateShow/' + updateCode;
                    window.location = newUpdateURL;
                }
            });
        }
        
    };

}
