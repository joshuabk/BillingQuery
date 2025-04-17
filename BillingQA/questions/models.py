from django.db import models

# Create your models here.

class billingQuestion(models.Model):
    Date = models.DateTimeField(auto_now_add=True)
    Type = models.CharField(max_length=25, null = True)
    Questioner = models.CharField(max_length=25, null = True)
    questionerEmail = models.CharField(max_length=25, default = '')
    Content = models.CharField(max_length=300, default  = '')
    Answer = models.CharField(max_length=300, null = True)
    Answered = models.BooleanField(default = False)
    Title = models.CharField(max_length=100, default  = '')
    
    def __str__(self):
        return self.billingQuestion

