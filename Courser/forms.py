from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField,
    UsernameField,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm
)
from django.forms import (
    HiddenInput,
    TextInput,
    CharField,
    PasswordInput,
    EmailField,
    EmailInput,
    ImageField,
    IntegerField
)
from django.contrib.auth.password_validation import password_validators_help_text_html
from .models import CustomUser
from .widgets import CustomClearableFileInput


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


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = CharField(
        label="Old password",
        strip=False,
        widget=PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = CharField(
        label="New password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = CharField(
        label="Repeat new password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomEditProfileForm(UserChangeForm):
    first_name = CharField(
        label="First name",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    last_name = CharField(
        label="Last name",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    address = CharField(
        label="Address",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    city = CharField(
        label="City",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    zip_code = CharField(
        label="Zip-code",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    phone_number = CharField(
        label="Phone number",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    user_photo = ImageField(
        label="Choose photo",
        widget=CustomClearableFileInput() # TODO Button w edit
    )
    password = ReadOnlyPasswordHashField(label="", widget=HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'address', 'city', 'zip_code', 'phone_number', 'user_photo')


class CustomEditPaymentForm(UserChangeForm):
    credit_card_number = IntegerField(
        label="Credit card number",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    credit_card_expire_date = CharField(
        label="Credit card expire date",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    credit_card_cvv = IntegerField(
        label="Credit card cvv number",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    password = ReadOnlyPasswordHashField(label="", widget=HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('credit_card_number', 'credit_card_expire_date', 'credit_card_cvv')
