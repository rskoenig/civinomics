function demographicsController($scope, $http){
    $scope.inDemographics = false;
	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.demographics = {
	    indexList : {
    	    birthday: 0,
            gender: 1,
            ethnicity: 2,
            education: 3,
            kids: 4,
            house: 5,
            income: 6,
            language: 7,
            residential: 8,
            multifamily: 9,
            peoplehousehold: 10
            },
        list : [
            {name: 'birthday', checked:false, text:'Birthday'},
            {name: 'gender', checked:false, text:'Gender'},
            {name: 'ethnicity', checked:false, text:'Ethnicity'},
            {name: 'education', checked:false, text:'Education Level'},
            {name: 'kids', checked:false, text:'Has Kids'},
            {name: 'house', checked:false, text:'Owns a House'},
            {name: 'income', checked:false, text:'Income Level'},
            {name: 'language', checked:false, text:'Native Language'},
            {name: 'residential', checked:false, text:'Residential or Commercial of the WSAC'}, 
            {name: 'multifamily', checked:false, text:'Single or Multifamily home'},
            {name: 'peoplehousehold', checked:false, text:'People in Household'} 
            ],
        values : [
            {name: 'birthday', type: 'date', text: 'What is your birth date?', placeholder: 'YYYY-MM-DD', values : ''},
            {name: 'gender', type: 'radio', text: 'What is your gender?', placeholder: '', values : ['Male', 'Female', 'Other']},
            {name: 'ethnicity', type: 'select', text: 'What is your ethnicity?', placeholder: '', values : ["White/Caucasian","Latino/Hispanic","African American", "Asian, or Pacific Islander", "Native American", "Mixed Race", "Other"]},
            {name: 'education', type: 'select', text: 'What is the highest education level you have completed?', placeholder: '', values : ["Some High School","High School Diploma/GED","Some College","Bachelor's or 4 year degree", "Post Graduate/Masters","PhD"]},
            {name: 'kids', type: 'radio', text: 'Do you have children?', placeholder: '', values : ['Yes', 'No']},
            {name: 'house', type: 'radio', text: 'Do you own or rent the house or apartment in which you live?', placeholder: '', values : ['Own', 'Rent']},
            {name: 'income', type: 'select', text: 'Estimate your annual household income.', placeholder: '', values : ["Under $10,000", "$10,000-$18,000","$18,000-$32,000","$32,000-$54,000","$54,000-$86,000","$86,000-$120,000","$120,000-$200,000","Over $200,000"]},
            {name: 'language', type: 'select', text: 'Native language', placeholder: '', values : ['English','Spanish','Russian','Other']},
            {name: 'residential', type: 'select', text: 'Are you a residential or commercial customer of the Santa Cruz Water Department?', placeholder: '', values : ["Residential","Commercial", "Both", "I am not a customer of the Santa Cruz Water Department"]},
            {name: 'multifamily', type: 'select', text: 'Do you live in a single family or multifamily home?', placeholder: '', values : ["Single Family", "Multifamily"]},
            {name: 'peoplehousehold', type: 'select', text: 'How many people live in your household?', placeholder: '', values : ['1','2','3','4','5','6','7','8','9','10']}
            ],
        required : ""
	}
	
	$scope.userDemographics = {
    	birthday: "0",
    	gender: "0",
    	ethnicity: "0",
    	education: "0",
    	kids: "0",
    	house: "0",
    	income: "0",
    	language: "0",
        residential: "0",
        multifamily: "0",
        peoplehousehold: "0",
        optout: "0",
	};
	
	$scope.hasDemographics = false;
	$scope.demographicsSent = false;
	$scope.userHasDemographics = false;
	$scope.closingDemoWindow = false;
	
	$scope.getDemographics = function(workshopCode, workshopUrl){
        var requestUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/demographics/get/";
        $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
				    $scope.hasDemographics = true;
				    var requiredDemo = data.required.split("|");
				    for (var i = 0; i < requiredDemo.length; i++){
    				    $scope.demographics.list[$scope.demographics.indexList[requiredDemo[i]]].checked = true;
				    };
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
					//Do something if it fails		
				}
			});
	};
	
	$scope.updateList = function(workshopCode, workshopUrl){        
	    var stringDemographicsList = conditionalListToString($scope.demographics.list);
	    var requestUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/demographics/add/"+stringDemographicsList;
        $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
				
					//Do something if they were added correctly (probably just update message or continue)
				} 
				else if (data.statusCode === 0){
					//Do something if it fails		
					//I'd rather do this			
				}
			});
	};
	
	$scope.userDemoChecked = false;
	
	$scope.checkDemographics = function(parentHref){
	    if ($scope.userDemoChecked) return;
    	var requestUrl = parentHref+"/demographics/check";
        $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
				    return '1';
				    $scope.userHasDemographics = true;
				} 
				else if (data.statusCode === 0){
				    $scope.demographics.required = data.required.split("|");
				    $scope.inDemographics = true;
				    $scope.hasDemographics = true;
				    return '0';
					//Do something if it fails		
					//I'd rather do this			
				}
			});
       $scope.userDemoChecked = true;     
	};
	
	$scope.sendUserDemographics = function(parentHref){
      $scope.inDemographics = false;
      $scope.hasVoted = false;
      var requestUrl = parentHref+"/demographics/set/";
      $http.post(requestUrl, $scope.userDemographics).success(function(data){
            $scope.demographicsSent = true;
            $scope.demographics.required = "";
            $scope.success = true
            $scope.newObjUrl = data.newObjUrl
            $scope.newObjCode = data.newObjCode
            
		});
	};
	
	$scope.changeClosingWindow = function(){
    	$scope.closingDemoWindow = !$scope.closingDemoWindow;
	};
	
	conditionalListToString = function(oldList){
        var listStr = "";
        var arrayAux = []
    	for(var i in oldList){
    	    if (oldList[i].checked){
                arrayAux.push(oldList[i].name);
            }
    	}
    	listStr = listToString(arrayAux);
    	return listStr;
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
	
};
