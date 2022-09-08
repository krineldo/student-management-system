from django.contrib.auth.models import User
from django.db import models


class AdminExtraInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=40, null=True)

	def __str__(self):
		return str(self.user)


class SecretaryExtraInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	join_date = models.DateField(auto_now_add=True)
	phone_number = models.CharField(max_length=40, null=True)
	status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)

	@property
	def get_id(self):
		return self.user.id

	@property
	def get_name(self):
		return self.user.first_name + " " + self.user.last_name

	@property
	def get_email(self):
		return self.user.email

	@property
	def get_username(self):
		return self.user.username


class StudentExtraInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	join_date = models.DateField(auto_now_add=True)
	phone_number = models.CharField(max_length=40, null=True)
	status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)

	@property
	def get_id(self):
		return self.user.id

	@property
	def get_name(self):
		return self.user.first_name + " " + self.user.last_name

	@property
	def get_email(self):
		return self.user.email

	@property
	def get_username(self):
		return self.user.username



class Announcement(models.Model):
	date = models.DateField(auto_now=True)
	by = models.CharField(max_length=20, null=True, default='school')
	message = models.CharField(max_length=500)
