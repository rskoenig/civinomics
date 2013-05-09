function ProfileEditController($scope, $http) {
    $scope.fullNameRegex = /^([A-Za-z0-9-_\s])+$/;
    $scope.postalCodeRegex = /^\d*$/;
    $scope.submitStatus = '-1';
    
    $scope.submitProfileEdit = function(){
        var submitURL = location.pathname + "/info/edit/handler"
        var thisForm = {member_name:$scope.fullName, email:$scope.email, postalCode:$scope.postalCode, greetingMsg:$scope.greetingMsg, websiteLink:$scope.websiteLink, websiteDesc:$scope.websiteDesc};
        $http.post(submitURL, thisForm).success(function(data){
            var alertClass = 'alert-success';
            if(data.statusCode == '1') {
                alertClass = 'alert-error';
                $scope.submitStatus = 1;
            }
            $scope.submitStatus = 0;
            /*
            var alertHTML = '<div class="alert ' + alertClass + '"><button type="button" class="close" data-dismiss="alert">&times;</button>' + data.result + '</div>'
            document.getElementById("submitResult").innerText = document.getElementById("submitResult").textContent = '';
            document.getElementById("submitResult").innerHTML = alertHTML;
            window.history.replaceState('Object', 'Title', data.returnURL);
            */
            $scope.dashboardFullName = $scope.fullName;
            $scope.dashboardGreetingMsg = $scope.greetingMsg;
            $scope.dashboardWebsiteLink = $scope.websiteLink;
            $scope.dashboardWebsiteDesc = $scope.websiteDesc;
            if(data.statusCode == '2') {
                $scope.updateGeoLinks();
            }
      });
    }
    $scope.updateGeoLinks = function(){
        var submitURL = "/geo/cityStateCountryLink/" + $scope.postalCode
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
        
        
    }
};

