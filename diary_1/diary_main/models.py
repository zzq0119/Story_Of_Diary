from django.db import models
from datetime import date,datetime
import django.utils.timezone as timezone
   
class User(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    img = models.FileField(upload_to='images',default="/media/images/picture.jpg")
    realname=models.CharField(max_length=20,default="")
    sex=models.CharField(max_length=2,default="")
    birthday=models.DateField(default=date(1970,1,1))
    telephone=models.CharField(max_length=11,default="")
    email=models.CharField(max_length=30,default="")
    def __str__(self):
        return self.username
        
class Diary(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    diary_text=models.TextField()
    simp_text=models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    title=models.CharField(max_length=50)
    public=models.BooleanField(default=False)
    def __str__(self):
        return self.simp_text
    def __iter__(self):
        return self
    def next(self):
                if self._i == 0:
                        self._i += 1
                        return self.name
                elif self._i == 1:
                        self._i += 1
                        return self.age
                else:
                        raise StopIteration()
       
class Comment(models.Model):
    diary=models.ForeignKey(Diary,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    pub_date=models.DateTimeField(default=datetime(1970,1,1,0,0,0))
    def __str__(self):
        return self.text
# Create your models here.
        
