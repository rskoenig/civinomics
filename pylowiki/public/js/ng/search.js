function SearchCtrl($scope, $http) {
    $scope.workshopsURL = '/search/workshops'
    $scope.peopleURL = '/search/people'
    $scope.searchQuery = window.location.search
    $scope.showingWorkshops = {'class': 'active', 'show': true};
    $scope.showingPeople = {'class': '', 'show': true};
    $scope.loading = true;
    
    $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
        $scope.workshops = data;
        $scope.loading = false;
    })
    
    $scope.searchWorkshops = function() {
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.loading = true;
        $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
            $scope.workshops = data;
            $scope.showingWorkshops = {'class': 'active', 'show': true};
            $scope.loading = false;
        })
    }
    
    $scope.searchPeople = function() {
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.loading = true;
        $http.get($scope.peopleURL + $scope.searchQuery).success(function(data){
            $scope.people = data;
            $scope.showingPeople = {'class': 'active', 'show': true};
            $scope.loading = false;
        })
    }
}