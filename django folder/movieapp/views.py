from django.shortcuts import render,render_to_response
from django.http import HttpRequest,HttpResponse

def index(request):
    print("I Am here")
    context = {
        'name': "Thor "
    }
    return render(request,'movieapp/design/design.html',context)
