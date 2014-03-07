function profileMessagesCtrl($scope, $http) {
    // '/workshop/' + $scope.code + '/' + $scope.url + '/ideas/get'
    //$scope.messagesURL = '/messages/get/' + $scope.code + '/' + $scope.url
    //$scope.orderProp = '-date';
    //$scope.filterProp = '!disabled';
    //$scope.numAdopted = '0';
    //$scope.numMessages = '0';
    //$scope.messagesLoading = true;

    //$http.get($scope.messagesURL).success(function(data){
    //    $scope.messagesLoading = true;
    //    if (data.statusCode === 1){
    //        $scope.noResult = true;
    //        $scope.messagesLoading = false;
    //    }
    //    else if (data.statusCode === 2){
    //        $scope.noResult = true;
    //        $scope.messagesLoading = false;
    //    }
    //    else if (data.statusCode === 0){
    //        $scope.noResult = false;
    //        $scope.messages = data.result;
    //        $scope.numAdopted = data.adopted;
    //        $scope.numMessages = data.numMessages;
    //        $scope.messagesLoading = false;
    //    }
    //});

//}

    $scope.listingType = 'messages';
    $scope.messagesType = '/all';
    $scope.messagesLoading = true;
    $scope.messageSliceLoading = false;
    $scope.noMoreSlices = false;
    $scope.busy = false;
    $scope.sliceSize = 10;
    $scope.offset = $scope.sliceSize;

    $scope.getMessages = function() {
        $scope.alertMsg = ''
        $scope.messagesLoading = true;
        $http.get('/getMessages/' + $scope.code + '/' + $scope.url + '/' + $scope.messagesType).success(function(data){
            if (data.statusCode == 1){
                $scope.messagesNoResult = true;
                $scope.messages = []
                $scope.alertMsg = data.alertMsg;
                $scope.alertType = data.alertType;
            } 
            else if (data.statusCode === 0){
                $scope.messagesNoResult = false;
                $scope.noMoreSlices = false;
                $scope.messages = data.result;
                
            }
            $scope.messagesLoading = false;
        })
    };

    $scope.getMessages();


    $scope.getAllMessages = function(){
        $scope.messagesType = '/all';
        $scope.getMessages();
        $scope.offset = $scope.sliceSize;
    };

    $scope.getMessagesSlice = function() {
        if ($scope.busy || $scope.noMoreSlices) return;
        $scope.busy = true;
        $scope.alertMsg = ''
        $scope.messagesSliceLoading = true;
        $http.get('/getMessagesSlice/' + $scope.code + '/' + $scope.url + '/' + $scope.messagesType + '/' + $scope.offset).success(function(data){
            if (data.statusCode == 1){
                $scope.noMoreSlices = true;
            } 
            else if (data.statusCode === 0){
                activitySlice = data.result;
                for (var i = 0; i < messagesSlice.length; i++) {
                    $scope.messages.push(messagesSlice[i]);
                }
                $scope.noMoreSlices = false;
            }
            $scope.messagesSliceLoading = false;
            $scope.busy = false;
            $scope.offset += $scope.sliceSize;
        })
    };

}