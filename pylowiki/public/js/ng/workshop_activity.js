
function activityWorkshopController($scope, $http) {
    $scope.addObjType = 'idea';
    if ($scope.allowIdeas == '0') {
        $scope.addObjType = 'discussion';
    }
    if ($scope.allowResources == '0' && $scope.allowIdeas == '0') {
        $scope.addObjType = 'discussion';
    }
	$scope.listingType = 'activity';
	$scope.objType = 'idea';
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.numAdopted = 0;
	$scope.numIdeas = 0;
	$scope.numDiscussions = 0;
	$scope.numResources = 0;
	if ($scope.offset == undefined) {
	    $scope.offset = 0;
	}

	$scope.getActivity = function() {
		$scope.alertMsg = '';
		$scope.activityLoading = true;
		$http.get('/workshop/' + $scope.code + '/' + $scope.url + '/getActivity').success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
				$scope.activity = [];
				$scope.alertMsg = "There are no ideas, resources or discussions yet. Be the first to add one!";
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.noMoreSlices = false;
				$scope.offset = $scope.sliceSize;
				$scope.activity = data.result;
				$scope.numAdopted = data.numAdopted;
				$scope.numIdeas = data.numIdeas;
				$scope.numDiscussions = data.numDiscussions;
				$scope.numResources = data.numResources;
			}
			$scope.activityLoading = false;
		})
	};

	$scope.getActivity();

	$scope.getActivitySlice = function() {
		if ($scope.busy || $scope.noMoreSlices) return;
		$scope.busy = true;
		$scope.alertMsg = ''
		$scope.activitySliceLoading = true;
		$http.get('/workshop/' + $scope.code + '/' + $scope.url + '/getActivity/' + $scope.offset).success(function(data){
			if (data.statusCode == 1){
				$scope.noMoreSlices = true;
			} 
			else if (data.statusCode === 0){
				activitySlice = data.result;
				for (var i = 0; i < activitySlice.length; i++) {
				    $scope.activity.push(activitySlice[i]);
				}
				$scope.noMoreSlices = false;
			}
			$scope.activitySliceLoading = false;
			$scope.busy = false;
			$scope.offset += $scope.sliceSize;
		})
	};


	// Add a new object
	$scope.objType = $scope.addObjType;
	$scope.submitNewObj = function(){
		$scope.showAddNew = false;
		var newObjData = {'submit':'submit', 'title': $scope.newObjTitle, 'text': $scope.newObjText, 'link': $scope.newObjLink};
		$scope.newObjURL = '/workshop/' + $scope.code + '/' + $scope.url + '/add/' + $scope.addObjType + '/handler';
		$http.post($scope.newObjURL, newObjData).success(function(data){
			//$scope.numComments = Number($scope.numComments) + 1;
            $scope.getActivity();
            $scope.newObjTitle = '';
	        $scope.newObjText = '';
	        $scope.newObjLink = '';
        });
	};

	// Inititial Values : Workshop Phases
	$scope.showResearch = false;
	$scope.showIdeas = false;
	$scope.showInitiatives = false;
	$scope.showFinal = false;
	$scope.showWinning = false;
	$scope.showImpact = false;

	$scope.showBrief = false;
	$scope.showStats = false;
	$scope.showAll = false;

	$scope.showAddBtn = true;
	$scope.showAddForm = false;
	$scope.orderProp = '';
	$scope.query = '';
	$scope.query2 = '!disabled';


	$scope.toggleAllActivity= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = true;
		$scope.showAddForm = false;
		$scope.orderProp = '';
		$scope.query = '';
		$scope.query2 = '!disabled';
		$scope.objType = 'idea';
		if ($scope.allowIdeas == '0') {
            $scope.addObjType = 'discussion';
        } else {
            $scope.addObjType = 'idea';
        }
	}

	$scope.toggleBrief= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = true;
		$scope.showList = false;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = false;
		$scope.showAddForm = false;
	}

	$scope.toggleResearch= function(){
		$scope.showResearch = true;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = false;
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.objType = 'resource';
		$scope.query = {objType:'resource'};
		$scope.query2 = '!disabled';
		if ($scope.allowResources == '0') {
            $scope.addObjType = 'discussion';
        } else {
            $scope.addObjType = 'resource';
        }
	};

	$scope.toggleIdeas= function(){
		$scope.showResearch = false;
		$scope.showIdeas = true;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = true;
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.query = {objType:'idea'};
		$scope.query2 = '!disabled';
		$scope.objType = 'idea'
		if ($scope.allowIdeas == '0') {
            $scope.addObjType = 'discussion';
        } else {
            $scope.addObjType = 'idea';
        }
	}

	$scope.toggleInitiatives= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = true;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = true;
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.query = {objType:'initiative'};
		$scope.query2 = '!disabled';
		$scope.objType = 'initiative'
		if ($scope.allowIdeas == '0') {
            $scope.addObjType = 'discussion';
        } else {
            $scope.addObjType = 'initiative';
        }
	}

	$scope.toggleFinal= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = true;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = false;
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.query = {objType:'initiative'};
		$scope.query2 = '!disabled';
		$scope.objType = 'initiative'
		if ($scope.allowIdeas == '0') {
            $scope.addObjType = 'discussion';
        } else {
            $scope.addObjType = 'initiative';
        }
	}

	$scope.toggleAdopted= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = true;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = false;
		$scope.showAddForm = false;
		
		$scope.query = {status:'adopted'};
		$scope.query2 = {status:'adopted'};
		$scope.objType = 'initiative'
	}

	$scope.toggleImpact= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = true;

		$scope.showBrief = false;
		$scope.showList = true;
		$scope.showStats = false;
		$scope.showAll = false;

		$scope.showAddBtn = false;
		$scope.showAddForm = false;
		
		$scope.query = {objType:'update'};
		$scope.query2 = '';
		$scope.addObjType = 'update'
	}


	$scope.toggleStats= function(){
		$scope.showResearch = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showFinal = false;
		$scope.showAdopted = false;
		$scope.showImpact = false;

		$scope.showBrief = false;
		$scope.showList = false;
		$scope.showStats = true;
		$scope.showAll = false;

		$scope.showAddBtn = false;
		$scope.showAddForm = false;
	}

	$scope.toggleDiscussions= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showDiscussions = true;
		$scope.showResources = false;
		$scope.showAddBtn = true;
		$scope.showAddNew = false;
		$scope.query = {objType:'discussion'};
		$scope.query2 = '';
		$scope.objType = 'discussion';
		$scope.addObjType = 'discussion';
	};

	$scope.toggleResources= function(){
		$scope.showSummary = false;
		$scope.showInfoPreview = false;
		$scope.showInfo = false;
		$scope.showStats = false;
		$scope.showIdeas = false;
		$scope.showInitiatives = false;
		$scope.showDiscussions = false;
		$scope.showResources = true;
		$scope.showAddBtn = true;
		$scope.showAddNew = false;
		$scope.query = {objType:'resource'};
		$scope.query2 = '';
		$scope.objType = 'resource';
		if ($scope.allowResources == '0') {
            $scope.addObjType = 'discussion';
        } else {
            $scope.addObjType = 'resource';
        }
	};

	$scope.toggleAddForm= function(){
		$scope.showAddForm = true;
	};

	$scope.cancelAddForm= function(){
        $scope.showAddForm = false;
        $scope.newObjTitle = '';
        $scope.newObjText = '';
        $scope.newObjLink = '';
	};
}

function workshopMenuController($scope, Data) {
	$scope.data = Data
}

