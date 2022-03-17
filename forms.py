from django.forms import ModelForm, Textarea 
from apitest.models import Case
class AuthorForm(ModelForm): 
    class Meta: 
            model = Case
            fields = ('response') 
            widgets = {
                'response': Textarea(attrs={'cols': 100}),
            }

