from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "Login name should be at least 5 characters"
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        if postData['password'] != postData['confrim_pw']:
            errors['confirm_pw']="Password must match"
        exists = Users.objects.filter(email=postData['email'])
        if len(exists) > 0:
            errors['email_exists'] = "This email exists"
        return errors
        

    def login_validator(self, postData):
        errors={}
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title'])==0:
            errors['title']="Title should be applied"
        if len(postData['title']) < 5:
            errors["title"] = "Title should be at least 5 characters"
        if len(postData['desc']) < 5:
            errors["desc"] = "Description should be at least 5 characters"
        return errors


class Users(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects=UserManager()   

    def __repr__(self):
        return f"{self.fname} {self.lname}"
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user
    
class Comments(models.Model):
    comment=models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    upload_by=models.ForeignKey(Users, related_name="firm",on_delete=models.CASCADE)
    objects=BookManager()