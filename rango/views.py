from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render




def index(request):
# Construct a dictionary to pass to the template engine as its context.
# Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Rango says here is the about page.'}
# Return a rendered response to send to the client.
# We make use of the shortcut function to make our lives easier.
# Note that the first parameter is the template we wish to use.
    HttpResponse("Rango says here is the about page.")

    return render(request, 'rango/index.html', context=context_dict)



def about(request):

    # context_dict = {'boldmessage': 'This tutorial has been put together by Ruyan Qin.'}
    context_dict = {'boldmessage': 'Rango says here is the about page.'}
    # HttpResponse("Rango says here is the about page.")
    return render_to_response('rango/about.html',context = context_dict)
    # return render(request, 'rango/about.html', context = context_dict)


