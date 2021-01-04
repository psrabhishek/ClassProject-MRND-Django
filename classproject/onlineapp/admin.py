from django.contrib import admin
from onlineapp import models


# Register your models here.
admin.site.register(models.College)
admin.site.register(models.Student)
admin.site.register(models.MockTest1)
admin.site.register(models.Teacher)