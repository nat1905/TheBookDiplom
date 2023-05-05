"""Create context processsor for year.
"""
from django.utils import timezone


def year(request):
    return {
        'year': timezone.now().year
    }
