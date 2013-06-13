var app = angular.module('civ', []);

app.controller('blogController', function($scope, $http){
    var getPostsURL = 'https://public-api.wordpress.com/rest/v1/sites/32509853/posts';
    var getBlogURL = 'https://public-api.wordpress.com/rest/v1/sites/32509853';
    $scope.posts = [];
    $scope.blog = {};
    
    $http.get(getPostsURL).success(function(data){
        $scope.posts = data.posts;
        console.log(data);
    });
    
    $http.get(getBlogURL).success(function(data){
        $scope.blog = data;
        console.log(data);
    });
});