from django import forms
from django.contrib.admin.widgets import AdminDateWidget 
from django.contrib.auth.models import User
from django.core.validators import validate_email
from models import *

import re


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': ' username'}))
    first_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': ' first name'}))
    last_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': ' last name'}))
    email = forms.CharField(max_length = 40, validators = [validate_email], widget=forms.TextInput(attrs={'placeholder': ' email'}))
    password1 = forms.CharField(max_length = 200, label='Password', widget = forms.PasswordInput(attrs={'placeholder': ' password'}))
    password2 = forms.CharField(max_length = 200, label='Confirm password', widget = forms.PasswordInput(attrs={'placeholder': ' confirm password'}))


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username	


class PostForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'maxlength':512,'rows':3,'style':'resize:none;','class':'form-control'}))
    # body = forms.CharField(required=False, label="", widget=forms.Textarea(attrs={'maxlength':0,'rows':1,'style':'visibility:hidden;','class':'form-control'}))
    public = forms.BooleanField(required=False,label="private", widget=forms.CheckboxInput(attrs={'text':'Private'}))
    class Meta:
        model = Post
        exclude = (
            'user',
            'userId',
            'date',
            'time',
            'username',
        )


class SettingsForm(forms.Form):
    profile_picture = forms.FileField(required=False)
    first_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': ' first name'}),required=False)
    last_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': ' last name'}),required=False)
    bio = forms.CharField(label="", widget=forms.Textarea(attrs={'maxlength':430,'rows':3,'style':'resize:none;','class':'form-control'}),required=False)
    birthday = forms.CharField(max_length=10,required=False)
    new_password1 = forms.CharField(max_length = 200, label='new_password1', widget = forms.PasswordInput(attrs={'placeholder': ' new password'}),required=False)
    new_password2 = forms.CharField(max_length = 200, label='new_password2', widget = forms.PasswordInput(attrs={'placeholder': ' confirm new password'}),required=False)
    old_password = forms.CharField(max_length = 200, label='old_password', widget = forms.PasswordInput(attrs={'placeholder': ' old password'}),required=False)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(SettingsForm, self).clean()

        # Confirms that the two password fields match
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

        # Customizes form validation for the username field.
    def clean_birthday(self):
        # Confirms that the username is not already present in the
        # User model database.
        birthday = self.cleaned_data.get('birthday')

        if birthday and not re.match('^\d\d\d\d-\d\d-\d\d$', birthday):
            raise forms.ValidationError('Must be yyyy-mm-dd')

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return birthday 

   
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('body', )
        widgets = {
            'body' : forms.Textarea(attrs={'rows':2,'style':'resize:none;'}),
        }








