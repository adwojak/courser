from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator
)
from django.db.models import (
    CharField,
    EmailField,
    FileField,
    ImageField,
    TextField,
    ForeignKey,
    IntegerField,
    DecimalField,
    CASCADE,
    Model
)
from PIL import Image
from resizeimage import resizeimage
from math import floor
from io import BytesIO
from sys import getsizeof
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomUser(AbstractUser):
    email = EmailField(unique=True)
    first_name = CharField(max_length=30, blank=True)
    last_name = CharField(max_length=50, blank=True)
    address = CharField(max_length=100, blank=True)
    city = CharField(max_length=50, blank=True)
    zip_code = CharField(max_length=6, blank=True)
    phone_number = IntegerField(max_length=12, blank=True)
    user_photo = ImageField(blank=True, null=True, upload_to="users/")
    credit_card_number = CharField(max_length=19, blank=True, null=True)
    credit_card_expire_date = CharField(max_length=7, blank=True, null=True)
    credit_card_cvv = CharField(max_length=3, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        if self.user_photo:
            with Image.open(self.user_photo) as image:
                aspect = 2.095
                width, height = image.size
                if height < width:
                    width = floor(height * aspect)
                elif height > width:
                    height = floor(width / aspect)
                cover = resizeimage.resize_cover(image, [width, height])
                output = BytesIO()
                cover.save(output, image.format)
                output.seek(0)
                self.user_photo = InMemoryUploadedFile(output, 'ImageField', '{}.jpg'.format(self.user_photo.name.split('.')[0]), 'image/jpeg', getsizeof(output), None)
                super(CustomUser, self).save()


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
    course_price = DecimalField(max_digits=6, decimal_places=2)
    course_length = IntegerField(blank=True, null=True)
    course_photo = ImageField(blank=True, null=True, upload_to="courses/")
    course_video = FileField(blank=True, null=True, upload_to="videos/")
    course_author = ForeignKey(CustomUser, on_delete=CASCADE)
    course_category = ForeignKey(Category, on_delete=CASCADE)
    course_level = ForeignKey(CourseLevel, on_delete=CASCADE, default=0)

    def __str__(self):
        return self.course_name

    def save(self, *args, **kwargs):
        with Image.open(self.course_photo) as image:
            aspect = 2.095
            width, height = image.size
            if height < width:
                width = floor(height * aspect)
            elif height > width:
                height = floor(width / aspect)
            cover = resizeimage.resize_cover(image, [width, height])
            output = BytesIO()
            cover.save(output, image.format)
            output.seek(0)
            self.course_photo = InMemoryUploadedFile(output, 'ImageField', '{}.jpg'.format(self.course_photo.name.split('.')[0]), 'image/jpeg', getsizeof(output), None)
            super(Course, self).save()



class Cart(Model):
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    course = ForeignKey(Course, on_delete=CASCADE)
