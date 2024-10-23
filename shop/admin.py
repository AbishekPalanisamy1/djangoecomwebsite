from django.contrib import admin
from . models import *



class Categoryadmin(admin.ModelAdmin):
    list_display=('name','image','description')

admin.site.register(Category,Categoryadmin)

admin.site.register(Product)
# Register your models here.
