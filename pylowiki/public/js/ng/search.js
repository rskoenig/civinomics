function SearchCtrl($scope, $http) {
    $scope.workshopsURL = '/search/workshops'
    $scope.peopleURL = '/search/people'
    $scope.searchQuery = window.location.search
    $scope.showingWorkshops = {'class': 'active', 'show':true};
    $scope.showingPeople = {'class':'', 'show':true};
    
    $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
        $scope.workshops = data;
    })
    
    $scope.searchWorkshops = function() {
        $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
            $scope.workshops = data;
            $scope.showingWorkshops = {'class': 'active', 'show': true};
            $scope.showingPeople = {'class': '', 'show': false};
        })
    }
    
    $scope.searchPeople = function() {
        $http.get($scope.peopleURL + $scope.searchQuery).success(function(data){
            $scope.people = data;
            $scope.showingPeople = {'class': 'active', 'show': true};
            $scope.showingWorkshops = {'class': '', 'show': false};
        })
    }
}