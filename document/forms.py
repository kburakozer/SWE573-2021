from django import forms
from .models import Tag

class Tag_form(forms.ModelForm):
     class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'tag_name':forms.TextInput(attrs={'class':'form-control'}),
            'tag_url':forms.TextInput(attrs={'class':'form-control'}),        
        }