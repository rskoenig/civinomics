
function geoSearchPostalChange(){
    var postalSelectIndex = document.getElementById("geoSearchPostal").selectedIndex;
    var postalSelect = document.getElementById("geoSearchPostal");
    var postalName = postalSelect.options[postalSelectIndex].value;
    var citySelectIndex = document.getElementById("geoSearchCity").selectedIndex;
    var citySelect = document.getElementById("geoSearchCity");
    var cityName = citySelect.options[citySelectIndex].value;
    var countySelectIndex = document.getElementById("geoSearchCounty").selectedIndex;
    var countySelect = document.getElementById("geoSearchCounty");
    var countyName = countySelect.options[countySelectIndex].value;
    var stateSelectIndex = document.getElementById("geoSearchState").selectedIndex;
    var stateSelect = document.getElementById("geoSearchState");
    var stateName = stateSelect.options[stateSelectIndex].value;
    document.getElementById("searchCountryButton").innerText = document.getElementById("searchCountryButton").textContent = "";
    document.getElementById("searchStateButton").innerText = document.getElementById("searchStateButton").textContent = "";
    document.getElementById("searchCountyButton").innerText = document.getElementById("searchCountyButton").textContent = "";
    document.getElementById("searchCityButton").innerText = document.getElementById("searchCityButton").textContent = "";
    document.getElementById("searchPostalButton").innerText = document.getElementById("searchPostalButton").textContent = "";
    if(postalSelectIndex) {
        var searchURL = '/workshops/geo/earth/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-") + "/" + cityName.replace(" ", "-") + "/" + postalName;
        var searchButton = "<a href=\"" + searchURL + "\" class=\"btn btn-success btn-small\">Go to Zip Code</a>";
        document.getElementById("searchPostalButton").innerHTML = searchButton;
    }
}

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
    document.getElementById("searchCountryButton").innerText = document.getElementById("searchCountryButton").textContent = "";
    document.getElementById("searchStateButton").innerText = document.getElementById("searchStateButton").textContent = "";
    document.getElementById("searchCountyButton").innerText = document.getElementById("searchCountyButton").textContent = "";
    document.getElementById("searchCityButton").innerText = document.getElementById("searchCityButton").textContent = "";
    document.getElementById("searchPostalButton").innerText = document.getElementById("searchPostalButton").textContent = "";
    
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    document.getElementById("searchPostalSelect").innerText = "";
    if(citySelectIndex) {
        var urlString = '/geo/postalList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-") + "/" + cityName.replace(" ", "-");
        var postalList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(postalList);
        if (gobj.result != "0") {
            var postalCodes = gobj.result.split(/\|/);
            var postalMenu = "<select id=\"geoSearchPostal\" name=\"geoSearchPostal\" class=\"geoSearchPostal\" onChange=\"geoSearchPostalChange(); return 1;\"><option value=\"0\">- Select a Zip Code -</option>";
            for(var i = 0;i < postalCodes.length;i++){
                if (postalCodes[i] !== "") {
                    postalMenu = postalMenu + "<option value=\"" + postalCodes[i] + "\">" + postalCodes[i] + "</option>";
                }
            }
            postalMenu = postalMenu + "</select>";
            var searchURL = '/workshops/geo/earth/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-") + "/" + cityName.replace(" ", "-");
            var searchButton = "<a href=\"" + searchURL + "\" class=\"btn btn-success btn-small\">Go to City</a>";
            document.getElementById("searchCityButton").innerHTML = searchButton;
            document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
            document.getElementById("searchPostalSelect").innerHTML = postalMenu;
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
    document.getElementById("searchCountryButton").innerText = document.getElementById("searchCountryButton").textContent = "";
    document.getElementById("searchStateButton").innerText = document.getElementById("searchStateButton").textContent = "";
    document.getElementById("searchCountyButton").innerText = document.getElementById("searchCountyButton").textContent = "";
    document.getElementById("searchCityButton").innerText = document.getElementById("searchCityButton").textContent = "";
    document.getElementById("searchPostalButton").innerText = document.getElementById("searchPostalButton").textContent = "";
    
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    if(selectIndex) {
        var urlString = '/geo/cityList/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-");
        var cityList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(cityList);
        if (gobj.result != "0") {
            var cities = gobj.result.split(/\|/);
            var cityMenu = "<select id=\"geoSearchCity\" name=\"geoSearchCity\" class=\"geoSearchCity\" onChange=\"geoSearchCityChange(); return 1;\"><option value=\"0\">- Select a City -</option>";
            for(var i = 0;i < cities.length;i++){
                if (cities[i] !== "") {
                    cityMenu = cityMenu + "<option value=\"" + cities[i] + "\">" + cities[i] + "</option>";
                }
            }
            cityMenu = cityMenu + "</select>";
            var searchURL = '/workshops/geo/earth/united-states/' + stateName.replace(" ", "-") + "/" + countyName.replace(" ", "-");
            var searchButton = "<a href=\"" + searchURL + "\" class=\"btn btn-success btn-small\">Go to County</a> ";
            document.getElementById("searchCountyButton").innerHTML = searchButton;
            document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
            document.getElementById("searchCitySelect").innerHTML = cityMenu; 
        }
    }
}


function geoSearchStateChange(){
    var selectIndex = document.getElementById("geoSearchState").selectedIndex;
    var stateSelect = document.getElementById("geoSearchState");
    var stateName = stateSelect.options[selectIndex].value;
    document.getElementById("searchCountryButton").innerText = document.getElementById("searchCountryButton").textContent = "";
    document.getElementById("searchStateButton").innerText = document.getElementById("searchStateButton").textContent = "";
    document.getElementById("searchCountyButton").innerText = document.getElementById("searchCountyButton").textContent = "";
    document.getElementById("searchCityButton").innerText = document.getElementById("searchCityButton").textContent = "";
    document.getElementById("searchPostalButton").innerText = document.getElementById("searchPostalButton").textContent = "";
    
    document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
    if(selectIndex) {
        var urlString = '/geo/countyList/united-states/' + stateName.replace(" ", "-");
        var countyList = $.ajax({
            type : 'POST',
            async : false,
            url  : urlString
        }).responseText;
        var gobj = jQuery.parseJSON(countyList);
        if (gobj.result != "0") {
            var counties = gobj.result.split(/\|/);
            var countyMenu = "<select id=\"geoSearchCounty\" name=\"geoSearchCounty\" class=\"geoSearchCounty\" onChange=\"geoSearchCountyChange(); return 1;\"><option value=\"0\">- Select a County -</option>";
            for(var i = 0;i < counties.length;i++){
                if (counties[i] !== "") {
                    countyMenu = countyMenu + "<option value=\"" + counties[i] + "\">" + counties[i] + "</option>";
                }
            }
            countyMenu = countyMenu + "</select>";
            var searchURL = '/workshops/geo/earth/united-states/' + stateName.replace(" ", "-");
            var searchButton = "<a href=\"" + searchURL + "\" class=\"btn btn-success btn-small\">Go to State</a>";
            document.getElementById("searchStateButton").innerHTML = searchButton;
            document.getElementById("searchCountySelect").innerHTML = countyMenu;  
        }
    }
}

function geoSearchCountryChange(){
    var selectIndex = document.getElementById("geoSearchCountry").selectedIndex;
    document.getElementById("searchCountryButton").innerText = document.getElementById("searchCountryButton").textContent = "";
    document.getElementById("searchStateButton").innerText = document.getElementById("searchStateButton").textContent = "";
    document.getElementById("searchCountyButton").innerText = document.getElementById("searchCountyButton").textContent = "";
    document.getElementById("searchCityButton").innerText = document.getElementById("searchCityButton").textContent = "";
    document.getElementById("searchPostalButton").innerText = document.getElementById("searchPostalButton").textContent = "";
    
    document.getElementById("searchStateSelect").innerText = document.getElementById("searchStateSelect").textContent = "";
    document.getElementById("searchCountySelect").innerText = document.getElementById("searchCountySelect").textContent = "";
    document.getElementById("searchCitySelect").innerText = document.getElementById("searchCitySelect").textContent = "";
    document.getElementById("searchPostalSelect").innerText = document.getElementById("searchPostalSelect").textContent = "";
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
            var stateMenu = "<select id=\"geoSearchState\" name=\"geoSearchState\" class=\"geoSearchState\" onChange=\"geoSearchStateChange(); return 1;\"><option value=\"0\">- Select a State -</option>";
            for(var i = 0;i < states.length;i++){
                if (states[i] !== "") {
                    stateMenu = stateMenu + "<option value=\"" + states[i] + "\">" + states[i] + "</option>";
                }
            }
            var searchURL = '/workshops/geo/earth/united-states';
            var searchButton = "<a href=\"" + searchURL + "\" class=\"btn btn-success btn-small\">Go to Country</a>";
            stateMenu = stateMenu + "</select>";
            document.getElementById("searchStateSelect").innerText = document.getElementById("searchStateSelect").textContent = "";
            document.getElementById("searchStateSelect").innerHTML = stateMenu;            
            document.getElementById("searchCountryButton").innerHTML = searchButton;
        }
    }
}

