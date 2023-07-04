from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Markpost(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    file = models.ManyToManyField('Document', blank=True)
    image = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mark-detail', kwargs={'mpost_id':self.pk})

class Markcomments(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Markpost', on_delete=models.CASCADE, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True , related_name='rep')

    @property
    def children(self):
        return Markcomments.objects.filter(parent = self).order_by('-date').all()
 
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return "Comment {}".format(self.content)

class Image(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='marketing-pic')
    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/marketing/%Y/%m/%d')

    @property
    def furl(self):
        return self.docfile.url