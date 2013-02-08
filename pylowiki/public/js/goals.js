function GoalsCtrl($scope, $http, $location) {
  var getGoalsURL = $location.url() + 'goals/get'
  $http.get(getGoalsURL).success(function(data){
    $scope.goals = data;
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
    var goalStatusURL = $scope.baseURL + 'goals/' + goal.code + '/update';
    $http.post(goalStatusURL, goal);
  };
  
  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.goals, function(todo) {
      count += todo.done ? 0 : 1;
    });
    return count;
  };
}