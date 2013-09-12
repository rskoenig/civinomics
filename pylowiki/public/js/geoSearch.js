
function geoSearchCityChange(){
    var citySelectIndex = document.getElementById("geoSearchCity").selectedIndex;
    var citySelect = document.getElementById("geoSearchCity");
    var cityName = citySelect.options[citySelectIndex].value;
    var countySelectIndex = document.getElementById("geoSearchCounty").selectedIndex;
    var countySelect = document.getElementById("geoSearchCounty");
    var countyName = countySelect.options[countySelectIndex].value;
    var stateSelectIndex = document.getElementById("geoSearchState").selectedIndex;
    var stateSelect = document.getElementById("geoSearchState");
    var stateName = stateSelect.options[stateSelectIndex].value;
    document.getElementById("searchUnderPostal").innerText = document.getElementById("searchUnderPostal").textContent = "";
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    if (citySelectIndex === 0) {
        document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "or leave blank if specific to the entire county."; 
    } else {
        document.getElementById("searchPostalSelect").innerText = "";
        var urlString = '/geo/postalList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-") + "/" + cityName.replace(" ", "-");
        var postalList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(postalList);
        if (gobj.result != "0") {
            var postalCodes = gobj.result.split(/\|/);
            var postalMenu = "<div class=\"span1\"></div><div class=\"span2\">Postal Code:</div><div class=\"span9\">  <select id=\"geoSearchPost\" name=\"geoSearchPostal\" class=\"geoSearchPostal\" onChange=\"geoSearchPostalChange(); return 1;\"><option value=\"0\">Select a postal code</option>";
            for(var i = 0;i < postalCodes.length;i++){
                if (postalCodes[i] !== "") {
                    postalMenu = postalMenu + "<option value=\"" + postalCodes[i] + "\">" + postalCodes[i] + "</option>";
                }
            }
            postalMenu = postalMenu + "</select></div>";
            document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
            document.getElementById("searchPostalSelect").innerHTML = postalMenu;  
            document.getElementById("searchUnderPostal").innerText = document.getElementById("searchUnderPostal").textContent = "or leave blank if specific to the entire city.";
        }
    }
}


function geoSearchCountyChange(){
    var selectIndex = document.getElementById("geoSearchCounty").selectedIndex;
    var countySelect = document.getElementById("geoSearchCounty");
    var countyName = countySelect.options[selectIndex].value;
    var stateSelectIndex = document.getElementById("geoSearchState").selectedIndex;
    var stateSelect = document.getElementById("geoSearchState");
    var stateName = stateSelect.options[stateSelectIndex].value;
    document.getElementById("searchUnderPostal").innerText = document.getElementById("searchUnderPostal").textContent = "";
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "or leave blank if specific to the entire state."; 
    } else {
        document.getElementById("searchCitySelect").innerText = "";
        var urlString = '/geo/cityList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-");
        var cityList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(cityList);
        if (gobj.result != "0") {
            var cities = gobj.result.split(/\|/);
            var cityMenu = "<div class=\"span1\"></div><div class=\"span2\">City:</div><div class=\"span9\">  <select id=\"geoSearchCity\" name=\"geoSearchCity\" class=\"geoSearchCity\" onChange=\"geoSearchCityChange(); return 1;\"><option value=\"0\">Select a city</option>";
            for(var i = 0;i < cities.length;i++){
                if (cities[i] !== "") {
                    cityMenu = cityMenu + "<option value=\"" + cities[i] + "\">" + cities[i] + "</option>";
                }
            }
            cityMenu = cityMenu + "</select></div>";
            document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
            document.getElementById("searchCitySelect").innerHTML = cityMenu;  
            document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "or leave blank if specific to the entire county.";
        }
    }
}


function geoSearchStateChange(){
    var selectIndex = document.getElementById("geoSearchState").selectedIndex;
    var stateSelect = document.getElementById("geoSearchState");
    var stateName = stateSelect.options[selectIndex].value;
    document.getElementById("searchUnderPostal").innerText = document.getElementById("searchUnderPostal").textContent = "";
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "or leave blank if specific to the entire country.";
    } else {
        document.getElementById("searchCountySelect").innerText = "";
        var urlString = '/geo/countyList/united-states/' + stateName.replace(" ", "-");
        var countyList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(countyList);
        if (gobj.result != "0") {
            var counties = gobj.result.split(/\|/);
            var countyMenu = "<div class=\"span1\"></div><div class=\"span2\">County:</div><div class=\"span9\"><select id=\"geoSearchCounty\" name=\"geoSearchCounty\" class=\"geoSearchCounty\" onChange=\"geoSearchCountyChange(); return 1;\"><option value=\"0\">Select a county</option>";
            for(var i = 0;i < counties.length;i++){
                if (counties[i] !== "") {
                    countyMenu = countyMenu + "<option value=\"" + counties[i] + "\">" + counties[i] + "</option>";
                }
            }
            countyMenu = countyMenu + "</select></div>";
            document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "";
            document.getElementById("searchCountySelect").innerHTML = countyMenu;  
            document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "or leave blank if specific to the entire state.";
        }
    }
}

function geoSearchCountryChange(){
    var selectIndex = document.getElementById("geoSearchCountry").selectedIndex;
    document.getElementById("searchStateSelect").innerText = document.getElementById("searchStateSelect").textContent = "";
    document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    document.getElementById("searchUnderPostal").innerText = document.getElementById("searchUnderPostal").textContent = "";
    if (selectIndex === 0) {
        document.getElementById("searchStateSelect").innerText = document.getElementById("searchStateSelect").textContent = "or leave blank if specific to the entire planet.";
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
            var stateMenu = "<div class=\"span1\"></div><div class=\"span2\">State:</div><div class=\"span9\"><select id=\"geoSearchState\" name=\"geoSearchState\" class=\"geoSearchState\" onChange=\"geoSearchStateChange(); return 1;\"><option value=\"0\">Select a state</option>";
            for(var i = 0;i < states.length;i++){
                if (states[i] !== "") {
                    stateMenu = stateMenu + "<option value=\"" + states[i] + "\">" + states[i] + "</option>";
                }
            }
            stateMenu = stateMenu + "</select></div>";
            document.getElementById("searchStateSelect").innerText = document.getElementById("searchStateSelect").textContent = "";
            document.getElementById("searchStateSelect").innerHTML = stateMenu;            
            document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "or leave blank if specific to the entire country.";
        }
    }
}

