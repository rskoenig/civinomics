
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
