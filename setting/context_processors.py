from .models import Setting


def general(request):
    gs = {}
    for v in Setting.objects.filter(type='general'):
        gs[v.value] = v.content
    return gs


def admin(request):
    gs = {}
    for v in Setting.objects.filter(type='admin'):
        gs[v.value] = v.content
    return gs
