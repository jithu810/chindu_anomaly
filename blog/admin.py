from django.contrib import admin
from .models import Post
from django.contrib.auth.models import User




class TestPermission(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True



admin.site.register(Post,TestPermission)

