from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    FileField,
    ImageField,
    OneToOneField,
    TextField,
    ForeignKey,
    IntegerField,
    BooleanField,
    CASCADE,
    Model
)


class CustomUser(AbstractUser):
    email = CharField(max_length=50)
    first_name = CharField(max_length=30, blank=True)
    last_name = CharField(max_length=50, blank=True)
    address = CharField(max_length=100, blank=True)
    city = CharField(max_length=50, blank=True)
    zip_code = CharField(max_length=6, blank=True) # TODO poprawic
    phone_number = CharField(max_length=9, blank=True) # TODO poprawic
    user_photo = ImageField(blank=True, null=True, upload_to="users/")
    credit_card_number = IntegerField(blank=True, null=True)
    credit_card_expire_date = CharField(max_length=4, blank=True, null=True)
    credit_card_cvv = IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    def is_payment_fulfilled(self):
        return all([
            self.email,
            self.phone_number,
            self.credit_card_number,
            self.credit_card_expire_date,
            self.credit_card_cvv
        ])


class Category(Model):
    category_name = CharField(max_length=40)

    def __str__(self):
        return self.category_name


class CourseLevel(Model):
    level_name = CharField(max_length=50)

    def __str__(self):
        return self.level_name


class Course(Model):
    course_name = CharField(max_length=100)
    course_description = TextField(max_length=1000)
    course_price = IntegerField()
    course_length = IntegerField(blank=True, null=True)
    course_photo = ImageField(blank=True, null=True, upload_to="courses/")
    course_video = FileField(blank=True, null=True, upload_to="videos/")
    course_author = ForeignKey(CustomUser, on_delete=CASCADE)
    course_category = ForeignKey(Category, on_delete=CASCADE)
    course_level = ForeignKey(CourseLevel, on_delete=CASCADE, default=0)

    def __str__(self):
        return self.course_name


class Cart(Model):
    course_id = IntegerField(default=0, null=False)
    course_name = CharField(max_length=100)
    course_price = IntegerField()