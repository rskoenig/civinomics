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
    var pathname = window.location.pathname;
    var pathList = pathname.split('/');
    /*var action = pathList[1];
    var pathlen = pathList.length;*/

    var action = 'ideas';
    var pathlen = pathList.length;
    $scope.noResult = false;
    $scope.noQuery = false;
    $scope.loading = true;
    $scope.pathname = pathname;
    
    $scope.searchType = 'name';
    
    $scope.searchString = 'bufs';
    
    if($scope.searchString === '') {
        $scope.noQuery = true;
        $scope.loading = false;
    }

    $scope.ideasURL = '/search/ideas/' + 'gen' + '/' + 'why';
    
    $scope.objType = 'ideas';
    $scope.orderProp = '-date';
    $scope.orderProp = '-date';
    $scope.tooltip = {bookmark: 'Bookmarks', activity: 'Ideas, conversations, resources, comments, photos'};
    $scope.currentPage = 0;
    $scope.pageSize = 20;

    $http.get($scope.ideasURL).success(function(data){
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
        else if (data.statusCode === 0)
        {
            $scope.workshops = data.result;
            $scope.showingWorkshops.show = true;
        }
        $scope.loading = false;
    });
    
    
    $scope.searchIdeas = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'ideas';
        $http.get($scope.ideasURL).success(function(data){
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
            else if (data.statusCode === 0)
            {
                $scope.ideas = data.result;
                $scope.showingIdeas = {'class': 'active', 'show': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.ideas.length/$scope.pageSize);                
        }
    };
app.filter('startFrom', function() {
    return function(input, start) {
        if(start) {
            start = +start; //parse to int
            return input.slice(start);
        } else {
            return input;
        }
    }
});