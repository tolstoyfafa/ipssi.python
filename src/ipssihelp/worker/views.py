from django.contrib.auth import get_user, decorators, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from .forms import SignupForm, UpdateProfileForm, LoginWorkerForm
from .models import Ad, User
from django.db.models import Count
from .methods import get_ads
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    template = loader.get_template('home.html')
    top_users = User.objects.annotate(ads=Count('ad')).order_by('-ads')[:5]
    print(top_users)
    context = {
        'top_users': top_users,
        'supply_top_ads': get_ads(True,'supply'),
        'demand_top_ads': get_ads(True,'demand')
    }
    return HttpResponse(template.render(context, request))


@csrf_protect
@requires_csrf_token
def signup(request):
    template = loader.get_template('accounts/signup.html')

    user = get_user(request)
    if not user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            context = {
                'form': form
            }
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password1']
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect('worker:home')
        else:
            form = SignupForm()
            context = {
                'form': form
            }

        return HttpResponse(template.render(context, request))

    return redirect('worker:home')

@csrf_protect
@requires_csrf_token
def login_worker(request):
    template = loader.get_template('accounts/login.html')
    user = get_user(request)
    if not user.is_authenticated:
        if request.method == 'POST':
            form =  LoginWorkerForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                login(request, user)
                return redirect('worker:profile')
        else:
            form = LoginWorkerForm()
            context = {
            'form': form
            }
        return HttpResponse(template.render(context, request))
    return redirect('worker:home')

@decorators.login_required(login_url='/accounts/login')
@csrf_protect
@requires_csrf_token
def worker_profile(request):
    template = loader.get_template('accounts/profile.html')
    user = get_user(request)
    form = UpdateProfileForm(initial={
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone': user.phone})
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email_name = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.save(update_fields=['first_name','last_name','phone','email'])
            print("sucess")
        else:
            print("error")
    else:
        UpdateProfileForm()
        context = {
            'form': form
        }
    return HttpResponse(template.render(context, request))


def supply(request):
    template = loader.get_template('ad/supply.html')
    query = request.GET.get('q')
    results = None
    if query:
        results = Ad.objects.filter(Q(title__icontains=query) | Q(description__icontains=query),type='supply' ,status__exact='online')
    else:
        results = get_ads(False,'supply')
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'ads': page_obj
    }
    return HttpResponse(template.render(context, request))

def demand(request):
    template = loader.get_template('ad/demand.html')
    query = request.GET.get('q')
    results = None
    if query:
        results = Ad.objects.filter(Q(title__icontains=query) | Q(description__icontains=query),type='demand' ,status__exact='online')
    else:
        results = get_ads(False,'demand')
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'ads': page_obj
    }
    return HttpResponse(template.render(context, request))


def detail(request, slug):
    template = loader.get_template('ad/detail.html')
    try:
        get_ad = Ad.objects.get(slug=slug)
        context = {
            'ad': get_ad
        }
    except ObjectDoesNotExist:
        context = {
            'ad': None
        }

    return HttpResponse(template.render(context, request))

@decorators.login_required(login_url='/accounts/login')
def getAllAds(request):
    """get all ads of an author"""
    template = loader.get_template('accounts/ads.html')
    user = get_user(request)
    if user:
        myads = user.ad_set.filter(type='demand', status__exact='online')
        print(myads)
    context = {
        'ads': myads
    }
    return HttpResponse(template.render(context, request))

@decorators.login_required(login_url='/accounts/login')
def protected_page_view(request):
    template = loader.get_template('your_template.html')
    # something
    return HttpResponse(template.render(None, request))
