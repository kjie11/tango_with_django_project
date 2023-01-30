from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm




def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]

    # page_list = list(Page.objects.order_by('-views')[:5])


    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages']=page_list
    # context_dict['boldmessage2']='There are no pages present.'

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

def add_category(request):
    if request.user.is_authenticated:
        form = CategoryForm()
    # A HTTP POST?
        if request.method == 'POST':
            form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
        # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            print(form.errors)
            # Will handle the bad form, new form, or no form supplied cases.
            # Render the form with error messages (if any).
            return render(request, 'rango/add_category.html', {'form': form})
    else:
        return redirect('rango:login')

def add_page(request, category_name_slug):
    if request.user.is_authenticated:
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None
        # You cannot add a page to a Category that does not exist...
        if category is None:
            return redirect('/rango/')
        form = PageForm()
        if request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views = 0
                    page.save()
                    return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
            else:
                print(form.errors)
        context_dict = {'form': form, 'category': category}


        return render(request, 'rango/add_page.html', context=context_dict)
    else:
        return redirect('rango:login')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:

            print(user_form.errors, profile_form.errors)
    else:

        user_form = UserForm()

        profile_form = UserProfileForm()
    return render(request, 'rango/register.html',context = {'user_form': user_form, 'profile_form': profile_form,'registered': registered})

def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")


        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    # return HttpResponse("Since you're logged in, you can see this text!")
    return render(request,'rango/restricted.html')

@login_required
def user_logout(request):
        # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))


