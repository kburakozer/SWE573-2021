from django import forms
from .models import Tag
from dal import autocomplete


class Tag_form(forms.ModelForm):
    custom_tag = forms.CharField(max_length=50, empty_value="")
    class Meta:
        model = Tag
        fields = ['tag_name']
        widgets = {
            'tag_name':forms.TextInput(attrs={'size': '40'}),      
        }
    


