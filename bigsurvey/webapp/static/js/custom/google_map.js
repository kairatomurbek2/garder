function showMap(latlon){
    var myOptions={
        center:latlon,
        zoom:15,
        scrollwheel:false,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        mapTypeControl:false,
        navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}
    };
    var map = new google.maps.Map(document.getElementById("mapholder"), myOptions);
    return new google.maps.Marker({
        position:latlon,
        map:map,
        draggable:true,
        title:"You are here"
    });
}

function showFormMap(position){
    var latInput = document.getElementById('id_latitude');
    var lonInput = document.getElementById('id_longitude');
    var latitude = latInput.value;
    var longitude = lonInput.value;
    if(latitude == 0 && longitude == 0){
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
        latInput.value = latitude;
        lonInput.value = longitude;
    }
    var latlon = new google.maps.LatLng(latitude, longitude);
    var marker = showMap(latlon);
    google.maps.event.addListener(
        marker,
        'drag',
        function() {
            latInput.value = marker.position.lat();
            lonInput.value = marker.position.lng();
        }
    );
}

function showError(error) {
    var messageField = document.getElementById("notification");
    switch(error.code) {
        case error.PERMISSION_DENIED:
            messageField.innerHTML = "Geolocation permission denied.";
            break;
        case error.POSITION_UNAVAILABLE:
            messageField.innerHTML = "Position unavailable, please, try again later.";
            break;
        case error.TIMEOUT:
            messageField.innerHTML = "Geolocation takes too long, please, try again later.";
            break;
        default:
            messageField.innerHTML = "Unknown geolocation error, please, try again later.";
    }
}

function getLocation(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showFormMap, showError);
    } else {
        var messageField = document.getElementById("notification");
        messageField.innerHTML = "Geolocation is not supported by your browser.";
    }
}

function showDetailMap(){
    var lat = document.getElementById('latitude').textContent;
    var lon = document.getElementById('longitude').textContent;
    var latlon = new google.maps.LatLng(lat, lon);
    showMap(latlon);
}