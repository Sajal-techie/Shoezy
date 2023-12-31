from django import forms
from .models import Address


class Adressform(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','country','state','district','town','house','land_mark','pincode','number','alternate_number']
        widgets = {
            'alternate_number': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'land_mark': forms.TextInput(attrs={'placeholder': 'Optional'})
        }
        
    def __init__(self, *args, **kwargs):
            super(Adressform, self).__init__(*args,**kwargs)
            self.fields['alternate_number'].required = False 
            self.fields['land_mark'].required = False 
            