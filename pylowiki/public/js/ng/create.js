function createController($scope, $http) {

	$scope.createUrl = '/profile/' + $scope.authorCode + '/' + $scope.authorUrl + '/createInitiative';
	
	$scope.createNew = function() {
        var createData = {'submit':'submit', 'title': $scope.title, 'description': $scope.description, 'scope': $scope.scope, 'tags': $scope.tag};
		//$scope.newObjURL = '/add/' + $scope.objType + '/handler';
		$http.post($scope.createUrl, createData).success(function(data){
            $scope.success = true
            $scope.newObjUrl = data.newObjUrl
            $scope.newObjCode = data.newObjCode
		});
	}
	
	// Scope
    $scope.planet = "0"
	$scope.country = "united-states"
	$scope.state = "0"
	$scope.county = "0"
	$scope.city = "0"
	$scope.postal = "0"
	
	$scope.updateScope = function(){
        $scope.scope = '0|0|' + $scope.country + '|0|' + $scope.state + '|0|' + $scope.county + '|0|' + $scope.city + '|0|' + $scope.postal;
        $scope.scope = $scope.scope.toLowerCase().replace(/ /g, '-')
	}
	
	$scope.getStateList = function() {
        $http.get('/geo/stateList/' + $scope.country).success(function(data){
            $scope.stateList = data.result;
            $scope.showStateSelect = true;
        });
	}
	
	$scope.getCountyList = function() {
        $http.get('/geo/countyList/'+ $scope.country + '/' + $scope.state).success(function(data){
            $scope.countyList = data.result;
            $scope.showCountySelect = true;
        });
	}
	
	$scope.getCityList = function() {
        $http.get('/geo/cityList/' + $scope.county + '/' + $scope.state + '/' + $scope.county).success(function(data){
            $scope.cityList = data.result;
            $scope.showCitySelect = true;
        });
	}
	
	$scope.getPostalList = function() {
        $http.get('/geo/postalList/' + $scope.county + '/' + $scope.state + '/' + $scope.county + '/' + $scope.city).success(function(data){
            $scope.postalList = data.result;
            $scope.showPostalSelect = true;
        });
	}
	
	$scope.changeStateList = function(){
        $scope.showCountySelect = false;
        $scope.updateScope();
        $scope.getStateList();
        $scope.county = '0'
        $scope.city = '0'
        $scope.postal = '0'
	};
	
	$scope.changeCountyList = function(){
        $scope.showCountySelect = false;
        $scope.updateScope();
        $scope.getCountyList();
        $scope.county = '0'
        $scope.city = '0'
        $scope.postal = '0'
	};
	
	$scope.changeCityList = function(){
        $scope.showCitySelect = false;
        $scope.updateScope();
        $scope.getCityList();
        $scope.city = '0'
        $scope.postal = '0'
	};
	
	$scope.changePostalList = function(){
        $scope.showPostalSelect = false;
        $scope.updateScope();
        $scope.getPostalList();
        $scope.postal = '0'
	};
	
	$scope.getStateList();
	$scope.showStateSelect = true;
	$scope.showCountySelect = false;
	$scope.showCitySelect = false;
	$scope.showPostalSelect = false;

}