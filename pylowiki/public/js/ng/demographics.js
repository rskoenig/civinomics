function demograpController($scope, $http){

	$scope.alert = {
		message : '',
		type: ''
	};
	
	$scope.demographics = {
        list : [
            {name: 'birthday', checked:false, text:'Birthday'},
            {name: 'gender', checked:false, text:'Gender'},
            {name: 'ethnicity', checked:false, text:'Ethnicity'},
            {name: 'education', checked:false, text:'Education Level'},
            {name: 'kids', checked:false, text:'Has Kids'},
            {name: 'house', checked:false, text:'Owns a House'},
            {name: 'income', checked:false, text:'Income Level'},
            {name: 'language', checked:false, text:'Native Language'} ],
        values : {
            birthday : '',
            gender: ['Male', 'Female', 'Other'],
            ethnicity: ['Caucasian','Hispanic', 'African american', 'Asian', 'Extraterrestrial', 'Other'],
            education: ['None', 'A lot', 'Other'],
            kids:['Yes', 'No'],
            house:['Yes', 'No'],
            income:['Millionaire', 'Multimillionaire'],
            language:['English','Spanish','Russian','Swahili']}
	}
	
	$scope.hasDemographics = false;
	
	$scope.updateList = function(workshopCode, workshopUrl){        
	    var stringDemographicsList = conditionalListToString($scope.demographics.list);
	    
	    var requestUrl = "/workshop/"+workshopCode+"/"+workshopUrl+"/demographics/add/"+stringDemographicsList;
        console.log(stringDemographicsList);
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
	
	$scope.checkDemographics = function(){
    	
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
    	console.log(listStr);
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
