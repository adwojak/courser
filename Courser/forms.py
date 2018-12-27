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
    Textarea,
    CharField,
    PasswordInput,
    EmailField,
    EmailInput,
    ImageField,
    FileField,
    IntegerField,
    DecimalField,
    ModelChoiceField,
    Select,
    ModelForm
)
from django.contrib.auth.password_validation import password_validators_help_text_html
from .models import (
    CustomUser,
    Course,
    Category,
    CourseLevel
)
from .widgets import CustomClearableFileInput


class CustomUserCreationForm(UserCreationForm):
    username = UsernameField(
        label="Username",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    email = EmailField(
        label="E-mail",
        widget=EmailInput(attrs={'class': 'form-control'})
    )
    password1 = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = CharField(
        label="Repeat password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        initial="",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    password = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = EmailField(
        label="E-mail",
        widget=EmailInput(attrs={'class': 'form-control'})
    )


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
    zip_code_prefix = IntegerField(
        label="Zip-code prefix",
        min_value=10,
        max_value=99,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    zip_code_suffix = IntegerField(
        label="Zip-code suffix",
        min_value=100,
        max_value=999,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    phone_number = CharField(
        label="Phone number",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    user_photo = ImageField(
        required=False,
        label="Choose photo",
        widget=CustomClearableFileInput()
    )
    password = ReadOnlyPasswordHashField(label="", widget=HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'address', 'city', 'zip_code_prefix', 'zip_code_suffix', 'phone_number', 'user_photo')


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


class AddCourseForm(ModelForm):
    course_name = CharField(
        label="Course name",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    course_description = CharField(
        label="Course description",
        widget=Textarea(attrs={'class': 'form-control'})
    )
    course_price = DecimalField(
        label="Course price",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    course_length = IntegerField(
        label="Course length",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    course_category = ModelChoiceField(
        label="Course category",
        widget=Select(attrs={'class': 'form-control'}),
        queryset=Category.objects.all()
    )
    course_level = ModelChoiceField(
        label="Course level",
        widget=Select(attrs={'class': 'form-control'}),
        queryset=CourseLevel.objects.all()
    )
    course_photo = ImageField(
        required=False,
        label="Choose photo",
        widget=CustomClearableFileInput()
    )
    course_video = FileField(
        required=False,
        label="Choose video",
        widget=CustomClearableFileInput()
    )

    class Meta:
        model = Course
        fields = ('course_name', 'course_description', 'course_price', 'course_length', 'course_category', 'course_level', 'course_photo', 'course_video')
