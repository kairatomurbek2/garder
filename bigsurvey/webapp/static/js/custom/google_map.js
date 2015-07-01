var GoogleMap = {
    mapHolder: null,
    latitudeInput: null,
    longitudeInput: null,
    notificationLabel: null,
    map: null,
    latitude: null,
    longitude: null,
    center: null,
    marker: null,

    initialize: function (isMarkerDraggable) {
        this.map = this.getMap();
        this.mapHolder.bind('contextmenu', function (e) {
            e.preventDefault();
        });
        this.marker = this.getMarker(isMarkerDraggable);

        try {
            this.latitudeInput.change(this.inputChanged.bind(this));
            this.longitudeInput.change(this.inputChanged.bind(this));
        } catch (e) {

        }
    },

    getMap: function () {
        var options = this.getOptions();
        return new google.maps.Map(this.mapHolder.get(0), options);
    },

    getOptions: function () {
        this.center = this.getCenter();
        return {
            center: this.center,
            zoom: 15,
            scrollwheel: true,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false,
            navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL}
        };
    },

    getCenter: function () {
        if (this.latitude == null || this.longitude == null) {
            this.setCenterCoords();
        }
        return new google.maps.LatLng(this.latitude, this.longitude);
    },

    setCenterCoords: function () {
        // Try to get coordinates from form inputs
        // If form inputs are empty or incorrect then fall back to geolocation
        try {
            var latitudeInputValue = this.latitudeInput.val();
            var longitudeInputValue = this.longitudeInput.val();
            if (!$.isNumeric(latitudeInputValue) || !$.isNumeric(longitudeInputValue)) {
                throw new Error('Values in form fields are not correct');
            }
            this.latitude = parseFloat(latitudeInputValue);
            this.longitude = parseFloat(longitudeInputValue);
        } catch (e) {
            this.setDefaultCenterCoords();
        }
    },

    setDefaultCenterCoords: function () {
        try {
            navigator.geolocation.getCurrentPosition(geolocationSuccessCallback.bind(this), geolocationErrorCallback.bind(this));
        } catch (e) {
            this.notificationLabel.text("Geolocation is not supported by your browser.");
        }
    },

    getMarker: function (isMarkerDraggable) {
        var marker = new google.maps.Marker({
            position: this.center,
            map: this.map,
            draggable: isMarkerDraggable,
            title: "Hazard's location"
        });
        if (isMarkerDraggable) {
            var draggedCallback = function () {
                this.latitude = marker.position.lat();
                this.longitude = marker.position.lng();
                this.setInputValues();
            };

            var rightClickedCallback = function (event) {
                this.latitude = event.latLng.lat();
                this.longitude = event.latLng.lng();
                this.setInputValues();
                this.marker.setPosition(event.latLng);
            };

            google.maps.event.addListener(marker, 'drag', draggedCallback.bind(this));
            google.maps.event.addListener(this.map, 'rightclick', rightClickedCallback.bind(this));
        }

        return marker;
    },

    setInputValues: function () {
        this.latitudeInput.val(this.latitude);
        this.longitudeInput.val(this.longitude);
    },

    inputChanged: function () {
        var latitudeInputValue = this.latitudeInput.val();
        var longitudeInputValue = this.longitudeInput.val();
        if (!$.isNumeric(latitudeInputValue) || !$.isNumeric(longitudeInputValue)) {
            return;
        }
        this.setCoords(parseFloat(latitudeInputValue), parseFloat(longitudeInputValue));
    },

    setCoords: function (latitude, longitude, redraw) {
        if (redraw == undefined) {
            redraw = true;
        }
        this.latitude = latitude;
        this.longitude = longitude;
        if (redraw) {
            this.center = new google.maps.LatLng(this.latitude, this.longitude);
            this.setInputValues();
            this.centerChanged();
        }
    },

    centerChanged: function () {
        this.map.setCenter(this.center);
        this.marker.setPosition(this.center);
    }
};

var geolocationSuccessCallback = function (position) {
    this.setCoords(position.coords.latitude, position.coords.longitude);
};

var geolocationErrorCallback = function (error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            this.notificationLabel.text("Geolocation permission denied.");
            break;
        case error.POSITION_UNAVAILABLE:
            this.notificationLabel.text("Position unavailable, please, try again later.");
            break;
        case error.TIMEOUT:
            this.notificationLabel.text("Geolocation takes too long, please, try again later.");
            break;
        default:
            this.notificationLabel.text("Unknown geolocation error, please, try again later.");
    }
    this.setCoords(0, 0);
};