from django.db import models
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    contain="hello"
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
# Create your models here.
