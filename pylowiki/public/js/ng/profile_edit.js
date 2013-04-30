function ProfileEditController($scope, $http) {
    $scope.fullNameRegex = /^([A-Za-z0-9-_\s])+$/;
    $scope.postalCodeRegex = /^\d*$/;
    
    $scope.submitProfileEdit = function(){
        var submitURL = location.pathname + "/info/edit/handler"
        var thisForm = {member_name:$scope.fullName, email:$scope.email, postalCode:$scope.postalCode, greetingMsg:$scope.greetingMsg, websiteLink:$scope.websiteLink, websiteDesc:$scope.websiteDesc};
        $http.post(submitURL, thisForm).success(function(data){
            document.getElementById("submitResult").innerText = document.getElementById("submitResult").textContent = '';
            document.getElementById("submitResult").innerText = document.getElementById("submitResult").textContent = data.result;
            if(data.statusCode == '2'){
                location.pathname = data.returnURL;
            }
      });
    }
};

