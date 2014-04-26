
function topicController($scope, $http, $location, $timeout) {
    $scope.addTopicTitleShow = false;
    $scope.addTopicTextShow = false;
    $scope.title = '';
    $scope.text = '';
    
    $scope.submitTopicForm = function(addTopicForm) {

        if(addTopicForm.title.$invalid) {
            $scope.addTopicTitleShow = true;
            $scope.addTopicTitleResponse =  "Title is required.";
        } else {
            $scope.addTopicTitleShow = false;
            $scope.addTopicTitleResponse =  "";  
        }
        if(addTopicForm.text.$invalid) {
            $scope.addTopicTextShow = true;
            $scope.addTopicTextResponse =  "Additional information is required.";
        } else {
            $scope.addTopicTextShow = false;
            $scope.addTopicTextResponse =  "";  
        }

        if(addTopicForm.$valid) {
            $scope.addTopicShow = true;
            $scope.addTopicResponse = "Submitting discussion topic...";
            var addURL = '/profile/' + $scope.userCode + '/' + $scope.userURL + '/add/discussion/handler/';

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
