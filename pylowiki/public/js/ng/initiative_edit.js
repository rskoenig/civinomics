function editInitiativeController($scope) {
	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };
}
