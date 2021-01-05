from .models import Slider


def get_slider(request):
    return {'slider': Slider.objects.all().order_by('-created')[:5]}
