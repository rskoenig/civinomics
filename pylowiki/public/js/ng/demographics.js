function demograpController($scope, $http){

	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.hasDemographics = false;
		
	listToString = function(list){
		var i = 0;
		var listStr = "";
		while ( i < list.length-1) {
			listStr += list[i] + "|";
			i++;	
		}
		listStr += list[i];
		return listStr;
	};
	
};
