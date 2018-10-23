from django.contrib import admin
from .models import Diary,User

# Register your models here.
class DiaryInline(admin.StackedInline):
    model = Diary
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username','password']}),
    ]
    inlines = [DiaryInline]

admin.site.register(User, UserAdmin)
