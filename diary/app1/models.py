from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.username
class Diary(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    diary_text=models.CharField(max_length=1000)
    simp_text=models.CharField(max_length=20)
    public=models.BooleanField()
    def __str__(self):
        return self.simp_text
