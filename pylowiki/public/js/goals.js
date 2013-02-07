function GoalsCtrl($scope, $http) {
  $scope.goals = [];
 
  $scope.addGoal = function() {
    if ($scope.goalTitle.length > 0)
    {
      var thisGoal = {title:$scope.goalTitle, done:false};
      $scope.goals.push(thisGoal);
      $scope.goalTitle = '';
      $http.post($scope.postURL, thisGoal);
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