function demographicsController($scope, $http){

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
            language: 7
            },
        list : [
            {name: 'birthday', checked:false, text:'Birthday'},
            {name: 'gender', checked:false, text:'Gender'},
            {name: 'ethnicity', checked:false, text:'Ethnicity'},
            {name: 'education', checked:false, text:'Education Level'},
            {name: 'kids', checked:false, text:'Has Kids'},
            {name: 'house', checked:false, text:'Owns a House'},
            {name: 'income', checked:false, text:'Income Level'},
            {name: 'language', checked:false, text:'Native Language'} 
            ],
        values : [
            {name: 'birtday', type: 'date', text: 'Birthday', placeholder: 'YYYY-MM-DD', values : ''},
            {name: 'gender', type: 'radio', text: 'Gender', placeholder: '', values : ['Male', 'Female', 'Other']},
            {name: 'ethnicity', type: 'select', text: 'Ethnicity', placeholder: '', values : ['Caucasian','Hispanic', 'African american', 'Asian', 'Extraterrestrial', 'Other']},
            {name: 'education', type: 'select', text: 'Education Level', placeholder: '', values : ['None', 'A lot', 'Other']},
            {name: 'kids', type: 'radio', text: 'Do you have kids?', placeholder: '', values : ['Yes', 'No']},
            {name: 'house', type: 'radio', text: 'Do you own a house?', placeholder: '', values : ['Yes', 'No']},
            {name: 'income', type: 'select', text: 'Income level', placeholder: '', values : ['Millionaire', 'Multimillionaire']},
            {name: 'language', type: 'select', text: 'Native language', placeholder: '', values : ['English','Spanish','Russian','Swahili']}
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
    	language: "0"
	};
	
	$scope.hasDemographics = false;
	
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
				} 
				else if (data.statusCode === 0){
				    $scope.demographics.required = data.required.split("|");
				    $scope.hasDemographics = true;
				    return '0';
				    
					//Do something if it fails		
					//I'd rather do this			
				}
			});
       $scope.userDemoChecked = true;     
	};
	
	$scope.sendUserDemographics = function(workshopCode, workshopUrl){
	    var userData = $scope.userDemographics.birthday +"|"+$scope.userDemographics.gender+"|"+$scope.userDemographics.ethnicity+"|"+$scope.userDemographics.education+"|"+$scope.userDemographics.kids+"|"+$scope.userDemographics.house+"|"+$scope.userDemographics.income+"|"+$scope.userDemographics.language
        var requestUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/demographics/set/"+userData;
        $http.get(requestUrl).success(function(data){
				if (data.statusCode == 1){
				    return '1';
				} 
				else if (data.statusCode === 0){
				    return '0';	
				}
			});
        /* Fancy, but doesn't work
$http.post(requestUrl, $scope.userDemographics).success(function(data){
            console.log("success!!!");
            $scope.success = true
            $scope.newObjUrl = data.newObjUrl
            $scope.newObjCode = data.newObjCode
		});
*/

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
