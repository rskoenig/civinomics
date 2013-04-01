var app = angular.module('civ', [], function($locationProvider){
    $locationProvider.html5Mode(true);
});

app.controller('GoalsCtrl', function($scope, $http, $location){
  $scope.baseURL = $location.path();
  $scope.location = $location;
  if ($scope.baseURL.match('preferences'))
  {
    $scope.baseURL = $scope.baseURL.slice(-$scope.baseURL.length, -11);
  }
  else if ($scope.baseURL.match('/add/idea'))
  {
    $scope.baseURL = $scope.baseURL.slice(-$scope.baseURL.length, -8);
  }
  $http.get($scope.baseURL + 'goals/get').success(function(data){
    $scope.goals = data;
    angular.forEach($scope.goals, function(goal){
        goal.editing = false;
    });
  });
 
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
  
  $scope.goalEditState = function(goal) {
    goal.editing = !goal.editing;
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
  
  $scope.deleteGoal = function(goal) {
    // javascript lacks a function to remove an item from an array other than pop()
    var goalDeleteURL = $scope.baseURL + 'goals/' + goal.code + '/delete';
    $http.post(goalDeleteURL, goal).success(function(data){
      var oldGoals = $scope.goals;
      $scope.goals = [];
      angular.forEach(oldGoals, function(goal) {
        if (goal.code != data.code) { $scope.goals.push(goal); }
      });
    });
  };
  
  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.goals, function(goal) {
      count += goal.done ? 0 : 1;
    });
    return count;
  };
});

app.directive('civBlur', function() 
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
