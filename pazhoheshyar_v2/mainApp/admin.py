from django.contrib import admin
from .models import User, Thesis
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display = ("user_id", "firstname", "lastname", )

class ThesisAdmin(admin.ModelAdmin):
  list_display = ("title", "student", "state", "created_at")

admin.site.register(User , UserAdmin)
admin.site.register(Thesis , ThesisAdmin)
