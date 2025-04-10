from django.db import models

# Create your models here.

class billingQuestion(models.Model):
    questionDate = models.DateTimeField(auto_now_add=True)
    questionType = models.CharField(max_length=25, null = True)
    questionContent = models.CharField(max_length=300)
    questionAnswer = models.CharField(max_length=300, null = True)

    def __str__(self):
        return self.billingQuestion

