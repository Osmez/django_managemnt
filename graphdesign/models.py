from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Graphpost(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=None,
    null=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ManyToManyField('Image', blank=True)
    file = models.ManyToManyField('Document', blank=True)

    def __str__(self):
        return self.title

class GraphComments(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Graphpost', on_delete=models.CASCADE, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True , related_name='rep')

    @property
    def children(self):
        return GraphComments.objects.filter(parent = self).order_by('-date').all()
 
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return "Comment {}".format(self.content)

class Image(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='graph-pic')
    
    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/graphic/%Y/%m/%d')

    @property
    def furl(self):
        return self.docfile.url