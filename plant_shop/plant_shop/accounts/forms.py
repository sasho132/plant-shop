from django.contrib.auth import forms as auth_forms, get_user_model, authenticate, login
from django import forms
from django.core.exceptions import ValidationError
from django.template.context_processors import request
from plant_shop.accounts.models import UserProfile

UserModel = get_user_model()


class SignUpForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control floatingInput shadow rounded'

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        field_classes = {
            'username': auth_forms.UsernameField,
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError(
                'Passwords does not match!'
            )


class SignInForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow rounded'

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        ),
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'address_line_1', 'address_line_2', 'city', 'zip_code')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
