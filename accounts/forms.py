from django import forms
from django.contrib.auth.models import User


class BootstrapMixinForm(forms.ModelForm):
    """
    Sample Django Form To add Bootstrap's Form Control class to every field.
    """
    def __init__(self, *args, **kwargs):
        super(BootstrapMixinForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        abstract = True


class UserForm(BootstrapMixinForm):
    """Signup Form"""
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text="*Required")
    email = forms.EmailField(required=True, help_text="*Required")
    username = forms.CharField(help_text="*Required")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class ProfileForm(BootstrapMixinForm):
    """Edit Profile Form."""
    email = forms.EmailField(required=True, help_text="*Required")

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ContactForm(forms.Form):
    """Contact Form."""
    name = forms.CharField(label="Enter your name:", required=True,
                           help_text="*Required")
    phone_number = forms.CharField(label="Enter phone number:", required=False)
    email = forms.EmailField(label="Enter email:", required=True,
                             help_text="*Required")
    feedback = forms.CharField(widget=forms.Textarea, label="Enter Feedback:",
                               required=True, help_text="*Required")
