
function resourceController($scope, $http, $location, $timeout) {
    $scope.resourceFormPrompt     = false;
    
    $scope.showResourcePrompt = function() {
        if(document.getElementById('resourceTypeURL').checked) {
            document.getElementById("resourceTypeEmbedForm").className = "collapse";
            document.getElementById("addResourceEmbed").value = ""
            document.getElementById("resourceTypeURLForm").className = "collapse in";
        } else if(document.getElementById('resourceTypeEmbed').checked) {
            document.getElementById("resourceTypeURLForm").className = "collapse";
            document.getElementById("addResourceLink").value = ""
            document.getElementById("resourceTypeEmbedForm").className = "collapse in";
        }
    };

}
