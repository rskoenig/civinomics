var app2 = angular.module('civ', []).controller('tagsController', ['$scope', '$http', function($scope, $http){
    console.log("a wee");
	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.subcategories = {
		type: 'tags',
		tagsList: []
	};
	
	$scope.subcategories.type = 'tags';
	
	$scope.tags = {
		name: "",
		value: 0	
	};
	
	$scope.tagsName = '';
	
	$scope.addTagsToList = function(){
		$scope.alert.message = '';
		if (!($scope.subcategories.tagsList.indexOf($scope.tagsName)>-1)) {
			$scope.subcategories.tagsList.push($scope.tagsName);
			$scope.tagsName = '';	
		} else {
			$scope.alert.message = 'You already added that tag.';	
			$scope.alert.type = 'tags'
		};
	};
	
	$scope.deleteTagsFromList = function (tags){
		var deleteTags = $scope.subcategories.tagsList.indexOf(tags);
		if (deleteTags > -1) {
			$scope.subcategories.tagsList.splice(deleteTags, 1);
		}
	};
	
	$scope.gettingTags = false;
	$scope.getTagsList = function(parentHref,thingCode){
	    if ($scope.gettingTags) return;
		if ($scope.hasTags) return;
		$scope.gettingTags = true;
		var requestUrl = parentHref+"/tags/get/"+thingCode;
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					$scope.subcategories.type = 'tags';
					$scope.subcategories.tagsList = data.tags;
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
    				$scope.subcategories.type = 'yesno';			
				}
				$scope.hasTags = true;
			})
	};
	
	$scope.sendTagsList = function(workshopCode, workshopUrl){
        	$scope.alert.type = '';
		$scope.alert.message = '';
		var baseUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/tags/add/";
		if ($scope.subcategories.tagsList.length > 0 ) { //Make this a switch block?
			var tags = listToString($scope.subcategories.tagsList);	
			requestUrl = baseUrl + tags;
		    $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
    					$scope.alert.message = 'Tag added correctly.';	
                    			$scope.alert.type = 'tags';
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
					//Do something if it fails					
				}
			})
		} else if ($scope.subcategories.tagsList.length == 0) {
			$scope.alert.type = 'error';
			$scope.alert.message = "Please add tags to continue.";
		} else { //This case needs to be fixed
			$scope.alert.type = 'error';
			$scope.alert.message = "You shouldn't see this at all.";
		};
	};
	
	$scope.initTags = function(tagsString){
		$scope.subcategories.type = 'tags';
		$scope.subcategories.tagsList = tagsString.split("|");
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
	  	Adding a tags
	  		Adding to an array
	  	Removing a tags
	  		Removing from the array
	  	Sending the tags to the workshop
	  		Array to string with pipes
	  			Custom cast? Yup
	  		Getting the workshop code
	  			URL split? no Mako injection? yes
	  		Do I really need a tags controller then?
	  		   YUP
	  		Are they ever gonna be separated from workshops?
	  			Not for now.
	  		
	  	In the future, there will need to be also functions to retrieve current tags and display them properly (for ideas and the likes) so we might need an independent controller.
  */
}]);


function tagsController($scope, $http){
	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.subcategories = {
		type: 'tags',
		tagsList: []
	};
	
	$scope.subcategories.type = 'tags';
	
	$scope.tags = {
		name: "",
		value: 0	
	};
	
	$scope.tagsName = '';
	
	$scope.addTagsToList = function(){
		$scope.alert.message = '';
		if (!($scope.subcategories.tagsList.indexOf($scope.tagsName)>-1)) {
			$scope.subcategories.tagsList.push($scope.tagsName);
			$scope.tagsName = '';	
		} else {
			$scope.alert.message = 'You already added that tag.';	
			$scope.alert.type = 'tags'
		};
	};
	
	$scope.deleteTagsFromList = function (tags){
		var deleteTags = $scope.subcategories.tagsList.indexOf(tags);
		if (deleteTags > -1) {
			$scope.subcategories.tagsList.splice(deleteTags, 1);
		}
	};
	
	$scope.gettingTags = false;
	$scope.getTagsList = function(parentHref,thingCode){
	    if ($scope.gettingTags) return;
		if ($scope.hasTags) return;
		$scope.gettingTags = true;
		var requestUrl = parentHref+"/tags/get/"+thingCode;
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					$scope.subcategories.type = 'tags';
					$scope.subcategories.tagsList = data.tags;
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
    				$scope.subcategories.type = 'yesno';			
				}
				$scope.hasTags = true;
			})
	};
	
	$scope.sendTagsList = function(workshopCode, workshopUrl){
        	$scope.alert.type = '';
		$scope.alert.message = '';
		var baseUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/tags/add/";
		if ($scope.subcategories.tagsList.length > 0 ) { //Make this a switch block?
			var tags = listToString($scope.subcategories.tagsList);	
			requestUrl = baseUrl + tags;
		    $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
    					$scope.alert.message = data.alertMsg;	
                        $scope.alert.type = data.alertType;
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
					//Do something if it fails					
				}
			})
		} else if ($scope.subcategories.tagsList.length == 0) {
			$scope.alert.type = 'error';
			$scope.alert.message = "Please add tags to continue.";
		} else { //This case needs to be fixed
			$scope.alert.type = 'error';
			$scope.alert.message = "You shouldn't see this at all. Like seriously, what did you do?";
		};
	};
	
	$scope.initTags = function(tagsString){
		$scope.subcategories.type = 'tags';
		$scope.subcategories.tagsList = tagsString.split("|");
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
	  	Adding a tags
	  		Adding to an array
	  	Removing a tags
	  		Removing from the array
	  	Sending the tags to the workshop
	  		Array to string with pipes
	  			Custom cast? Yup
	  		Getting the workshop code
	  			URL split? no Mako injection? yes
	  		Do I really need a tags controller then?
	  		   YUP
	  		Are they ever gonna be separated from workshops?
	  			Not for now.
	  		
	  	In the future, there will need to be also functions to retrieve current tags and display them properly (for ideas and the likes) so we might need an independent controller.
  */
};