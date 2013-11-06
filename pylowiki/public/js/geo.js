
$('button.geoButton').click(function(e){
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
            document.getElementById("werror").innerText = document.getElementById("werror").textContent = "No such zip code: " + document.getElementById("publicPostal").value;
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


function geoTagCityChange(){
    var citySelectIndex = document.getElementById("geoTagCity").selectedIndex;
    var citySelect = document.getElementById("geoTagCity");
    var cityName = citySelect.options[citySelectIndex].value;
    var countySelectIndex = document.getElementById("geoTagCounty").selectedIndex;
    var countySelect = document.getElementById("geoTagCounty");
    var countyName = countySelect.options[countySelectIndex].value;
    var stateSelectIndex = document.getElementById("geoTagState").selectedIndex;
    var stateSelect = document.getElementById("geoTagState");
    var stateName = stateSelect.options[stateSelectIndex].value;
    document.getElementById("underPostal").innerText = document.getElementById("underPostal").textContent = "";
    document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "";
    if (citySelectIndex === 0) {
        document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "Leave 'City' blank if specific to the entire county."; 
    } else {
        document.getElementById("postalSelect").innerText = "";
        var urlString = '/geo/postalList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-") + "/" + cityName.replace(" ", "-");
        var postalList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(postalList);
        if (gobj.result != "0") {
            var postalCodes = gobj.result.split(/\|/);
            var postalMenu = "<div class=\"span1\"></div><div class=\"span3\">Zip Code:</div><div class=\"span8\">  <select id=\"geoTagPost\" name=\"geoTagPostal\" class=\"geoTagPostal\" onChange=\"geoTagPostalChange(); return 1;\"><option value=\"0\">Select a Zip Code</option>";
            for(var i = 0;i < postalCodes.length;i++){
                if (postalCodes[i] !== "") {
                    postalMenu = postalMenu + "<option value=\"" + postalCodes[i] + "\">" + postalCodes[i] + "</option>";
                }
            }
            postalMenu = postalMenu + "</select></div>";
            document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "";
            document.getElementById("postalSelect").innerHTML = postalMenu;  
            document.getElementById("underPostal").innerText = document.getElementById("underPostal").textContent = "Leave 'Zip Code' blank if specific to the entire city.";
        }
    }
}


function geoTagCountyChange(){
    var selectIndex = document.getElementById("geoTagCounty").selectedIndex;
    var countySelect = document.getElementById("geoTagCounty");
    var countyName = countySelect.options[selectIndex].value;
    var stateSelectIndex = document.getElementById("geoTagState").selectedIndex;
    var stateSelect = document.getElementById("geoTagState");
    var stateName = stateSelect.options[stateSelectIndex].value;
    document.getElementById("underPostal").innerText = document.getElementById("underPostal").textContent = "";
    document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "";
    document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "Leave 'County' blank if specific to the entire state."; 
    } else {
        document.getElementById("citySelect").innerText = "";
        var urlString = '/geo/cityList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-");
        var cityList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(cityList);
        if (gobj.result != "0") {
            var cities = gobj.result.split(/\|/);
            var cityMenu = "<div class=\"span1\"></div><div class=\"span3\">City:</div><div class=\"span8\">  <select id=\"geoTagCity\" name=\"geoTagCity\" class=\"geoTagCity\" onChange=\"geoTagCityChange(); return 1;\"><option value=\"0\">Select a city</option>";
            for(var i = 0;i < cities.length;i++){
                if (cities[i] !== "") {
                    cityMenu = cityMenu + "<option value=\"" + cities[i] + "\">" + cities[i] + "</option>";
                }
            }
            cityMenu = cityMenu + "</select></div>";
            document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
            document.getElementById("citySelect").innerHTML = cityMenu;  
            document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "Leave 'City' blank if specific to the entire county.";
        }
    }
}


function geoTagStateChange(){
    var selectIndex = document.getElementById("geoTagState").selectedIndex;
    var stateSelect = document.getElementById("geoTagState");
    var stateName = stateSelect.options[selectIndex].value;
    document.getElementById("underPostal").innerText = document.getElementById("underPostal").textContent = "";
    document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "";
    document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
    document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
    document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "Leave 'City' blank if specific to the entire country.";
    } else {
        document.getElementById("countySelect").innerText = "";
        var urlString = '/geo/countyList/united-states/' + stateName.replace(" ", "-");
        var countyList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(countyList);
        if (gobj.result != "0") {
            var counties = gobj.result.split(/\|/);
            var countyMenu = "<div class=\"span1\"></div><div class=\"span3\">County:</div><div class=\"span8\"><select id=\"geoTagCounty\" name=\"geoTagCounty\" class=\"geoTagCounty\" onChange=\"geoTagCountyChange(); return 1;\"><option value=\"0\">Select a county</option>";
            for(var i = 0;i < counties.length;i++){
                if (counties[i] !== "") {
                    countyMenu = countyMenu + "<option value=\"" + counties[i] + "\">" + counties[i] + "</option>";
                }
            }
            countyMenu = countyMenu + "</select></div>";
            document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "";
            document.getElementById("countySelect").innerHTML = countyMenu;  
            document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "Leave 'County' blank if specific to the entire state.";
        }
    }
}

function geoTagCountryChange(){
    var selectIndex = document.getElementById("geoTagCountry").selectedIndex;
    document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "";
    document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "";
    document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
    document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "";
    document.getElementById("underPostal").innerText = document.getElementById("underPostal").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "Leave 'Country' blank if specific to the entire planet.";
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
            var stateMenu = "<div class=\"span1\"></div><div class=\"span3\">State:</div><div class=\"span8\"><select id=\"geoTagState\" name=\"geoTagState\" class=\"geoTagState\" onChange=\"geoTagStateChange(); return 1;\"><option value=\"0\">Select a state</option>";
            for(var i = 0;i < states.length;i++){
                if (states[i] !== "") {
                    stateMenu = stateMenu + "<option value=\"" + states[i] + "\">" + states[i] + "</option>";
                }
            }
            stateMenu = stateMenu + "</select></div>";
            document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "";
            document.getElementById("stateSelect").innerHTML = stateMenu;            
            document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "Leave 'State' blank if specific to the entire country.";
        }
    }
}


$('.geoTagCountry').change(function(e){
    e.preventDefault();
    var selectIndex = document.getElementById("geoTagCountry").selectedIndex;
    document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "";
    document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "";
    document.getElementById("citySelect").innerText = document.getElementById("citySelect").textContent = "";
    document.getElementById("postalSelect").innerText = document.getElementById("postalSelect").textContent = "";
    document.getElementById("underPostal").innerText = document.getElementById("underPostal").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "Leave 'Country' blank if specific to the entire planet.";
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
            var stateMenu = "<div class=\"span1\"></div><div class=\"span3\">State:</div><div class=\"span8\"><select id=\"geoTagState\" name=\"geoTagState\" class=\"geoTagState\" onChange=\"geoTagStateChange(); return 1;\"><option value=\"0\">Select a state</option>";
            for(var i = 0;i < states.length;i++){
                if (states[i] !== "") {
                    stateMenu = stateMenu + "<option value=\"" + states[i] + "\">" + states[i] + "</option>";
                }
            }
            stateMenu = stateMenu + "</select></div>";
            document.getElementById("stateSelect").innerText = document.getElementById("stateSelect").textContent = "";
            document.getElementById("stateSelect").innerHTML = stateMenu;            
            document.getElementById("countySelect").innerText = document.getElementById("countySelect").textContent = "Leave 'State' blank if specific to the entire country.";
        }
    }
});

function geoCheckPostalCode(){
    var postalCode = document.getElementById("postalCode").value;
    document.getElementById("postalCodeResult").innerText = document.getElementById("postalCodeResult").textContent = "";
    var checkURL = "/geo/cityStateCountry/" + postalCode
    var checkResult = $.ajax({
        type : 'POST',
        async : false,
        url  : checkURL
    }).responseText;
    var gobj = jQuery.parseJSON(checkResult);
    document.getElementById("postalCodeResult").innerText = document.getElementById("postalCodeResult").textContent = gobj.result;
}

