from .models import Banner


def get_banner(request):
    return {'slider': Banner.objects.all().order_by('-created')[:5]}
