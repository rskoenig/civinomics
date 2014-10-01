var app = angular.module('civ');

app.controller('demographicsController', function($scope, $http){

	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.rating = {
		type: '',
		criteriaList: []
	};
	
	$scope.criteriaName = '';
	$scope.hasCriteria = false;
	
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
	
	$scope.getCriteriaList = function(parentHref,thingCode){
		if ($scope.hasCriteria) return;
		var requestUrl = parentHref+"/criteria/get/"+thingCode;
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					$scope.rating.type = 'criteria';
					$scope.rating.criteriaList = data.criteria;
					console.log($scope.rating.criteriaList);
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
    				console.log($scope.rating.criteriaList);
					return false;				
				}
				$scope.hasCriteria = true;
			})
	};
	
	$scope.sendCriteriaList = function(workshopCode, workshopUrl){
        $scope.alert.type = '';
		$scope.alert.message = '';
		var baseUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/criteria/add/";
		if ($scope.rating.type === "criteria" && $scope.rating.criteriaList.length > 0 ) { //Make this a switch block?
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
			
		} else { //This case needs to be fixed
			$scope.alert.type = 'error';
			$scope.alert.message = "Please choose a type of Rating.";
		};
	};
	
	$scope.initCriteria = function(criteriaString){
		$scope.rating.type = 'criteria';
		$scope.rating.criteriaList = criteriaString.split("|");
	};
	
	$scope.addVote = function(hover, amount, criteria){
    	hover = !hover;
    	$scope.vote = criteria.amount; 
    	criteria.amount = amount;
	};
	
	$scope.removeVote = function(hover, criteria){
        hover = !hover;	
        criteria.amount = $scope.vote;
	};
	
	$scope.rateCriteria = function(parentHref, thingCode, criteria){
    	var requestUrl = parentHref+"/criteria/rate/"+thingCode+"/"+criteria.criteria+"/"+criteria.amount;
    	$scope.vote = criteria.amount;
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					$scope.vote = criteria.amount;
				} 
				else if (data.statusCode === 0){			
				}
        })
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
	};
	
	
  /*
	  Things that I need for this controller:
	  	Adding a criteria
	  		Adding to an array
	  	Removing a criteria
	  		Removing from the array
	  	Sending the criteria to the workshop
	  		Array to string with pipes
	  			Custom cast? Yup
	  		Getting the workshop code
	  			URL split? no Mako injection? yes
	  		Do I really need a criteria controller then?
	  		   YUP
	  		Are they ever gonna be separated from workshops?
	  			Not for now.
	  		
	  	In the future, there will need to be also functions to retrieve current criteria and display them properly (for ideas and the likes) so we might need an independent controller.
  */
});
