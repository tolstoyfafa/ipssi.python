from django.contrib.auth import get_user, decorators, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from .forms import SignupForm
from .models import Ad


def home(request):
    template = loader.get_template('home.html')
    context = {
        'text': 'Home page'
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


def supply(request):
    template = loader.get_template('ad/supply.html')
    context = {
        'supply_ads': Ad.objects.filter(type='supply', status__exact='online')
    }
    return HttpResponse(template.render(context, request))


def demand(request):
    template = loader.get_template('ad/demand.html')
    context = {
        'demand_ads': Ad.objects.filter(type='demand', status__exact='online')
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
