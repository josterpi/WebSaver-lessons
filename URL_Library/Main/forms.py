from django import forms
from Sign_up.models import UserContent

class URLForm(forms.ModelForm):
    class Meta:
        model = UserContent
        fields = ['name','url','description']
        # styles for form
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),

            'url': forms.TextInput(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'class': 'form-control'})
        }