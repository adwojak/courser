from django.db import models


class Author(models.Model):
    author_name = models.CharField(max_length=15)
    author_surname = models.CharField(max_length=25)
    author_description = models.TextField(max_length=1000)
    author_photo = models.ImageField(blank=True, null=True, upload_to="authors/")


class Category(models.Model):
    category_name = models.CharField(max_length=40)


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=40)


class Type(models.Model):
    type_name = models.CharField(max_length=20)


class Country(models.Model):
    country_name = models.CharField(max_length=50)
    language_code = models.CharField(max_length=10)
    language_name = models.CharField(max_length=30)


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_description = models.TextField(max_length=1000)
    course_price = models.IntegerField()
    course_length = models.IntegerField(null=True)
    course_pages = models.IntegerField(null=True)
    course_photo = models.ImageField(blank=True, null=True, upload_to="courses/")
    course_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    course_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    course_language = models.ForeignKey(Country, on_delete=models.CASCADE)
