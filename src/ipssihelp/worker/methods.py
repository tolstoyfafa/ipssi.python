from .models import Ad, User

def get_ads(top, ads_type):
    if top:
        return Ad.objects.filter(type=ads_type, status__exact='online').order_by('-created')[:5]
    else:
        return Ad.objects.filter(type=ads_type, status__exact='online')
