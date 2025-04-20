
from django.db import models




class Login(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    type=models.CharField(max_length=20)

class Expert(models.Model):
    login_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    expert_name = models.CharField(max_length=255)
    place = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    experience = models.IntegerField()
    qualification = models.CharField(max_length=255)
    photo = models.FileField()


class User(models.Model):
    login_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    pin = models.CharField(max_length=10)

    photo = models.FileField()







class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    complaint = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    feedback = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField()


class Tips(models.Model):
    id = models.AutoField(primary_key=True)
    tips = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    expert_id = models.ForeignKey(Expert, on_delete=models.CASCADE)


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    from_id = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="sent_messages")
    to_id = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="received_messages")
    chat = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)


class Notification(models.Model):
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    expert_id = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="notifications")

class Admin_Notification(models.Model):
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100)