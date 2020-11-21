from django.db import models
import re 

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']="First name must be longer than 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name']="Last name must be longer than 2 characters"
        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']="Password must be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw']="Password and confirm password must match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = ""
        if len(postData['content'])==0:
            errors="Message cannot be blank"
        return errors 

class MessagePost(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(MessagePost, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



