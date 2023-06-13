from django import forms
from .models import Booking 

FAVOURITE_DISHES = [
    ('italian' , 'Italian'),
    ('greek' , 'Greek'),
    ('turkish' , 'Turkish'),
]

class DemoForm(forms.Form):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    email = forms.EmailField(label='Enter an email address')
    reservation_date = forms.DateField()
    favourite_dish = forms.ChoiceField(choices=FAVOURITE_DISHES, widget=forms.RadioSelect)


class ApplicationForm(forms.Form):  
    name = forms.CharField(label='Name of Applicant', max_length=50)  
    address = forms.CharField(label='Address', max_length=100)  
    posts = (('Manager', 'Manager'),('Cashier', 'Cashier'),('Operator', 'Operator'))  
    field = forms.ChoiceField(choices=posts)
 
class BookingForm(forms.ModelForm): 
    class Meta: 
        model = Booking 
        fields = '__all__'