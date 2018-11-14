from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField,
    UsernameField,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.forms import (
    HiddenInput,
    TextInput,
    CharField,
    PasswordInput,
    EmailField,
    EmailInput
)
from django.contrib.auth.password_validation import password_validators_help_text_html
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = UsernameField(widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control'}))
    password1 = CharField(
        label=("Password1"),
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = CharField(
        label=("Password2"),
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="Password", widget=HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'address', 'city', 'zip_code', 'phone_number', 'user_photo')


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(initial="", widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control'}))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = CharField(
        label="New password",
        widget=PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validators_help_text_html(),
    )
    new_password2 = CharField(
        label="New password confirmation",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )
