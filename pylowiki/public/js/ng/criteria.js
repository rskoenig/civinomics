var app = angular.module('civ');

app.controller('ratingsController', function($scope, $http){

	$scope.rating = {
		type: '',
		criteriaList: []
	};
	
	$scope.criteriaName = '';
	
	$scope.addCriteriaToList = function(){
		console.log($scope.rating.criteriaList.indexOf($scope.criteriaName));
		console.log(!($scope.rating.criteriaList.indexOf($scope.criteriaName)>-1));
		console.log(!$scope.rating.criteriaList.indexOf($scope.criteriaName)>-1);
		if(!($scope.rating.criteriaList.indexOf($scope.criteriaName)>-1)){
		
			$scope.rating.criteriaList.push($scope.criteriaName);
			$scope.criteriaName = '';	
		};
	};
	
	$scope.deleteCriteriaFromList = function (criteria){
		
	};
	
	$scope.sendCriteriaList = function (){
		
	};
  /*
	  Things that I need for this controller:
	  	Adding a criteria
	  		Adding to an array
	  	Removing a criteria
	  		Removing from the array
	  	Sending the criteria to the workshop
	  		Array to string with pipes
	  			Custom cast?
	  		Getting the workshop code
	  			URL split? Mako injection?
	  		Do I really need a criteria controller then?
	  		Are they ever gonna be separated from workshops?
	  			Not for now.
	  		
	  	In the future, there will need to be also functions to retrieve current criteria and display them properly (for ideas and the likes) so we might need an independent controller.
  */
});
