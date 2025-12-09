from .models import CIO

def cios_processor(request):
    """
    Make all CIOs available as 'cios' in every template.
    """
    return {
        "cios": CIO.objects.all().order_by('-id')
    }
