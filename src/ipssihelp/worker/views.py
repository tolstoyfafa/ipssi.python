from django.contrib.auth import get_user, decorators, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from .forms import SignupForm, UpdateProfileForm
from .models import Ad, User
from django.db.models import Count
from .methods import get_ads


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

#"""@decorators.login_required(login_url='/your_login_page')""""
@csrf_protect
@requires_csrf_token
def worker_profile(request, user_id):
    template = loader.get_template('accounts/profile.html')
    id = int(user_id)
    user = User.objects.get(id=id)
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
    context = {
        'supply_ads': get_ads(False,'supply')
    }
    return HttpResponse(template.render(context, request))


def demand(request):
    template = loader.get_template('ad/demand.html')
    context = {
        'demand_ads': get_ads(False,'demand')
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


@decorators.login_required(login_url='/your_login_page')
def protected_page_view(request):
    template = loader.get_template('your_template.html')
    # something
    return HttpResponse(template.render(None, request))
