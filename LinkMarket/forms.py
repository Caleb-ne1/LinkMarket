from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import CustomUser, Product, Category, Business
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'role')

class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['image', 'name']
        


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
             'type': "file",
             'id': "file",
             'name': "image"
        })
        self.fields["name"].widget.attrs.update({
            'type':"text",
            'name': "name", 
            'class': "input"
        })
        
        self.fields["category"].widget.attrs.update({
            'type':"text",
            'name':"category",
            'class':"input"
        })
        
        self.fields["price"].widget.attrs.update({
            'type':"text", 
            'name':"price", 
            'class':"input"
        })
    class Meta:
        model = Product
        fields = ['image', 'name', 'category', 'stock', 'price', 'sold', 'description']     
        
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description', 'image']
    