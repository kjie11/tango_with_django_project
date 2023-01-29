from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page




def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
    # page_list = list(Page.objects.order_by('-views')[:5])


    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages']=page_list
    context_dict['boldmessage2']='There are no pages present.'

    HttpResponse("Rango says here is the about page.")

    return render(request, 'rango/index.html', context=context_dict)



def about(request):

    # context_dict = {'boldmessage': 'This tutorial has been put together by Ruyan Qin.'}
    context_dict = {'boldmessage': 'Rango says here is the about page. This tutorial has been put together by Ruyan Qin.'}

    return render_to_response('rango/about.html',context = context_dict)
    # return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_slug):

    context_dict = {}
    try:

        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

# def show_page(request, page_name_slug):
#     context_dict={}
#     try:
#         page=Page.object.get(slug=page_name_slug)
#
#     except Page.DoseNotExist:
#         context_dict['pages'] = None
#     return render(request,'rango/page.html',context = context_dict)





