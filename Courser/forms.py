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
    DateField,
    DateInput,
    ChoiceField,
    Select,
    ModelForm
)
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.core.validators import RegexValidator
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
        widget=PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = CharField(
        label="Repeat password",
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'})
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
        max_length=30,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    last_name = CharField(
        label="Last name",
        max_length=50,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    address = CharField(
        label="Address",
        max_length=100,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    city = CharField(
        label="City",
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-z]+$')],
        widget=TextInput(attrs={'class': 'form-control'})
    )
    zip_code_prefix = CharField(
        label="Zip-code prefix",
        min_length=2,
        max_length=2,
        validators=[RegexValidator(r'^\d+$')],
        widget=TextInput(attrs={'class': 'form-control'})
    )
    zip_code_suffix = CharField(
        label="Zip-code suffix",
        min_length=3,
        max_length=3,
        validators=[RegexValidator(r'^\d+$')],
        widget=TextInput(attrs={'class': 'form-control'})
    )
    phone_number = CharField(
        label="Phone number",
        min_length=8,
        max_length=12,
        validators=[RegexValidator(r'^\d+$')],
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
    credit_card_number = CharField(
        label="Credit card number",
        min_length=12,
        max_length=19,
        validators=[RegexValidator(r'^\d+$')],
        widget=TextInput(attrs={'class': 'form-control'})
    )
    credit_card_expire_date_prefix = ChoiceField(
        label='Credit card expire month',
        choices=tuple([(month, month) for month in range(1, 13)]),
        widget=Select(attrs={'class': 'form-control'}),
    )
    credit_card_expire_date_suffix = ChoiceField(
        label='Credit card expire year',
        choices=tuple([(year, year) for year in range(2019, 2030)]),
        widget=Select(attrs={'class': 'form-control'}),
    )
    credit_card_cvv = CharField(
        label="Credit card cvv number",
        min_length=3,
        max_length=3,
        validators=[RegexValidator(r'^\d+$')],
        widget=TextInput(attrs={'class': 'form-control'})
    )
    password = ReadOnlyPasswordHashField(label="", widget=HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('credit_card_number', 'credit_card_expire_date_prefix', 'credit_card_expire_date_suffix', 'credit_card_cvv')


class AddCourseForm(ModelForm):
    course_name = CharField(
        label="Course name",
        max_length=100,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    course_description = CharField(
        label="Course description",
        max_length=1000,
        widget=Textarea(attrs={'class': 'form-control'})
    )
    course_price = DecimalField(
        label="Course price",
        max_digits=6,
        decimal_places=2,
        widget=TextInput(attrs={'class': 'form-control'})
    )
    course_length = IntegerField(
        label="Course length",
        min_value=1,
        max_value=99999,
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
