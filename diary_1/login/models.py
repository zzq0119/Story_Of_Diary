from django.db import models

# Create your models here.
class User(models.Model):
    user_nickname=models.CharField(max_length=30)
    user_password=models.CharField(max_length=30)
    
#CREATE TABLE "login_users" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_nickname" varchar(30) NOT NULL, "user_password" varchar(30) NOT NULL);

