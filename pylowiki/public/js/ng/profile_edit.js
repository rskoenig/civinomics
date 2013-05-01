function ProfileEditController($scope, $http) {
    $scope.fullNameRegex = /^([A-Za-z0-9-_\s])+$/;
    $scope.postalCodeRegex = /^\d*$/;
    
    $scope.submitProfileEdit = function(){
        var submitURL = location.pathname + "/info/edit/handler"
        var thisForm = {member_name:$scope.fullName, email:$scope.email, postalCode:$scope.postalCode, greetingMsg:$scope.greetingMsg, websiteLink:$scope.websiteLink, websiteDesc:$scope.websiteDesc};
        $http.post(submitURL, thisForm).success(function(data){
            var alertClass = 'alert-success';
            if(data.statusCode == '1') {
                alertClass = 'alert-error';   
            }
            var alertHTML = '<div class="alert ' + alertClass + '"><button type="button" class="close" data-dismiss="alert">&times;</button>' + data.result + '</div>'
            document.getElementById("submitResult").innerText = document.getElementById("submitResult").textContent = '';
            document.getElementById("submitResult").innerHTML = alertHTML;
            if(data.statusCode == '2'){
                location.hash = 'tab-edit'
                location.pathname = data.returnURL;
            }
      });
    }
};

