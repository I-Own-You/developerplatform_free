from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from django.db.utils import IntegrityError
from django.http import request
from .models import Developer
import re


class UserEditForm(forms.Form):

    first_name = forms.CharField(
        label='First Name', max_length=20, required=True)
    last_name = forms.CharField(
        label='Last Name', max_length=20, required=True)
    work_position = forms.CharField(
        label='Work Position', max_length=30, required=True)
    short_bio = forms.CharField(
        label='Short Bio', widget=forms.Textarea(attrs={'cols': '40', 'rows': '10'}), required=True, max_length=100)
    social_link_github = forms.URLField(label='GitHub')
    social_link_linkedIn = forms.URLField(label='LinkedIn')
    username = forms.CharField(
        label='Username', max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.fields[key].widget.attrs.update(
            {'class': 'all-inputs-form-custom '}) for key in self.fields]

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if len(username) < 8 or re.fullmatch('[a-z]+\d*', username) == None:
            raise ValidationError(
                f"{self.fields['last_name'].label} must contain 8-20 alphabetic characters,\
                    digits allowed only at the end!"
            )

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').lower().capitalize()
        if first_name.isalpha() == False or len(first_name.lower()) < 4:
            raise ValidationError(
                f"{self.fields['first_name'].label} must contain only alphabetic characters!"
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').lower().capitalize()
        if last_name.isalpha() == False or len(last_name) < 4:
            raise ValidationError(
                f"{self.fields['last_name'].label} must contain only alphabetic characters!"
            )
        return last_name

    def clean_work_position(self):
        work_position = self.cleaned_data.get('work_position')
        return work_position

    def clean_short_bio(self):
        short_bio = self.cleaned_data.get('short_bio')
        return short_bio

    def clean_social_link_github(self):
        social_link_github = self.cleaned_data.get('social_link_github')
        try:
            URLValidator(social_link_github)
        except:
            raise ValidationError('Invalid link')
        return social_link_github

    def clean_social_link_linkedIn(self):
        social_link_linkedIn = self.cleaned_data.get('social_link_linkedIn')
        try:
            URLValidator(social_link_linkedIn)
        except:
            raise ValidationError('Invalid link')
        return social_link_linkedIn


class RegisterForm(forms.Form):

    email = forms.EmailField(
        label='E-mail', required=True)

    password = forms.CharField(
        label='Password', max_length=15, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.fields[key].widget.attrs.update(
            {'class': 'all-inputs-form-custom '}) for key in self.fields]

        self.fields['email'].widget.attrs['class'] += 'inp-email '
        self.fields['password'].widget.attrs['class'] += 'inp-password '

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Developer.objects.filter(email=email).exists():
            raise ValidationError('Email already taken')
        else:
            validate_email(email)

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or re.fullmatch('[a-zA-Z0-9\?\!]*', password) == None:
            raise ValidationError(
                f"{self.fields['password'].label} must contain 8-20 characters: letters\digits and also: ? !"
            )
        return password


class ProjCreateForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '40', 'rows': '10'}), label='Description', required=True, max_length=400)
    source_link = forms.URLField(label='Source Link', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.fields[key].widget.attrs.update(
            {'class': 'all-inputs-proj-create '}) for key in self.fields]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return description

    def clean_source_link(self):
        source_link = self.cleaned_data.get('source_link')
        try:
            URLValidator(source_link)
        except:
            raise ValidationError('Invalid link')
        return source_link


class MessageCreateForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=50, required=True)
    content = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '50', 'rows': '10'}), label='Content', max_length=500, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.fields[key].widget.attrs.update(
            {'class': 'all-inputs-msg-create'}) for key in self.fields]

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')

        return subject

    def clean_content(self):
        content = self.cleaned_data.get('content')

        return content

    # class MyForm(forms.Form):
    #     myfield = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))

    # class MyForm(forms.ModelForm):
    #     class Meta:
    #         model = MyModel
    #         widgets = {
    #             'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
    #         }

    # class MyForm(forms.ModelForm):
    #     class Meta:
    #         model = MyModel

    #     def __init__(self, *args, **kwargs):
    #         super(MyForm, self).__init__(*args, **kwargs)
    #         self.fields['myfield'].widget.attrs.update({'class' : 'myfieldclass'})
