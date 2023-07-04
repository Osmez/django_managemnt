from http.client import ACCEPTED
from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import Value
from django.db.models.signals import post_save
from PIL import Image


        
class Requests(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Specialization = models.CharField(max_length=30)
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    accepted = models.BooleanField(default=False)
    def __str__(self):
        return self.username

    def settrue():
        return True


class Profile(models.Model):
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{} profile.' .format(self.user.username)

    def save(self ,*args,**kwarg):
        super().save(*args,**kwarg)

        img=Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

def create_profile(sender,**kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])

post_save.connect(create_profile,sender=User)

class Sections(models.Model):
    CHOICE1 = 'Marketing'
    CHOICE2 = 'GraphicDesign'
    CHOICE3 = 'Programming'

    SECTIONS_CHOICES= (
        (CHOICE1 , 'Marketing'),
        (CHOICE2 , 'GraphicDesign'),
        (CHOICE3 , 'Programming'),
    )



