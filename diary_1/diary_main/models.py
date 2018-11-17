from django.db import models
from datetime import date
   
class User(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    img = models.ImageField(upload_to='img',default="img/picture.jpg")
    realname=models.CharField(max_length=20,default="")
    sex=models.CharField(max_length=2,default="")
    birthday=models.DateField(default=date(1970,1,1))
    telephone=models.CharField(max_length=11,default="")
    def __str__(self):
        return self.username
        
class Diary(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    diary_text=models.TextField()
    simp_text=models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    public=models.BooleanField(default=True)
    def __str__(self):
        return self.simp_text
# Create your models here.
