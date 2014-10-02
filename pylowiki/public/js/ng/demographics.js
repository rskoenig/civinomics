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
            gender: ['Male', 'Female'],
            ethnicity: ['Caucasian','Hispanic', 'African american', 'Asian', 'Extraterrestrial'],
            education: ['None', 'A lot'],
            kids:['Yes', 'No'],
            house:['Yes', 'No'],
            income:['Millionaire', 'Multimillionaire'],
            language:['English','Spanish','Russian','Swahili']}
	}
	
	$scope.hasDemographics = false;
	
	$scope.updateList = function(){
    	console.log($scope.demographics.list);
    	
    	console.log($scope.demographics.list);
        var oldList = $scope.demographics.list;
        var listStr = "";
    	for(var i in oldList){
    	    if (oldList[i].name === 'language' && oldList[i].checked){
        	    listStr += 'language';
    	    }
            else if (oldList[i].checked){
                console.log("it's checked");
                listStr += oldList[i].name + "|";
            }
    	}
    	console.log(listStr);
	}
	
/*
	
	$scope.$watch('demographics.list',function(){
    	console.log("list changed");
    	
    	console.log($scope.demographics.list);
	});
*/

/*
	conditionalListToString = function(list){
        for(var demo in ){
            
        }
	};
*/
		
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
