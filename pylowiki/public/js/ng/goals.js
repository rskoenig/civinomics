function GoalsCtrl($scope, $http, $location) {
  var getGoalsURL = $location.url() + 'goals/get'
  $http.get(getGoalsURL).success(function(data){
    $scope.goals = data;
    angular.forEach($scope.goals, function(goal){
        goal['editing'] = false;
    })
    $scope.baseURL = $location.url()
  })
 
  $scope.addGoal = function() {
    if ($scope.goalTitle.length > 0)
    {
      var thisGoal = {title:$scope.goalTitle, done:false};
      var addGoalURL = $scope.baseURL + 'goals/add';
      $http.post(addGoalURL, thisGoal).success(function(item){
        $scope.goals.push(item);
        $scope.goalTitle = '';
      });
    }
  };
  
  $scope.goalStatus = function(goal) {
    var goalUpdateURL = $scope.baseURL + 'goals/' + goal.code + '/update';
    $http.post(goalUpdateURL, goal);
  };
  
  $scope.goalEdit = function(goal) {
    goal.editing = true;
  };
  
  $scope.goalEditCancel = function(goal) {
    goal.editing = false;
  };
  
  $scope.goalEditDone = function(goal) {
    var goalUpdateURL = $scope.baseURL + 'goals/' + goal.code + '/update';
    if (this.editTitle){
      goal.title = this.editTitle;
      $http.post(goalUpdateURL, goal).success(function(data){
        goal.title = data.title;
        goal.done = data.done;
        goal.editing = false;
      });
    }
  };
  
  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.goals, function(todo) {
      count += todo.done ? 0 : 1;
    });
    return count;
  };
}

angular.module('civ', [])

.directive('civBlur', function() 
{
  return function( scope, elem, attrs ) {
    elem.bind('blur', function() {
      scope.$apply(attrs.civBlur);
    });
  };
})

.directive('civFocus', function( $timeout ) {
  return function( scope, elem, attrs ) {
    scope.$watch(attrs.civFocus, function( newval ) {
      if ( newval ) {
        $timeout(function() {
          elem[0].focus();
        }, 0, false);
      }
    });
  };
});