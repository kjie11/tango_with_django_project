from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context_dict={'boldmessage': 'Hello newRango!'}
    return render(request, 'newRango/newindex.html', context = context_dict)
    # return HttpResponse("Rango says hey there partner!")
# Create your views here.
def about(request):
    HttpResponse("'Rango says here is the about page.")
    context_dict={'boldmessage': 'This tutorial has been put together by Ruyan Qin.'}
    return render(request,'newRango/about.html',context = context_dict)
