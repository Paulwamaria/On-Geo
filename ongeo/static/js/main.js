$(document).ready(function () {
    if (!navigator.geolocation) {
        showAttendanceWarning("Your browser does not support location check-in.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        onPositionUpdate,
        showLocationWarning,
        {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 20000
        }
    );
});

// function getLoc(){om
//     navigator.geolocation.getCurrentPosition(onPositionUpdate);
// }


function onPositionUpdate(position) {
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var accuracy = position.coords.accuracy;

    console.log("My Position is, " + lat + " " + long + " accuracy: " + accuracy + "m");
    $.ajax({
            url: '/distance/',
            data: {
                'user_latitude': lat,
                'user_longitude': long,
            },
            dataType: 'json'
            // success : function() {
            //     document.getElementById("demo").innerHTML = ("Your Latitude: "+ lat + " < " +" Your Longitude: " + long);
            //     console.log("Your Latitude:"+ lat + " " +" Your Longitude:" + long);


            // }
        })

        .done(function (data) {
                nams = $("#lname").val(data.last_name)

            if (data.distance <= 50) {
                console.log(data.distance)
         
                $(".card-b").show()
                $("ol#inattendance").prepend("<li>"+ data.user_data.first_name + " " + data.user_data.last_name + "</li>");
                $.ajax({
                    url:'/save_to_db/',
                    method:'GET',
                    data:{
                       'first_name':data.user_data.first_name,
                        'last_name':data.user_data.last_name,
                      
                    },
                    statusCode:{
                        404:function(){
                            console.log('NOT FOUND') 
                        },
                        500:function(){
                            console.log('INTERNAL SERVER ERROR') 
                        }
                    }
                })
                .done(function(data){
                    if(data.saved){
                        window.location.replace('/')
                    }
                })
            } else if (data.distance > 50) {
                var warning = document.getElementById("attendance-warning");
                var warningMessage = document.getElementById("outb");
                var distanceFromCheckpoint = formatDistance(data.distance);
                var accuracyMessage = formatAccuracy(accuracy);

                warningMessage.textContent = "We are sorry, the system can't check you in because you are " + distanceFromCheckpoint + " from the checkpoint. The allowed range is 50 m." + accuracyMessage;
                warning.removeAttribute("hidden");
                warning.style.display = "flex";
            }
        })
        .fail(function (xhr) {
            var message = "We could not check your distance from the checkpoint.";

            if (xhr.responseJSON && xhr.responseJSON.error) {
                message = xhr.responseJSON.error;
            }

            showAttendanceWarning(message);
        });
}

function formatDistance(distanceInMeters) {
    var meters = Number(distanceInMeters);

    if (!Number.isFinite(meters)) {
        return "outside the allowed range";
    }

    if (meters >= 1000) {
        return (meters / 1000).toFixed(2) + " km";
    }

    return Math.round(meters) + " m";
}

function formatAccuracy(accuracyInMeters) {
    var meters = Number(accuracyInMeters);

    if (!Number.isFinite(meters)) {
        return "";
    }

    return " Your browser reported location accuracy of +/- " + formatDistance(meters) + ".";
}

function showLocationWarning(error) {
    var message = "We could not access your location. Enable location permissions to check in.";

    if (error && error.code === error.TIMEOUT) {
        message = "We could not get a precise location in time. Move near a window or outside, then try again.";
    }

    showAttendanceWarning(message);
}

function showAttendanceWarning(message) {
    var warning = document.getElementById("attendance-warning");
    var warningMessage = document.getElementById("outb");

    if (!warning || !warningMessage) {
        return;
    }

    warningMessage.textContent = message;
    warning.removeAttribute("hidden");
    warning.style.display = "flex";
}
