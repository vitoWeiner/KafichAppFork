from django.contrib import admin
from .models import *

model_list = [Pice]
admin.site.register(model_list)