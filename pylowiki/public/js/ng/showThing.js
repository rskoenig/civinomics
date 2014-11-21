function showThingCtrl($scope, $http, $location, $anchorScroll, $window) {
	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };
    
    $scope.scrollTo = function(id) {
      $location.hash(id);
      $anchorScroll();
   	}

   	$scope.location = $location.absUrl()
   	// need to get to the bottom of why angular is injecting a '/' at the end of the url this hack works in the meantime...
	var splitLocation = $scope.location.split("#")
	if (splitLocation.length > 1) {
		$scope.hash = splitLocation[1]
		$scope.hash = $scope.hash.replace('/', '')
		$scope.scrollTo($scope.hash)
	};

	$scope.$watch(function(){
       return $window.innerWidth;
    }, function(value) {
       $scope.windowSize = value;
       if(value >= 768){
    		$scope.xs = false;
    	} else{
    		$scope.xs = true;
    	};
   });

	$(window).resize(function(){
    	if(window.innerWidth >= 768){
    		$scope.xs = false;
    	} else{
    		$scope.xs = true;
    	};

	    $scope.$apply(function(){
	       console.log('window resizing')
	       console.log($scope.xs)
	       console.log(window.innerWidth)
	    });
	});


    $scope.getUrl = '/' + $scope.objType + '/' + $scope.thingCode + '/' + $scope.thingUrl + '/json';

    $scope.getThingData = function(){
    	$http.get($scope.getUrl).success(function(data){
			if (data.statusCode === 0){
				$scope.noResult = true;
			}
			else if (data.statusCode == 1){
				$scope.noResult = false;
				$scope.item = data.thing;

				$scope.summary = $scope.item.text;
				if ($scope.summary) {
					$scope.getWordCount()
				};
				$scope.urlCode= $scope.item.urlCode;
				$scope.url= $scope.item.url;
				$scope.totalVotes= $scope.item.voteCount;
				$scope.yesVotes= $scope.item.ups;
				$scope.noVotes= $scope.item.downs;
				$scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
        		$scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
				$scope.objType= $scope.item.objType;
				$scope.rated= $scope.item.rated;
				$scope.goal= $scope.item.goal;
				if ($scope.rated == 0) {
			        $scope.voted = '';
			    }
			    else if ($scope.rated == 1){
			        $scope.voted = 'yesVoted';
			    }
			    else if ($scope.rated == -1){
			        $scope.voted = 'noVoted';
			    }

			}
			$scope.loading = false;
		});
    };

    $scope.getThingData();

    if ($scope.summary) {
		$scope.wordCount = $scope.summary.trim().split(/\s+/).length;
   	};
	$scope.getWordCount = function() {
   		if ($scope.summary == ''){
   			$scope.wordCount = 0;
   		} else{
        	$scope.wordCount = $scope.summary.trim().split(/\s+/).length;
        };
	}   	

}
