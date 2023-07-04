from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from django.urls import reverse

class post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    post_date=models.DateTimeField(default=timezone.now)
    post_update=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
       # return '/detail/{}' .format(self.pk)
       return reverse('detail' , args=[self.pk])

    class Meta:
        ordering=('-post_date',)


class ProgramCommentNotifi(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User,related_name="not_to_p",on_delete=models.CASCADE,null=True)
    from_user = models.ForeignKey(User,related_name='not_from_p',on_delete=models.CASCADE,null=True)
    prg_post = models.ForeignKey("programming.Progrmpost", related_name="pp", on_delete=models.CASCADE,blank=True,null=True)
    prg_Comment = models.ForeignKey('programming.ProgrmComments',on_delete=models.CASCADE,null=True,related_name='pc',blank=True)
    date = models.DateTimeField(default=timezone.now)
    stuff_name = models.TextField(max_length=20,default='Alaa')
    user_has_seen = models.BooleanField(default=False)

class MarkCommentNotifi(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User,related_name="not_to_m",on_delete=models.CASCADE,null=True)
    from_user = models.ForeignKey(User,related_name='not_from_m',on_delete=models.CASCADE,null=True)
    mrk_post = models.ForeignKey("marketing.Markpost", related_name="mp", on_delete=models.CASCADE,blank=True,null=True)
    mrk_Comment = models.ForeignKey('marketing.Markcomments',on_delete=models.CASCADE,null=True,related_name='mc',blank=True)
    date = models.DateTimeField(default=timezone.now)
    stuff_name = models.TextField(max_length=20,default='Alaa')
    user_has_seen = models.BooleanField(default=False)

class GraphCommentNotifi(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User,related_name="not_to_g",on_delete=models.CASCADE,null=True)
    from_user = models.ForeignKey(User,related_name='not_from_g',on_delete=models.CASCADE,null=True)
    gr_post = models.ForeignKey("graphdesign.Graphpost", related_name="gp", on_delete=models.CASCADE,blank=True,null=True)
    gr_Comment = models.ForeignKey('graphdesign.GraphComments',on_delete=models.CASCADE,null=True,related_name='gc',blank=True)
    date = models.DateTimeField(default=timezone.now)
    stuff_name = models.TextField(max_length=20,default='Alaa')
    user_has_seen = models.BooleanField(default=False)