from django.contrib import admin

from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class meta:
        model = Course

admin.site.register(Course, CourseAdmin)