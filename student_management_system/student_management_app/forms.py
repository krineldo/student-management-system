from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


# Admin form
class CreateAdminForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CreateAdminFormExtraInfo(forms.ModelForm):
	class Meta:
		model = models.AdminExtraInfo
		fields = ['phone_number']


# Secretary form
class CreateSecretaryForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UpdateSecretaryForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']


class CreateSecretaryFormExtraInfo(forms.ModelForm):
	class Meta:
		model = models.SecretaryExtraInfo
		fields = ['phone_number', 'status']


# Student form
class CreateStudentForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UpdateStudentForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']

class CreateStudentFormExtraInfo(forms.ModelForm):
	class Meta:
		model = models.StudentExtraInfo
		fields = ['phone_number', 'status']


# Notice form
class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = models.Announcement
		fields = '__all__'
