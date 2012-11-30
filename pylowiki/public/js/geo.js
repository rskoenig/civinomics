
$('button.geoButton').live('click', function(e){
    e.preventDefault();
    $geo = $(this);
    var urlString = '/geoHandler/united-states/' + document.getElementById("publicPostal").value;
    var geoScope = $.ajax({
       type : 'POST',
       async : false,
       url  : urlString
    }).responseText;
    var gobj = jQuery.parseJSON(geoScope);
    if (gobj.result == "0") {
            document.getElementById("werror").innerText = document.getElementById("werror").textContent = "No such postal code: " + document.getElementById("publicPostal").value;
            document.getElementById("publicPostal").value = document.getElementById("wpostal").innerText;
            document.getElementById("publicPostal").value = document.getElementById("wpostal").textContent;
    } else {
            var scopeList = gobj.result.split(/\|/);
            var country = scopeList[2]; 
            var state = scopeList[4]; 
            var county = scopeList[6]; 
            var city = scopeList[8]; 
            var postal = scopeList[9]; 
            document.getElementById("wcountry").innerText = document.getElementById("wcountry").textContent = country;
            document.getElementById("wstate").innerText = document.getElementById("wstate").textContent = state;
            document.getElementById("wcounty").innerText = document.getElementById("wcounty").textContent = county;
            document.getElementById("wcity").innerText = document.getElementById("wcity").textContent = city;
            document.getElementById("wpostal").innerText = document.getElementById("wpostal").textContent = document.getElementById("publicPostal").value;
    }
});


function geoTagCountyChange(){
    var selectIndex = document.getElementById("geoTagCounty").selectedIndex;
    var countySelect = document.getElementById("geoTagCounty");
    var countyName = countySelect.options[selectIndex].value;
    var stateSelectIndex = document.getElementById("geoTagState").selectedIndex;
    var stateSelect = document.getElementById("geoTagState");
    var stateName = stateSelect.options[stateSelectIndex].value;
    if (selectIndex === 0) {
        document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "or leave blank if your workshop is specific to the entire state.";
        document.getElementById("underCity").innerText = document.getElementById("underCity").textContent = "";   
    } else {
        document.getElementById("stateSelect").innerText = "";
        var urlString = '/geo/cityList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-");
        var cityList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(cityList);
        if (gobj.result != "0") {
            var cities = gobj.result.split(/\|/);
            var cityMenu = "City:  <select id=\"geoTagCity\" name=\"geoTagCity\" class=\"geoTagCity\" onChange=\"geoTagCityChange(); return 1;\"><option value=\"Choose a city\">Choose a city</option>";
            for(var i = 0;i < cities.length;i++){
                if (cities[i] !== "") {
                    cityMenu = cityMenu + "<option value=\"" + cities[i] + "\">" + cities[i] + "</option>";
                }
            }
            cityMenu = cityMenu + "</select>";
            document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
            document.getElementById("citySelect").innerHTML = cityMenu;  
            document.getElementById("underCity").innerText = document.getElementById("underCity").textContent = "or leave blank if your workshop is specific to the entire county.";
        }
    }
}


function geoTagStateChange(){
    var selectIndex = document.getElementById("geoTagState").selectedIndex;
    var stateSelect = document.getElementById("geoTagState");
    var stateName = stateSelect.options[selectIndex].value;
    if (selectIndex === 0) {
        document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "or leave blank if your workshop is specific to the entire country.";
        document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
        document.getElementById("underCity").innerText = document.getElementById("underCity").textContent = "";  
    } else {
        document.getElementById("stateSelect").innerText = "";
        var urlString = '/geo/countyList/united-states/' + stateName.replace(" ", "-");
        var countyList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(countyList);
        if (gobj.result != "0") {
            var counties = gobj.result.split(/\|/);
            var countyMenu = "County:  <select id=\"geoTagCounty\" name=\"geoTagCounty\" class=\"geoTagCounty\" onChange=\"geoTagCountyChange(); return 1;\"><option value=\"Choose a county\">Choose a county</option>";
            for(var i = 0;i < counties.length;i++){
                if (counties[i] !== "") {
                    countyMenu = countyMenu + "<option value=\"" + counties[i] + "\">" + counties[i] + "</option>";
                }
            }
            countyMenu = countyMenu + "</select>";
            document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "";
            document.getElementById("countySelect").innerHTML = countyMenu;  
            document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "or leave blank if your workshop is specific to the entire state.";
        }
    }
}


$('.geoTagCountry').change(function(e){
    e.preventDefault();
    var selectIndex = document.getElementById("geoTagCountry").selectedIndex;
    if (selectIndex === 0) {
        document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "or leave blank if your workshop is specific to the entire planet.";
        document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "";
        document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";       
    }
    if (selectIndex === 1) {
        var urlString = '/geo/stateList/united-states';
        var stateList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(stateList);
        if (gobj.result != "0") {
            var states = gobj.result.split(/\|/);
            var stateMenu = "<br />State:  <select id=\"geoTagState\" name=\"geoTagState\" class=\"geoTagState\" onChange=\"geoTagStateChange(); return 1;\"><option value=\"Choose a state\">Choose a state</option>";
            for(var i = 0;i < states.length;i++){
                if (states[i] !== "") {
                    stateMenu = stateMenu + "<option value=\"" + states[i] + "\">" + states[i] + "</option>";
                }
            }
            stateMenu = stateMenu + "</select>";
            document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "";
            document.getElementById("stateSelect").innerHTML = stateMenu;            
            document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "or leave blank if your workshop is specific to the entire country.";
        }
    }
});

