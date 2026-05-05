(function () {
    "use strict";

    function onReady(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback);
        } else {
            callback();
        }
    }

    function setStatus(status, message) {
        status.textContent = message;
    }

    function setLegacyLocation(widget, longitude, latitude) {
        if (!window.OpenLayers || !widget || !widget.map || !widget.layers || !widget.layers.vector) {
            return false;
        }

        var sourceProjection = new OpenLayers.Projection("EPSG:4326");
        var mapProjection = widget.map.getProjectionObject();
        var point = new OpenLayers.LonLat(longitude, latitude).transform(sourceProjection, mapProjection);
        var feature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(point.lon, point.lat));

        widget.deleteFeatures();
        widget.layers.vector.addFeatures([feature]);
        widget.map.setCenter(point, 16);
        widget.write_wkt(feature);

        if (widget.modifiable && widget.enableEditing) {
            widget.enableEditing();
        }

        return true;
    }

    function setModernLocation(widget, longitude, latitude) {
        if (!window.ol || !widget || !widget.map || !widget.featureOverlay) {
            return false;
        }

        var point = ol.proj.transform([longitude, latitude], "EPSG:4326", widget.map.getView().getProjection());
        var feature = new ol.Feature({geometry: new ol.geom.Point(point)});

        widget.clearFeatures();
        widget.featureOverlay.getSource().addFeature(feature);
        widget.map.getView().setCenter(point);
        widget.map.getView().setZoom(16);
        widget.serializeFeatures();

        return true;
    }

    onReady(function () {
        var field = document.getElementById("id_location");
        var map = document.getElementById("id_location_admin_map") || document.getElementById("id_location_div_map");

        if (!field || !map || !navigator.geolocation) {
            return;
        }

        var wrapper = document.createElement("div");
        wrapper.style.margin = "0 0 10px";

        var button = document.createElement("button");
        button.type = "button";
        button.className = "button";
        button.textContent = "Use current location";

        var status = document.createElement("span");
        status.style.marginLeft = "10px";
        status.style.color = "#5c6670";

        wrapper.appendChild(button);
        wrapper.appendChild(status);
        map.parentNode.insertBefore(wrapper, map);

        button.addEventListener("click", function () {
            button.disabled = true;
            setStatus(status, "Getting location...");

            navigator.geolocation.getCurrentPosition(
                function (position) {
                    var longitude = position.coords.longitude;
                    var latitude = position.coords.latitude;
                    var applied = setLegacyLocation(window.geodjango_location, longitude, latitude);

                    if (!applied) {
                        applied = setModernLocation(window.geodjango_location, longitude, latitude);
                    }

                    if (!applied) {
                        field.value = "POINT(" + longitude + " " + latitude + ")";
                        field.dispatchEvent(new Event("change", {bubbles: true}));
                    }

                    setStatus(status, "Location selected.");
                    button.disabled = false;
                },
                function () {
                    setStatus(status, "Could not access your location.");
                    button.disabled = false;
                },
                {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 15000
                }
            );
        });
    });
}());
