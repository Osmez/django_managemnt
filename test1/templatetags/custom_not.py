from django import template
from test1.models import ProgramCommentNotifi,MarkCommentNotifi,GraphCommentNotifi
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('test1/show_notification.html', takes_context=True)
def show_notif(context):
    request_user = context['request'].user
    notification = ProgramCommentNotifi.objects.filter(to_user=request_user).exclude(user_has_seen=True).exclude(from_user=request_user).order_by('-date')
    return {'notification': notification}

@register.inclusion_tag('test1/show_notification_m.html', takes_context=True)
def show_mnotif(context):
    request_user = context['request'].user
    notification = MarkCommentNotifi.objects.filter(to_user=request_user).exclude(user_has_seen=True).exclude(from_user=request_user).order_by('-date')
    return {'notification': notification}

@register.inclusion_tag('test1/show_notification_g.html', takes_context=True)
def show_gnotif(context):
    request_user = context['request'].user
    notification = GraphCommentNotifi.objects.filter(to_user=request_user).exclude(user_has_seen=True).exclude(from_user=request_user).order_by('-date')
    return {'notification': notification}

@register.inclusion_tag('test1/stuff_notification.html', takes_context=True)
def stuff_notif(context):
    request_user = context['request'].user
    u = User.objects.get(id=17)
    pnot = ProgramCommentNotifi.objects.filter(to_user=u).exclude(user_has_seen=True).exclude(from_user=request_user).order_by('-date')
    mnot = MarkCommentNotifi.objects.filter(to_user=u).exclude(user_has_seen=True).exclude(from_user=request_user).order_by('-date')
    gnot = GraphCommentNotifi.objects.filter(to_user=u).exclude(user_has_seen=True).exclude(from_user=request_user).order_by('-date')

    return {'pnot': pnot,'mn':mnot,'gn':gnot}