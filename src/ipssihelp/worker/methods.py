from .models import Ad, User
from django.core.paginator import Paginator
from django.db.models import Q

def get_ads(top, ads_type):
    if top:
        return Ad.objects.filter(type=ads_type, status__exact='online').order_by('-created')[:5]
    else:
        return Ad.objects.filter(type=ads_type, status__exact='online')

def get_ads_common(request, ads_type, my_status):
    query = request.GET.get('q')
    results = None
    if query:
        results = Ad.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), type=ads_type ,status__exact=my_status)
    else:
        results = get_ads(False,'demand')
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'ads': page_obj
    }
    return context
