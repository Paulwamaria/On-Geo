$(document).ready(function () {
    navigator.geolocation.getCurrentPosition(onPositionUpdate);
});


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

            if (data.distance < 1) {
                $("#fname").val(data.user_data.first_name)
                $("#lname").val(data.user_data.last_name)
                console.log(data.user_data);
                console.log("You are within Moringa Vicinity!");
                $("ol#inattendance").prepend(data.user_data.first_name + " " + data.user_data.last_name);
                $.ajax({
                    url:'/save_to_db/',
                    method:'GET',
                    data:{
                       'first_name':data.user_data.first_name,
                        'last_name':data.user_data.last_name
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
            } else if (data.distance > 1) {
                document.getElementById("outb").innerHTML = 'We we are sorry the system cant check you in, you are not Within Moringa'
                console.log("Sorry You are out of bound");
            }
        });
    console.log(name);


}