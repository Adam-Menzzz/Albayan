from django.contrib import admin
from .models import Category, Course, Module

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    exclude = ('slug',)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
