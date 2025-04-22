from django import forms
from .models import billingQuestion
from datetime import datetime


class questionForm(forms.ModelForm):

    class Meta:
        model = billingQuestion
        fields = [ "Title","Questioner", "Content"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class answerForm(forms.ModelForm):

    class Meta:
        model = billingQuestion
        fields = ["Answer"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class editQuestionForm(forms.ModelForm):

    class Meta:
        model = billingQuestion
        fields= [ "Type", "Content", "Answer"]
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            