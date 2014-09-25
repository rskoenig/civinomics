var app = angular.module('civ');

app.controller('ratingsController', function($scope, $http){

	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.rating = {
		type: '',
		criteriaList: []
	};
	
	$scope.criteriaName = '';
	
	$scope.addCriteriaToList = function(){
		$scope.alert.message = '';
		if (!($scope.rating.criteriaList.indexOf($scope.criteriaName)>-1)) {
			$scope.rating.criteriaList.push($scope.criteriaName);
			$scope.criteriaName = '';	
		} else {
			$scope.alert.message = 'You already added that criteria.';	
			$scope.alert.type = 'criteria'
		};
	};
	
	$scope.deleteCriteriaFromList = function (criteria){
		var deleteCriteria = $scope.rating.criteriaList.indexOf(criteria);
		if (deleteCriteria > -1) {
			$scope.rating.criteriaList.splice(deleteCriteria, 1);
		}
	};
	
	$scope.sendCriteriaList = function(workshopCode, workshopUrl){
		console.log($scope.rating.type);
		$scope.alert.type = '';
		$scope.alert.message = '';
		var baseUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/criteria/add/";
		if ($scope.rating.type === "criteria" && $scope.rating.criteriaList.length > 0 ) {
			var criteria = listToString($scope.rating.criteriaList);	
			requestUrl = baseUrl + criteria;
		    $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
					//Do something if it fails					
				}
			})
		} else if ($scope.rating.type === "criteria" && $scope.rating.criteriaList.length == 0) {
			$scope.alert.type = 'error';
			$scope.alert.message = "Please add criteria to continue or choose a 'Yes/No' rating.";
		} else if ($scope.rating.type === "yesno"){
			//Logic for uploading a yesno
			console.log("I'm here");
			requestUrl = baseUrl + "0";
			console.log(requestUrl);
			$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
					//Do something if it fails					
				}
				$scope.activityLoading = false;
			})
			
		} else {
			$scope.alert.type = 'error';
			$scope.alert.message = "Please choose a type of Rating.";
		};
	};
	
	listToString = function(list){
		var i = 0;
		var listStr = "";
		while ( i < list.length-1) {
			listStr += list[i] + "|";
			i++;	
		}
		listStr += list[i];
		return listStr;
	}

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
