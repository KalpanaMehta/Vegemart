from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication.models import User,Profile

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})

    class Meta:
        model = User
        fields = ['username', 'email']

class Profileform(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Full Name'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Bio'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Phone Number'}))
    class Meta:
        model = Profile
        fields = ["full_name","image","bio","phone"]