# cadastro\context_processors.py

from core import settings


def global_context(request):
    return {
        'dono': settings.APP_OWNER,
    }
