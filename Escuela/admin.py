from django.contrib import admin
from .models import Student, Subject, Group, Assignment, EvaluationElement, Grade, Attendance, Communication, Teacher, User

class TeacherAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        # Solo superuser o admins pueden ver la app completa
        if request.user.is_superuser or request.user.is_admin:
            return True
        return False

class StudentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser or request.user.is_admin:
            return True
        return False

# Registrar modelos con restricciones
admin.site.register(User)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(EvaluationElement)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(Communication)
