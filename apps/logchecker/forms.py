from django import forms
from apps.logchecker.models import District, Log, STATUS
from django.contrib.auth import get_user_model
User = get_user_model()

class DistrictModelForm(forms.ModelForm):
    
    status = forms.ChoiceField(choices = STATUS, widget=forms.Select(attrs={'class': 'form-control'},))
    user = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'), widget=forms.Select(attrs={'class': 'form-control'},))

    class Meta:
        model = District
        fields = ('user', 'name', 'psid', 'server', 'status')
        widgets = {
            # 'user': forms.TextInput(attrs={'class': 'form-control', 
            #                                     'autocomplete': 'off'}),
            'name': forms.TextInput(attrs={'class': 'form-control',
                                                'autocomplete': 'off',
                                                'placeholder': 'Ingresar Entity Name...'}),
            'server': forms.TextInput(attrs={'class': 'form-control',
                                                'autocomplete': 'off',
                                                'placeholder': 'Ingresar Server (format: 4-1)...'}),
            'psid': forms.NumberInput(attrs={'class': 'form-control',
                                                'autocomplete': 'off'}),
            'created': forms.DateInput(format=('%Y-%m-%d'),
                                      attrs={'type': 'date', 'class': 'form-control',
                                             'placeholder': 'Ingrese AAAA-MM-DD'}),
            'status': forms.Select(attrs={'class': "form-control", 'autocomplete': "off", }),
        }



# pydantic