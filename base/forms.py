from django.forms import ModelForm
from .models import State



class StateForm(ModelForm):
    class Meta:
        model = State
        fields = '__all__'
        exclude =['host']