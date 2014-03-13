
function topicController($scope, $http, $location, $timeout) {
    $scope.addTopicTitleShow = false;
    $scope.addTopicTextShow = false;
    
    $scope.submitTopicForm = function(addTopicForm) {


        if(addTopicForm.title.$invalid) {
            $scope.addTopicTitleShow = true;
            $scope.addTopicTitleResponse =  "Title is required.";
        } else {
            $scope.addTopicTitleShow = false;
            $scope.addTopicTitleResponse =  "";  
        }
        if(addUpdateForm.text.$invalid) {
            $scope.addTopicTextShow = true;
            $scope.addTopicTextResponse =  "Additional information is required.";
        } else {
            $scope.addTopicTextShow = false;
            $scope.addTopicTextResponse =  "";  
        }

        if(addTopicForm.$valid) {
            $scope.addUpdateShow = true;
            $scope.addUpdateResponse = "Submitting progress report...";
            var addURL = '/profile/' + $scope.userCode + '/' + $scope.userURL + '/add/discussion/handler/' + $scope.updateCode;

            var postData = {'title':$scope.title, 'text': $scope.text};
            $http.post(addURL, postData).success(function(data){
                if(data.state == 'Error'){
                    $scope.addTopicShow = true;
                    $scope.addTopicResponse = data.errorMessage;
                } else {
                    var topicCode = data.topicCode;
                    var topicURL = data.topicURL;

                    var newTopicURL = '/profile/' + $scope.userCode + '/' + $scope.userURL + '/discussion/show/' + topicCode;
                    window.location = newTopicURL;
                }
            });
        }
        
    };

}
