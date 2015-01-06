function leaderboardController ($scope, $http){

    $scope.leaderboard = {
        type: "initiatives",
        list: [],
        offset: 0,
        limit: 10,
        sortBy: ''
    };
    
    $scope.loading = true;
    $scope.sliceLoading = false;
    $scope.busy = false;
    
    $scope.firstSector = $scope.leaderboard.offset == 0;
    
    $scope.getLeaderboard = function(){
        if ($scope.busy) return;
        $scope.busy = true;
        var requestUrl = "leaderboard/"+$scope.leaderboard.type+"/"+$scope.leaderboard.offset;
        if ($scope.leaderboard.sortBy != ''){
            requestUrl += "/" + $scope.leaderboard.sortBy;
        }
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
				    console.log("Yes");
				    $scope.leaderboard.list = data.list;	
				    $scope.loading = false;
				    $scope.sliceLoading = false;
				    $scope.busy = false;
				};
			})
    };
    
    $scope.getSector = function(type){
        $scope.sliceLoading = true;
        console.log(type);
        console.log($scope.leaderboard.type);
        switch (type){
            case 'more':
                $scope.leaderboard.offset += $scope.leaderboard.limit;
                break;
            case 'less':
                $scope.leaderboard.offset -= $scope.leaderboard.limit;
                break;
        }
        
        if ($scope.leaderboard.offset > 0) {
            $scope.firstSector = false;
        } else if ($scope.leaderboard.offset == 0) {
            $scope.leaderboard.offset = 0;
            $scope.firstSector = true;
        };
        
        $scope.getLeaderboard();
    };
    
    $scope.changeSorting = function(sortBy){
        $scope.leaderboard.sortBy = sortBy;
        $scope.getLeaderboard();
    };
    
    $scope.$watch($scope.leaderboard.type, function(newValue){
     console.log($scope.leaderboard.type);   
    $scope.getLeaderboard();
    });
    
   
    
	/*
$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.rating = {
		type: 'default',
		criteriaList: []
	};
	
	$scope.rating.type = 'default';
	
	$scope.criteria = {
		name: "",
		value: 0	
	};

	$scope.descriptions = {
    	Effectiveness : "The expected decrease in demand OR increase in storage or supply related to this proposal.",
    	Practicability : "Cost, community and political support, regulatory considerations.",
    	'Environmental Benefits' : "Environmental consequences, considering energy intensity, and riverine, marine, and terrestrial benefits or impacts.",
    	'Local Economy Benefits' : "Potential to create sustainable local jobs in the planning, implementation, and support of the proposal."
	};
	
	$scope.hover1 = false;
	$scope.hover2 = false || $scope.hover1;
	$scope.hover3 = false || $scope.hover1 || $scope.hover2;
	$scope.hover4 = false || $scope.hover1 || $scope.hover2 || $scope.hover3;
	$scope.hover5 = false || $scope.hover1 || $scope.hover2 || $scope.hover3 || $scope.hover4;
	$scope.vote = 0;
	
	$scope.criteriaName = '';
	$scope.hasCriteria = false;
	$scope.showAverage = false;
	$scope.hasVoted = false;

	$scope.showRatingPanel = false;
	$scope.changeShowAverage = function(){
		if ($scope.showRatingPanel == true && $scope.showAverage == true) {
    		$scope.showRatingPanel = false;
    	} else{
    		$scope.showRatingPanel = true;
    	};
    	$scope.showAverage = true;
	}

	$scope.changeShowMyRatings = function(){
		if ($scope.showRatingPanel == true && $scope.showAverage == false) {
    		$scope.showRatingPanel = false;
    	} else{
    		$scope.showRatingPanel = true;
    	};
    	$scope.showAverage = false;
	}
	
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
	$scope.gettingCriteria = false;
	$scope.getCriteriaList = function(parentHref,thingCode){
	    if ($scope.gettingCriteria) return;
		if ($scope.hasCriteria) return;
		$scope.gettingCriteria = true;
		var requestUrl = parentHref+"/criteria/get/"+thingCode;
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					$scope.rating.type = 'criteria';
					$scope.rating.criteriaList = data.criteria;
					//Do something if they were added correctly (probably just update message or continue)
					$scope.checkRatingComplete()
				} 
				else if (data.statusCode === 0){
    				$scope.rating.type = 'yesno';			
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
    					$scope.alert.message = 'Criteria added correctly.';	
                    			$scope.alert.type = 'criteria';
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
			requestUrl = baseUrl + "0";
			$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					//Do something if they were added correctly (probably just update message or continue)
					$scope.alert.message = 'Rating set to yes/no.';	
                    			$scope.alert.type = 'yesno';
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
	
	$scope.initYesno = function(){
		$scope.rating.type = 'yesno';
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
    	$scope.hasVoted = true;
		$http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
					$scope.vote = criteria.amount;
					$scope.getCriteriaList(parentHref,thingCode);
					$scope.checkRatingComplete()
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

	$scope.checkRatingComplete = function() {
		$scope.ratingComplete = true;
		for (i = 0; i < $scope.rating.criteriaList.length; i++) { 
			if ($scope.rating.criteriaList[i]['amount'] == '0'){
				$scope.ratingComplete = false;
				break
			};
		}
		if ($scope.ratingComplete) {
			$scope.showAverage = true;
			$scope.rating.criteriaList[1].numVotes += 1;
		};

	};
*/
	
	
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
}