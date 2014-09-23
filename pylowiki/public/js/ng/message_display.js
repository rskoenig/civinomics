function messageDisplayCtrl($scope, $http) {
    // '/workshop/' + $scope.code + '/' + $scope.url + '/ideas/get'
    //console.log('test read '+$scope.read);
    $scope.classUnread = '';

    
    $scope.updateReadStatus = function(initializing) {
        if ($scope.classUnread == 'warning unread-message') {
            $scope.classUnread = '';
            $.post('/message/' + $scope.messageCode + '/mark/read/').
                success(function(data) {
                    console.log(data);
                }).
                error(function(data) {
                    //console.log(data);
                    $scope.classUnread = 'warning unread-message';
                });
        } else if ($scope.read == '0' && initializing==true) {
            $scope.classUnread = 'warning unread-message';
        } else {
            $scope.classUnread = '';
        }
    }

    // note: turned this off while I test to see how facilitator invite works
    $scope.updateReadStatus(true);

    $scope.isRead= function(read) {
        if (read == '1') {
            return true;
        } else {
            return false;
        }
    }

    $scope.notRead = function(read) {
        if (read != '1') {
            return true;
        } else {
            return false;
        }
    }

}