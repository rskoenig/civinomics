var app = angular.module('civ', ['ngSanitize']);

app.controller('ratingsController', function($scope, $http){
  /*
	  Things that I need for this controller:
	  	Adding a criteria
	  		Adding to an array
	  	Removing a criteria
	  		Removing from the array
	  	Sending the criteria to the workshop
	  		Array to string with pipes
	  			Custom cast?
	  		Getting the workshop code
	  			URL split? Mako injection?
	  		Do I really need a criteria controller then?
	  		Are they ever gonna be separated from workshops?
	  			Not for now.
	  		
	  	In the future, there will need to be also functions to retrieve current criteria and display them properly (for ideas and the likes) so we might need an independent controller.
  */
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
