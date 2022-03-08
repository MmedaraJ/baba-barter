from __future__ import unicode_literals
from email.policy import default
from django.db import models
import re, bcrypt

from django.forms import CharField
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def signup_validations(self, post_data) -> dict:
        errors={}
        first_name = self.validate_signup_first_name(post_data, errors)
        last_name = self.validate_signup_last_name(post_data, errors)
        email = self.validate_signup_email(post_data, errors)
        date_of_birth = self.validate_signup_date_of_birth(post_data, errors)
        description = self.validate_signup_description(post_data, errors)
        password = self.validate_signup_password(post_data, errors)
        confirm_password = self.validate_signup_repeat_password(post_data, errors)
        return {**first_name, **last_name, **email, **date_of_birth, **description, **password, **confirm_password}

    def validate_signup_first_name(self, post_data, errors) -> dict:
        if len(post_data['signup_first_name_input']) < 1:
            errors['signup_first_name_input'] = "First name cannot be empty"
        elif len(post_data['signup_first_name_input']) < 2:
            errors['signup_first_name_input'] = "First name must contain at least two letters"
        else: 
            for s in post_data['signup_first_name_input']:
                if not s.isalpha() and s!='-':
                    errors['signup_first_name_input'] = "First name must only include letters or '-'"
                    break
        return errors

    def validate_signup_last_name(self, post_data, errors) -> dict:
        if len(post_data['signup_last_name_input']) < 1:
            errors['signup_last_name_input'] = "Last name cannot be empty"
        elif len(post_data['signup_last_name_input']) < 2:
            errors['signup_last_name_input'] = "Last name must contain at least two letters"
        else: 
            for s in post_data['signup_last_name_input']:
                if not s.isalpha() and s!='-':
                    errors['signup_last_name_input'] = "Last name must only include letters or '-'"
                    break
        return errors

    #TODO Check email flag. 
    #Register error if user's email has a current flag. Use UserFlag model 
    def validate_signup_email(self, post_data, errors) -> dict: 
        if len(post_data['signup_email_input']) < 1:
            errors['signup_email_input'] = "Email cannot be empty"
        elif not EMAIL_REGEX.match(post_data['signup_email_input']):
            errors['signup_email_input'] = 'Invalid email address'
        else: 
            email = User.objects.filter(email=post_data['signup_email_input'])
            if len(email) > 0: 
                errors['signup_email_input'] = 'Email address already exists'
        return errors

    #TODO Stop underage login
    def validate_signup_date_of_birth(self, post_data, errors) -> dict:
        if len(post_data['signup_date_of_birth_input']) < 1:
            errors['signup_date_of_birth_input'] = "Date of birth cannot be empty"
        else:
            try:
                datetime.datetime.strptime(post_data['signup_date_of_birth_input'], '%Y-%m-%d')
            except ValueError:
                errors['signup_date_of_birth_input'] = "Invalid date of birth"
        return errors

    #TODO Filter profanity
    def validate_signup_description(self, post_data, errors) -> dict:
        if len(post_data['signup_description_input']) < 1:
            errors['signup_description_input'] = "Description cannot be empty"
        elif len(post_data['signup_description_input']) < 3:
            errors['signup_description_input'] = "Description must contain at least three characters"
        return errors

    def validate_signup_password(self, post_data, errors) -> dict:
        if len(post_data['signup_password_input']) < 1:
            errors['signup_password_input'] = "Password cannot be empty"
        elif len(post_data['signup_password_input']) < 9:
            errors['signup_password_input'] = "Password must contain more than 8 characters"
        else:
            up = False
            num = False
            for s in post_data['signup_password_input']:
                if s.isupper(): up = True
                if s.isdigit(): num = True
            if not up:
                errors['signup_password_input'] = "Password must contain at least one uppercase letter"
            elif not num:
                errors['signup_password_input'] = "Password must contain at least one numerical value"
        return errors
            
    def validate_signup_repeat_password(self, post_data, errors) -> dict:
        if len(post_data['signup_repeat_password_input']) < 1:
            errors['signup_repeat_password_input'] = "Confirm password cannot be empty"
        elif post_data['signup_repeat_password_input'] != post_data['signup_password_input']:
            errors['signup_repeat_password_input'] = "Confirm password is not the same as password"
        return errors

    def signin_validations(self, post_data):
        errors={}
        email = self.validate_signin_email(post_data, errors)
        password = self.validate_signin_password(post_data, errors)
        return {**email, **password}

    def validate_signin_email(self, post_data, errors):
        if len(post_data['signin_email_input']) < 1:
            errors['signin_email_input'] = "Email cannot be empty"
        elif not EMAIL_REGEX.match(post_data['signin_email_input']):
            errors['signin_email_input'] = 'Invalid email address'
        else:
            user = User.objects.filter(email=post_data['signin_email_input'])
            if len(user) < 1: 
                errors['signin_email_input'] = 'Incorrect email address'
        return errors

    def validate_signin_password(self, post_data, errors):
        if len(post_data['signin_password_input']) < 1:
            errors['signin_password_input'] = "Password cannot be empty"
        else:
            user = User.objects.filter(email=post_data['signin_email_input'])
            if len(user)>0:
                if not bcrypt.checkpw(post_data['signin_password_input'].encode(), user[0].password_hash.encode()): 
                    errors['sign_in_password'] = "Incorrect password"
        return errors

#TODO add session to user and make session table
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, default="")
    date_of_birth = models.DateField(max_length=20)
    description = models.TextField(max_length=255, default="")
    token_count = models.IntegerField(default=0)
    access_level = models.IntegerField(default=1)
    score = models.IntegerField(default=100)
    has_paid = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class CategoryManager(models.Manager):
    def category_validations(self):
        return

class Category(models.Model):
    name = models.CharField(max_length=20)
    users = models.ManyToManyField(User, related_name="users", default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManager()

    def __str__(self) -> str:
        return f"{self.name}"

class SubCategoryManager(models.Manager):
    def subcategory_validations(self):
        return

class SubCategory(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, related_name="subcategories", default='other', on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SubCategoryManager()

    def __str__(self) -> str:
        return f"{self.name}"

#TODO validate images
class SwappableManager(models.Manager):
    def swappable_validations(self, post_data) -> dict:
        errors={}
        name = self.validate_name(post_data, errors)
        type = self.validate_type(post_data, errors)
        category = self.validate_category(post_data, errors)
        short_description = self.validate_short_description(post_data, errors)
        long_description = self.validate_long_description(post_data, errors)
        value = self.validate_value(post_data, errors)
        currency = self.validate_currency(post_data, errors)
        return {**name, **type, **category, **short_description, **long_description, **value, **currency}

    def validate_name(self, post_data, errors) -> dict:
        if len(post_data['name']) < 1:
            errors['name'] = "Name cannot be empty"
        return errors

    def validate_type(self, post_data, errors) -> dict:
        if post_data['type'] == "none":
            errors['type'] = "Select Product or Category"
        return errors

    def validate_category(self, post_data, errors) -> dict:
        if post_data['category'] == "none":
            errors['category'] = "Select a category"
        return errors

    def validate_short_description(self, post_data, errors) -> dict:
        if len(post_data['short_description']) < 1:
            errors['short_description'] = "Short description cannot be empty"
        return errors

    def validate_long_description(self, post_data, errors) -> dict:
        if len(post_data['long_description']) < 1:
            errors['long_description'] = "Long description cannot be empty"
        return errors

    def validate_value(self, post_data, errors) -> dict:
        if len(post_data['value']) < 1:
            errors['value'] = "Value cannot be empty"
        return errors

    def validate_currency(self, post_data, errors) -> dict:
        if post_data['currency'] == "none":
            errors['currency'] = "Select a currency"
        return errors

class Swappable(models.Model):
    name = models.CharField(max_length=30, default="")
    type = models.CharField(max_length=10, default="")
    user = models.ForeignKey(User, related_name="user_swappables", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="category_swappables", default="other", on_delete=models.SET_DEFAULT)
    sub_categories = models.ManyToManyField(SubCategory, related_name="all_swappables", default="")
    short_description = models.TextField(max_length=50)
    long_description = models.TextField()
    notes = models.TextField()
    value = models.IntegerField(default=0)
    currency = models.CharField(max_length=50, default="")
    score = models.IntegerField(default=100)
    condition = models.IntegerField(default=100)
    is_deleted = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SwappableManager()

    def __str__(self) -> str:
        return f"{self.name}-{self.short_description}"

class SwappableImageManager(models.Manager):
    def swappable_image_validations(self):
        return

class SwappableImage(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='swappable_images/', default="")
    swappable = models.ForeignKey(Swappable, related_name='swappable_image', on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SwappableImageManager()

    def __str__(self) -> str:
        return f"{self.name}"

class UserImageManager(models.Manager):
    def user_image_validations(self):
        return

class UserImage(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='user_images/', default="")
    user = models.ForeignKey(User, related_name='user_image', on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserImageManager()

    def __str__(self) -> str:
        return f"{self.name}"

class SwappableAddressManager(models.Manager):
    def swappable_address_validations(self):
        return

class SwappableAddress(models.Model):
    swappable = models.ForeignKey(Swappable, related_name='swappable_address', on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    postalcode = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SwappableAddressManager()

    def __str__(self) -> str:
        return f"{self.swappable}-{self.city}-{self.state}-{self.country}-{self.postalcode}"