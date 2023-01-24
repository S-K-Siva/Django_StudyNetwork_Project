from django.forms import ModelForm
from django import forms 
from .models import Room,User

from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['name','username','email','password1','password2']
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']
class UserUpdateForm(ModelForm):
    class Meta:
        model = User 
        fields = ['avatar','name','username','email','bio']
# class Userform(ModelForm):
#     bio = forms.CharField(label='Bio', max_length=100)
#     class Meta:
#         model = User 
#         fields = ['username','email','bio']

