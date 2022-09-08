from django.contrib import admin
from .models import StudentExtraInfo, SecretaryExtraInfo

# Register your models here.
admin.site.register(StudentExtraInfo)
admin.site.register(SecretaryExtraInfo)