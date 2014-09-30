var app = angular.module('civ', ['$strap.directives', 'ngSanitize']);

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
    var action = pathList[1];
    var pathlen = pathList.length;
    $scope.noResult = false;
    $scope.noQuery = false;
    $scope.loading = true;
    $scope.pathname = pathname;
    if(action === 'search' && pathlen === 2) {
        $scope.searchType = 'name';
        var searchList = window.location.search.split('=');
        $scope.searchString = searchList[1];
    } else if(action === 'search' && pathlen === 4) {
        $scope.searchType = pathList[3];
        $scope.searchString = pathList[4];
    } else if(action === 'searchTags') {
        $scope.searchType = 'tag';
        $scope.searchString = pathList[2];
    } else if(action === 'workshops') {
        $scope.searchType = 'geo';
        if (pathlen === 4) {
            $scope.searchString = "||0||0||0||0|0";
        }
        if (pathlen === 5) {
            $scope.searchString = "||" + pathList[4] + "||0||0||0|0";
        }
        if (pathlen === 6) {
            $scope.searchString = "||" + pathList[4] + "||" + pathList[5] + "||0||0|0";
        }
        if (pathlen === 7) {
            $scope.searchString = "||" + pathList[4] + "||" + pathList[5] + "||" + pathList[6] + "||0|0";
        }
        if (pathlen === 8) {
            $scope.searchString = "||" + pathList[4] + "||" + pathList[5] + "||" + pathList[6] + "||" + pathList[7] + "|0";
        }
        if (pathlen === 9) {
            $scope.searchString = "||" + pathList[4] + "||" + pathList[5] + "||" + pathList[6] + "||" + pathList[7] + "|" + pathList[8];
        }
    } else if (action === 'browse' || action === 'splash'){
        $scope.searchType = 'browse';
    }

    if($scope.searchString === '') {
        $scope.noQuery = true;
        $scope.loading = false;
    }
    $scope.workshopsURL = '/search/workshops/' + $scope.searchType + '/' + $scope.searchString;
    $scope.peopleURL = '/search/people/' + $scope.searchType + '/' + $scope.searchString;
    $scope.resourcesURL = '/search/resources/' + $scope.searchType + '/' + $scope.searchString;
    $scope.discussionsURL = '/search/discussions/' + $scope.searchType + '/' + $scope.searchString;
    $scope.ideasURL = '/search/ideas/' + $scope.searchType + '/' + $scope.searchString;
    $scope.photosURL = '/search/photos/' + $scope.searchType + '/' + $scope.searchString;
    $scope.initiativesURL = '/search/initiatives/' + $scope.searchType + '/' + $scope.searchString;
    $scope.searchQueryPretty = $("#search-input").val();
    $scope.showingWorkshops = {'class': '', 'show': false, 'create': false};
    //$scope.showingWorkshops = {'class': 'active', 'show': false, 'create': false};
    $scope.showingPeople = {'class': '', 'show': false, 'create': false};
    $scope.showingResources = {'class': '', 'show': false, 'create': false};
    $scope.showingDiscussions = {'class': '', 'show': false, 'create': false};
    $scope.showingIdeas = {'class': '', 'show': false, 'create': false};
    $scope.showingPhotos = {'class': '', 'show': false, 'create': false};
    $scope.showingInitiatives = {'class': 'active', 'show': false, 'create': false};
    //$scope.showingInitiatives = {'class': '', 'show': false, 'create': false};
    $scope.objType = 'initiatives';
    //$scope.objType = 'workshops';
    if(action === 'splash'){
        $scope.orderProp = '-voteCount';
    } else {
        $scope.orderProp = '-date';
    }

    /* refine the search results with a tag filter if in url */
    $scope.query = '';
    if ($scope.searchType == 'geo') {
        var searchList = window.location.search.split('=');
        if (searchList[1]){
            $scope.query = searchList[1]; 
        };
    };

    $scope.votedornot = 'nvote'
    $scope.tooltip = {bookmark: 'Bookmarks', activity: 'Ideas, conversations, resources, comments, photos, initiatives'};
    $scope.currentPage = 0;
    $scope.pageSize = 10;

    $http.get($scope.initiativesURL).success(function(data){
    //$http.get($scope.workshopsURL).success(function(data){
        if (data.statusCode == 1)
        {
            $scope.noQuery = true;
            $scope.noResult = true;
            $scope.showingPhotos = {'class': 'active', 'show': false, 'create': true};
            $scope.photos = null;
        }
        else if (data.statusCode == 2)
        {
            $scope.noResult = true;
            $scope.showingInitiatives = {'class': 'active', 'show': false, 'create': true};
            //$scope.showingWorkshops = {'class': 'active', 'show': false, 'create': true};
            $scope.photos = null;
        }
        else if (data.statusCode === 0)
        {
            $scope.initiatives = data.result;
            //$scope.workshops = data.result;
            $scope.showingInitiatives = {'class': 'active', 'show': true, 'create': true};
            //$scope.showingWorkshops = {'class': 'active', 'show': true, 'create': true};
        }
        $scope.loading = false;
    });
    $scope.numberOfPages=function(){
        //return Math.ceil($scope.initiatives.length/$scope.pageSize); 
        return Math.ceil($scope.initiatives.length/$scope.pageSize);
    }
    
    $scope.searchWorkshops = function() {
        $scope.currentPage = 0;
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.showingInitiatives = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'workshops';
        $http.get($scope.workshopsURL).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingWorkshops = {'class': 'active', 'show': false, 'create': true};
                $scope.workshops = null;
            }
            else if(data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingWorkshops = {'class': 'active', 'show': false, 'create': true};
                $scope.workshops = null;
            }
            else if (data.statusCode === 0)
            {
                $scope.workshops = data.result;
                $scope.showingWorkshops = {'class': 'active', 'show': true, 'create': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.workshops.length/$scope.pageSize);                
        }
    };
    
    $scope.searchPeople = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.showingInitiatives = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'people';
        $http.get($scope.peopleURL).success(function(data){
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
            else if (data.statusCode === 0)
            {
                $scope.people = data.result;
                $scope.showingPeople = {'class': 'active', 'show': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.people.length/$scope.pageSize);                
        }
    };
    
    $scope.searchResources = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.showingInitiatives = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'resources';
        $http.get($scope.resourcesURL).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingResources = {'class': 'active', 'show': false, 'create': true};
                $scope.resources = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingResources = {'class': 'active', 'show': false, 'create': true};
                $scope.resources = null;
            }
            else if (data.statusCode === 0)
            {
                $scope.resources = data.result;
                $scope.showingResources = {'class': 'active', 'show': true, 'create': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.resources.length/$scope.pageSize);                
        }
    };
    
    $scope.searchDiscussions = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.showingInitiatives = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'discussions';
        $http.get($scope.discussionsURL).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingDiscussions = {'class': 'active', 'show': false, 'create': true};
                $scope.discussions = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingDiscussions = {'class': 'active', 'show': false, 'create': true};
                $scope.discussions = null;
            }
            else if (data.statusCode === 0)
            {
                $scope.discussions = data.result;
                $scope.showingDiscussions = {'class': 'active', 'show': true, 'create': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.discussions.length/$scope.pageSize);                
        }
    };
    
    $scope.searchIdeas = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.showingInitiatives = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'ideas';
        $http.get($scope.ideasURL).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingIdeas = {'class': 'active', 'show': false, 'create': true};
                $scope.ideas = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingIdeas = {'class': 'active', 'show': false, 'create': true};
                $scope.ideas = null;
            }
            else if (data.statusCode === 0)
            {
                $scope.ideas = data.result;
                $scope.showingIdeas = {'class': 'active', 'show': true, 'create': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.ideas.length/$scope.pageSize);                
        }
    };
        
    $scope.searchPhotos = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.showingInitiatives = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'photos';
        $http.get($scope.photosURL).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingPhotos = {'class': 'active', 'show': false, 'create': true};
                $scope.photos = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingPhotos = {'class': 'active', 'show': false, 'create': true};
                $scope.photos = null;
            }
            else if (data.statusCode === 0)
            {
                $scope.photos = data.result;
                $scope.showingPhotos = {'class': 'active', 'show': true, 'create': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.photos.length/$scope.pageSize);                
        }
    };
    
    $scope.searchInitiatives = function() {
        $scope.currentPage = 0;
        $scope.showingWorkshops = {'class': '', 'show': false};
        $scope.showingPeople = {'class': '', 'show': false};
        $scope.showingResources = {'class': '', 'show': false};
        $scope.showingDiscussions = {'class': '', 'show': false};
        $scope.showingIdeas = {'class': '', 'show': false};
        $scope.showingPhotos = {'class': '', 'show': false};
        $scope.noResult = false;
        $scope.noQuery = false;
        $scope.loading = true;
        $scope.objType = 'initiatives';
        $http.get($scope.initiativesURL).success(function(data){
            if (data.statusCode == 1)
            {
                $scope.noQuery = true;
                $scope.noResult = true;
                $scope.showingPhotos = {'class': 'active', 'show': false, 'create': true};
                $scope.photos = null;
            }
            else if (data.statusCode == 2)
            {
                $scope.noResult = true;
                $scope.showingInitiatives = {'class': 'active', 'show': false, 'create': true};
                $scope.photos = null;
            }
            else if (data.statusCode === 0)
            {
                $scope.initiatives = data.result;
                $scope.showingInitiatives = {'class': 'active', 'show': true, 'create': true};
            }
            $scope.loading = false;
        });
        $scope.numberOfPages=function(){
            return Math.ceil($scope.initiatives.length/$scope.pageSize);                
        }
    };
});


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
