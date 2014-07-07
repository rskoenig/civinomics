function createController($scope, $http) {

	$scope.createUrl = '/profile/' + $scope.authorCode + '/' + $scope.authorUrl + '/createInitiative';
	
	$scope.createNew = function() {
        var createData = {'submit':'submit', 'title': $scope.title, 'description': $scope.description, 'scope': $scope.scope, 'tags': $scope.tag, 'deadline': $scope.date};
		//$scope.newObjURL = '/add/' + $scope.objType + '/handler';
		$http.post($scope.createUrl, createData).success(function(data){
            $scope.success = true
            $scope.newObjUrl = data.newObjUrl
            $scope.newObjCode = data.newObjCode
		});
	}
	
	// Scope
	$scope.thing = "Thing"
	
	$scope.thingList = ['Initiative', 'Workshop']
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
        $http.get('/geo/stateListJSON/' + $scope.country).success(function(data){
            $scope.stateList = data.result;
            $scope.showStateSelect = true;
        });
	}
	
	$scope.getCountyList = function() {
        $http.get('/geo/countyListJSON/'+ $scope.country + '/' + $scope.state).success(function(data){
            $scope.countyList = data.result;
            $scope.showCountySelect = true;
        });
	}
	
	$scope.getCityList = function() {
        $http.get('/geo/cityListJSON/' + $scope.county + '/' + $scope.state + '/' + $scope.county).success(function(data){
            $scope.cityList = data.result;
            $scope.showCitySelect = true;
        });
	}
	
	$scope.getPostalList = function() {
        $http.get('/geo/postalListJSON/' + $scope.county + '/' + $scope.state + '/' + $scope.county + '/' + $scope.city).success(function(data){
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
	
	// Date picker
	
    $scope.clear = function () {
        $scope.date = null;
    };
    
    
    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
    
        $scope.opened = true;
    };
    
    $scope.dateOptions = {
        'year-format': "'yy'",
        'starting-day': 1
    };
    
    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'shortDate'];
    $scope.format = $scope.formats[0];

}