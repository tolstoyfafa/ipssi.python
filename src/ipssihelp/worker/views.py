from django.contrib.auth import get_user, decorators, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from .forms import SignupForm
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
