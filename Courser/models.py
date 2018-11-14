from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.CharField(max_length=50)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=6, blank=True) # Poprawic
    phone_number = models.CharField(max_length=9, blank=True) # poprawic
    user_photo = models.ImageField(blank=True, null=True, upload_to="users/")

    def __str__(self):
        return self.username


class Author(models.Model):
    author_name = models.CharField(max_length=15)
    author_surname = models.CharField(max_length=25)
    author_description = models.TextField(max_length=1000)
    author_photo = models.ImageField(blank=True, null=True, upload_to="authors/")

    def __str__(self):
        return self.author_name


class Category(models.Model):
    category_name = models.CharField(max_length=40)

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, default=0)
    subcategory_name = models.CharField(max_length=40)

    def __str__(self):
        return self.subcategory_name


class CourseLevel(models.Model):
    level_name = models.CharField(max_length=50)

    def __str__(self):
        return self.level_name


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_description = models.TextField(max_length=1000)
    course_price = models.IntegerField()
    course_length = models.IntegerField(blank=True, null=True)
    course_photo = models.ImageField(blank=True, null=True, upload_to="courses/")
    course_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    course_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=0)
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.course_name
