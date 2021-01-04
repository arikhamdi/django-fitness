from .models import Banner


def get_banner(request):
    return {'banner': Banner.objects.all()[:5]}
