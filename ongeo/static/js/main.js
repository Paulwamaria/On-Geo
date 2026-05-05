$(document).ready(function () {
    navigator.geolocation.getCurrentPosition(onPositionUpdate, showLocationWarning);
});

// function getLoc(){om
//     navigator.geolocation.getCurrentPosition(onPositionUpdate);
// }


function onPositionUpdate(position) {
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
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

                warningMessage.textContent = "We are sorry, the system can't check you in because you are outside the allowed range.";
                warning.removeAttribute("hidden");
                warning.style.display = "flex";
            }
        });
}

function showLocationWarning() {
    var warning = document.getElementById("attendance-warning");
    var warningMessage = document.getElementById("outb");

    if (!warning || !warningMessage) {
        return;
    }

    warningMessage.textContent = "We could not access your location. Enable location permissions to check in.";
    warning.removeAttribute("hidden");
    warning.style.display = "flex";
}
