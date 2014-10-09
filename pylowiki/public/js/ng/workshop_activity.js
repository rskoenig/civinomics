
function activityWorkshopController($scope, $http) {
    $scope.addThing = 'Idea';
    if ($scope.allowIdeas == '0') {
        $scope.addThing = 'Discussion';
    }
    if ($scope.allowResources == '0' && $scope.allowIdeas == '0') {
        $scope.addThing = 'Discussion';
    }
	$scope.listingType = 'activity';
	//$scope.thing = 'Idea';
	$scope.test = true
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
	if ($scope.phase == undefined || $scope.phase == '') {
	    $scope.phase = 'ideas';
	}

	$scope.getActivity = function() {
		$scope.alertMsg = '';
		$scope.activityURL = '/workshop/' + $scope.code + '/' + $scope.url + '/getActivity/0'
		if ($scope.thing){
			$scope.activityURL += '/' + $scope.thing
		}
		$scope.activityLoading = true;
		$http.get($scope.activityURL).success(function(data){
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

	$scope.getActivitySlice = function() {
		if ($scope.busy || $scope.noMoreSlices) return;
		$scope.busy = true;
		$scope.alertMsg = ''
		$scope.activityURL = '/workshop/' + $scope.code + '/' + $scope.url + '/getActivity/' + $scope.offset
		$scope.activityURL
		if ($scope.thing){
			$scope.activityURL += '/' + $scope.thing
		}
		$scope.activitySliceLoading = true;
		$http.get($scope.activityURL).success(function(data){
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
	$scope.thing = $scope.addThing;
	$scope.submitNewObj = function(){
		$scope.showAddNew = false;
		var newObjData = {'submit':'submit', 'title': $scope.newObjTitle, 'text': $scope.newObjText, 'link': $scope.newObjLink};
		$scope.newObjURL = '/workshop/' + $scope.code + '/' + $scope.url + '/add/' + $scope.addThing + '/handler';
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
		$scope.thing = undefined;
		if ($scope.allowIdeas == '0') {
            $scope.addThing = 'Discussion';
        } else {
            $scope.addThing = 'Idea';
        }

        $scope.getActivity();

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

		$scope.thisPhaseStatus = false;

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

		$scope.showAddBtn = true;
		$scope.showAddForm = false;

		if($scope.phase == 'research'){
			$scope.thisPhaseStatus = 'present'
		} else{
			$scope.thisPhaseStatus = 'past'
		};

		$scope.orderProp = '';
		$scope.thing = 'resource';
		$scope.query = {objType:'Resource'};
		$scope.query2 = '!disabled';
		if ($scope.allowResources == '0') {
            $scope.addThing = 'Discussion';
        } else {
            $scope.addThing = 'Resource';
        }

		$scope.getActivity();

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

		if($scope.phase == 'ideas'){
			$scope.thisPhaseStatus = 'present'
			$scope.showAddBtn = true;	
		} else if($scope.phase == 'research'){
			$scope.thisPhaseStatus = 'future'
			$scope.showAddBtn = false;
		} else{
			$scope.thisPhaseStatus = 'past'
			$scope.showAddBtn = false;
		};
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.query = {objType:'Idea'};
		$scope.query2 = '!disabled';
		$scope.thing = 'Idea'
		if ($scope.allowIdeas == '0') {
            $scope.addThing = 'Discussion';
        } else {
            $scope.addThing = 'Idea';
        }

        $scope.getActivity();

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

		if($scope.phase == 'initiatives'){
			$scope.thisPhaseStatus = 'present'
			$scope.showAddBtn = true;	
		} else if($scope.phase == 'research' || $scope.phase == 'ideas'){
			$scope.thisPhaseStatus = 'future'
			$scope.showAddBtn = false;
		} else{
			$scope.thisPhaseStatus = 'past'
			$scope.showAddBtn = false;
		};
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.query = {objType:'Initiative'};
		$scope.query2 = '!disabled';
		$scope.thing = 'Initiative'
		if ($scope.allowIdeas == '0') {
            $scope.addThing = 'Discussion';
        } else {
            $scope.addThing = 'Initiative';
        }

        $scope.getActivity();

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

		if($scope.phase == 'final rating'){
			$scope.thisPhaseStatus = 'present'
		} else if($scope.phase == 'research' || $scope.phase == 'ideas' || $scope.phase == 'initiatives'){
			$scope.thisPhaseStatus = 'future'
		} else{
			$scope.thisPhaseStatus = 'past'
		};
		$scope.showAddBtn = false;
		$scope.showAddForm = false;

		$scope.orderProp = '';
		$scope.query = {objType:'Initiative'};
		$scope.query2 = '!disabled';
		$scope.thing = 'Initiative'
		if ($scope.allowIdeas == '0') {
            $scope.addThing = 'Discussion';
        } else {
            $scope.addThing = 'Initiative';
        }

		$scope.getActivity();

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

		if($scope.phase == 'winning initiatives'){
			$scope.thisPhaseStatus = 'present'
		} else if($scope.phase != 'impact'){
			$scope.thisPhaseStatus = 'future'
		} else{
			$scope.thisPhaseStatus = 'past'
		};
		$scope.showAddBtn = false;
		$scope.showAddForm = false;
		
		$scope.query = {status:'adopted'};
		$scope.query2 = {status:'adopted'};
		$scope.thing = 'Initiative'

		$scope.getActivity();

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

		if($scope.phase == 'impact'){
			$scope.thisPhaseStatus = 'present'
		} else{
			$scope.thisPhaseStatus = 'future'
		};
		$scope.showAddBtn = false;
		$scope.showAddForm = false;
		
		$scope.query = {objType:'Update'};
		$scope.query2 = '';
		$scope.addThing = 'Update'

		$scope.getActivity();

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

		$scope.thisPhaseStatus = false;
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
		$scope.query = {objType:'Discussion'};
		$scope.query2 = '';
		$scope.thing = 'Discussion';
		$scope.addThing = 'Discussion';

		$scope.getActivity();

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
		$scope.query = {objType:'Resource'};
		$scope.query2 = '';
		$scope.thing = 'Resource';
		if ($scope.allowResources == '0') {
            $scope.addThing = 'Discussion';
        } else {
            $scope.addThing = 'Resource';
        }

        $scope.getActivity();

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

	if ($scope.phase == 'research'){
		$scope.researchClass = 'active-phase';
		$scope.toggleResearch();
	} else if ($scope.phase == 'ideas'){
		$scope.ideasClass = 'active-phase';
		$scope.toggleIdeas();
	} else if ($scope.phase == 'initiatives'){
		$scope.initiativesClass = 'active-phase';
		$scope.toggleInitiatives();
	} else if ($scope.phase == 'final rating'){
		$scope.finalClass = 'active-phase';
		$scope.toggleFinal();
	} else if ($scope.phase == 'winning initiatives'){
		$scope.adoptedClass = 'active-phase';
		$scope.toggleAdopted();
	} else if ($scope.phase == 'impact'){
		$scope.impactClass = 'active-phase';
		$scope.toggleImpact();
	};

}

function workshopMenuController($scope, Data) {
	$scope.data = Data
}

