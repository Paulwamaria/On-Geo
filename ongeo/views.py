from django.shortcuts import render

def index(request):
    message = "Welcome to On-Geo Manager"


    context = {
        "message":message
    }
    return render(request,"ongeo/index.html", context)