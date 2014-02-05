
function updateController($scope, $http, $location, $timeout) {
    $scope.addUpdateTitleShow = false;
    $scope.addUpdateTextShow = false;
    
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
            var addURL = '/initiative/' + $scope.parentCode + '/' + $scope.parentURL + '/updateEditHandler/' + $scope.updateCode;

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
