var app = angular.module('civ', ['$strap.directives']);

app.controller('SearchCtrl', function($scope, $http){
//function SearchCtrl($scope, $http) {
    /* 
    * This controller could benefit from some refactoring
    * 
    * Server response:
    *       statusCode == 0: Same as unix exit code (OK)
    *       statusCode == 1: No query was submitted
    *       statusCode == 2: Query submitted, no results found
    */
    $scope.workshopsURL = '/search/workshops'
    $scope.peopleURL = '/search/people'
    $scope.ideasURL = '/search/ideas'
    var searchQuery = window.location.search;
    $scope.searchQuery = searchQuery;
    $scope.searchQueryPretty = $("#search-input").val();
    $scope.showingWorkshops = {'class': 'active', 'show': false};
    $scope.showingPeople = {'class': '', 'show': false};
    $scope.showingIdeas = {'class': '', 'show': false};
    $scope.loading = true;
    $scope.noResult = false;
    $scope.noQuery = false;
    $scope.objType = 'workshops';
    
    $scope.tooltip = {bookmark: 'Bookmarks', activity: 'Ideas, conversations, resources, comments'};
    
    $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
        if (data.statusCode == 1)
        {
            $scope.noQuery = true;
            $scope.noResult = true;
            $scope.showingWorkshops.show = false;
            $scope.workshops = null;
        }
        else if (data.statusCode == 2)
        {
            $scope.noResult = true;
            $scope.workshops = null;
        }
        else if (data.statusCode == 0)
        {
            $scope.workshops = data.result;
            $scope.showingWorkshops.show = true;
        }
        $scope.loading = false;
    })
    
    $scope.searchWorkshops = function() {
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'workshops';
        $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingWorkshops = {'class': 'active', 'show': false};
                $scope.workshops = null;
            }
            else if(data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingWorkshops = {'class': 'active', 'show': false};
                $scope.workshops = null;
            }
            else if (data.statusCode == 0)
            {
                $scope.workshops = data.result;
                $scope.showingWorkshops = {'class': 'active', 'show': true};
            }
            $scope.loading = false;
        })
    }
    
    $scope.searchPeople = function() {
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'people';
        $http.get($scope.peopleURL + $scope.searchQuery).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingPeople = {'class': 'active', 'show': false};
                $scope.people = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingPeople = {'class': 'active', 'show': false};
                $scope.people = null;
            }
            else if (data.statusCode == 0)
            {
                $scope.people = data.result;
                $scope.showingPeople = {'class': 'active', 'show': true};
            }
            $scope.loading = false;
        })
    }
    
    $scope.searchIdeas = function() {
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'ideas';
        $http.get($scope.ideasURL + $scope.searchQuery).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingIdeas = {'class': 'active', 'show': false};
                $scope.ideas = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingIdeas = {'class': 'active', 'show': false};
                $scope.ideas = null;
            }
            else if (data.statusCode == 0)
            {
                $scope.ideas = data.result;
                $scope.showingIdeas = {'class': 'active', 'show': true};
            }
            $scope.loading = false;
        })
    }
})