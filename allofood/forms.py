
from django import forms
from django.forms import TextInput, PasswordInput

import allofood


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = allofood.models.User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password', 'telephone', 'address')
        widgets = {
            'telephone': TextInput(),
            'password': PasswordInput()
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data


class LoginForm(forms.Form):

    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    fields = ['email', 'password']


class OrderForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput())
    telephone = forms.CharField(min_length=9, widget=forms.NumberInput(attrs={'class' : 'numberinput'}))
    password = forms.CharField(widget=forms.PasswordInput())
    fields = ['address', 'telephone', 'password']

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        telephone = cleaned_data.get('telephone')
        if len(str(telephone)) < 9:
            self.add_error('telephone', "9 please")
            raise forms.ValidationError("9 please")

        return cleaned_data
