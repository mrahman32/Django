from django.contrib import admin
from .models import Department, Course, Semester, Student, StudentDocument
from .views import index
from .viewmodels.StudentViewModel import StudentBt

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_roll", "added_date")
    search_fields = ("student_name", "student_roll", "added_date")


admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentDocument)
