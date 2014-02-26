function messageDisplayCtrl($scope, $http) {
    // '/workshop/' + $scope.code + '/' + $scope.url + '/ideas/get'
    //console.log('test read '+$scope.read);
    $scope.classUnread = '';

    
    $scope.updateReadStatus = function() {
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
        } else if ($scope.read == '0') {
            $scope.classUnread = 'warning unread-message';
        } else {
            $scope.classUnread = '';
        }
    }

    $scope.updateReadStatus();

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