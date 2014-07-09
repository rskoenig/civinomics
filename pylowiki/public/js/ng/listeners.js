
function listenerController($scope, $http, $location) {
    $scope.addListenerShow     = false;
    $scope.disableListenerShow     = false;
    $scope.emailListenerShow     = false;
    
    $scope.listeners = [];
      
    $scope.getList = function() {
        var listURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/list/handler';
        $http.get(listURL).success(function(data){
            $scope.listeners = data.listeners
        });
    };
    $scope.saveListener = function() {
        var addURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/add/handler';
        var postData = {'userCode':$scope.user, 'lName': $scope.lName, 'lTitle': $scope.lTitle, 'lEmail': $scope.lEmail};
        $http.post(addURL, postData).success(function(data){
            $scope.addListenerShow = true;
            if(data.state == 'Error'){
                $scope.addListenerResponse = data.errorMessage;
            } else {
                $scope.addListenerResponse = 'Listener Added.';
                var newListeners = [];
                newListeners.push(data);
                for (var i = 0; i < $scope.listeners.length; i++) {
                    newListeners.push($scope.listeners[i]);
                }
                $scope.listeners = newListeners;
            }
            $scope.lName = '';
            $scope.lTitle = '';
            $scope.lEmail = '';
            
        });
    };
    $scope.editListener = function(urlCode) {
        var editURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/edit/handler';
        var formName = 'editForm' + urlCode;
        var form = document.getElementById(formName);
        var lName = form.lName.value;
        var lTitle = form.lTitle.value;
        var lEmail = form.lEmail.value;
        var nameSpanLabel = 'listenerName' + urlCode;
        var titleSpanLabel = 'listenerTitle' + urlCode;
        var responseName = 'editListenerResponse' + urlCode;
        var response = document.getElementById(responseName);
        response.innerHTML = '';
        var postData = {'userCode':$scope.user, 'urlCode': urlCode, 'lName': lName, 'lTitle': lTitle, 'lEmail': lEmail};
        $http.post(editURL, postData).success(function(data){
            $scope.editListenerShow = true;
            $scope.editListenerResponse = data;
            document.getElementById(nameSpanLabel).innerHTML = '';
            document.getElementById(nameSpanLabel).innerHTML = lName;
            document.getElementById(titleSpanLabel).innerHTML = '';
            document.getElementById(titleSpanLabel).innerHTML = lTitle;
            response.innerHTML = 'Changes saved.';
        });
    };
    
    $scope.toggleListener = function(urlCode, toggleState) {
        var reasonName = 'lReason' + urlCode
        var responseName = 'toggleListenerResponse' + urlCode
        var lReason = document.getElementById(reasonName).value;
        var toggleURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/toggle/handler';

        var postData = {'urlCode':urlCode, 'lReason':lReason, 'toggleState':toggleState};
        $http.post(toggleURL, postData).success(function(data){
            $scope.toggleListenerShow = true;
            $scope.toggleListenerResponse = data;
            document.getElementById(reasonName).value  = '';
            document.getElementById(responseName).innerHTML  = data;
            $scope.getList();
        });

    };
    $scope.emailListener = function() {
        var emailURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/email/handler';
        var postData = {'urlCode':$scope.listener, 'memberMessage':$scope.memberMessage};
        $http.post(emailURL, postData).success(function(data){
            $scope.emailListenerShow = true;
            $scope.emailListenerResponse = data;
        });
    };
    $scope.suggestListener = function() {
        var suggestURL = '/workshop/' + $scope.code + '/' + $scope.url + '/listener/' + $scope.user + '/suggest/handler';
        var postData = {'suggestListener':$scope.suggestListenerText};
        $http.post(suggestURL, postData).success(function(data){
            $scope.suggestListenerText = "";
            $scope.suggestListenerShow = true;
            $scope.suggestListenerResponse = data;
        });
    };
}
  