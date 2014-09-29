function infoCtrl($scope){
	$scope.resourcesModule = '';
	$scope.imagesModule = '';
	$scope.infoModule = 'hidden';

	$scope.switchResources = function() {
		$scope.resourcesModule = 'hidden';
		$scope.imagesModule = '';
		$scope.infoModule = '';
	}
	$scope.switchInfo = function() {
		$scope.resourcesModule = '';
		$scope.imagesModule = '';
		$scope.infoModule = 'hidden';
	}
	$scope.switchImages = function() {
		$scope.resourcesModule = '';
		$scope.imagesModule = 'hidden';
		$scope.infoModule = '';
	}
};