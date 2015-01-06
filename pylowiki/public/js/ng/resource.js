
function resourceController($scope, $http, $location, $timeout) {
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
            var addURL = '/' + $scope.rType + '/' + $scope.parentCode + '/' + $scope.parentURL + '/add/resource/handler';

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

}
