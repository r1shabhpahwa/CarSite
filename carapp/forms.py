from django import forms
from carapp.models import OrderVehicle, Vehicle


class OrderVehicleForm(forms.ModelForm):
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'vehicles_ordered']
        labels = {'vehicles_ordered': 'Number of Vehicles Ordered'}
        widgets = {'buyer': forms.Select(attrs={'class': 'form-control'})}


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

class VehicleSearch(forms.Form):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
