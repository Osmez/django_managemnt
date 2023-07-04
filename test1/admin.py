from django.contrib import admin
from .models import post,ProgramCommentNotifi,MarkCommentNotifi,GraphCommentNotifi

admin.site.register(post)
admin.site.register(ProgramCommentNotifi)
admin.site.register(MarkCommentNotifi)
admin.site.register(GraphCommentNotifi)