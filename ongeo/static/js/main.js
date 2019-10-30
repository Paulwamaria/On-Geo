function isGeo(){
    if("geolocation" in navigator){
    console.log("geolocation is available");
    document.getElementById("demo").innerHTML = "geolocation is available";
}else{
    console.log("Geolocation not available");
    document.getElementById("demo").innerHTML = "geolocation is unavailable";
}

}
navigator.geolocation.getCurrentPosition(function(position) {
    console.log(position.coords.latitude, position.coords.longitude);
  });