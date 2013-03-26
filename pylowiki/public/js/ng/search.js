function SearchCtrl($scope, $http) {
    $scope.workshopsURL = '/search/workshops'
    $scope.peopleURL = '/search/people'
    $scope.searchQuery = window.location.search
    $scope.showingWorkshops = true;
    $scope.showingPeople = false;
    
    $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
        $scope.workshops = data;
        $scope.showingWorkshops = true;
    })
    
    $scope.searchWorkshops = function() {
        $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
            $scope.workshops = data;
            $scope.showingWorkshops = true;
            $scope.showingPeople = false;
        })
    }
    
    $scope.searchPeople = function() {
        $http.get($scope.peopleURL + $scope.searchQuery).success(function(data){
            $scope.people = data;
            $scope.showingPeople = true
            $scope.showingWorkshops = false;
        })
    }
}