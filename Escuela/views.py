# escuela/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teacher, Assignment, Group, Student, EvaluationElement, Grade, Attendance, Communication
from django.contrib import messages


# ------------------------------------------
# Dashboard principal del profesor
# ------------------------------------------
@login_required
def profesor_dashboard(request):
    if not request.user.is_teacher:
        # Redirige a admin o login si no es profesor
        if request.user.is_admin or request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/login/')

    teacher = Teacher.objects.get(user=request.user)
    assignments = Assignment.objects.filter(teacher=teacher)

    context = {
        'teacher': teacher,
        'assignments': assignments
    }
    return render(request, 'escuela/profesor_dashboard.html', context)


# ------------------------------------------
# Lista de estudiantes de un grupo y materia
# ------------------------------------------
@login_required
def estudiantes_por_asignacion(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # Seguridad: solo puede acceder el profesor asignado
    if request.user != assignment.teacher.user:
        messages.error(request, "No tienes permiso para ver estos estudiantes.")
        return redirect('profesor_dashboard')

    students = Student.objects.filter(group=assignment.group)

    context = {
        'assignment': assignment,
        'students': students
    }
    return render(request, 'escuela/estudiantes_por_asignacion.html', context)


# ------------------------------------------
# Registro de calificaciones
# ------------------------------------------
@login_required
def registrar_calificacion(request, student_id, assignment_id):
    student = get_object_or_404(Student, pk=student_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # Seguridad
    if request.user != assignment.teacher.user:
        messages.error(request, "No tienes permiso para registrar calificaciones aquí.")
        return redirect('profesor_dashboard')

    elements = EvaluationElement.objects.filter(assignment=assignment)

    if request.method == 'POST':
        for element in elements:
            grade_value = request.POST.get(f'grade_{element.id}')
            if grade_value:
                grade_obj, created = Grade.objects.get_or_create(
                    student=student,
                    evaluation_element=element,
                    defaults={'score': grade_value}
                )
                if not created:
                    grade_obj.score = grade_value
                    grade_obj.save()
        messages.success(request, "Calificaciones guardadas correctamente.")
        return redirect('estudiantes_por_asignacion', assignment_id=assignment.id)

    context = {
        'student': student,
        'assignment': assignment,
        'elements': elements
    }
    return render(request, 'escuela/registrar_calificacion.html', context)


# ------------------------------------------
# Registro de asistencia
# ------------------------------------------
@login_required
def registrar_asistencia(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # Seguridad
    if request.user != assignment.teacher.user:
        messages.error(request, "No tienes permiso para registrar asistencia aquí.")
        return redirect('profesor_dashboard')

    students = Student.objects.filter(group=assignment.group)

    if request.method == 'POST':
        for student in students:
            presencias = request.POST.getlist(f'student_{student.id}')  # checkbox lista
            total_lecciones = int(request.POST.get('total_lecciones', 1))
            # Guardar asistencia
            Attendance.objects.update_or_create(
                student=student,
                assignment=assignment,
                defaults={'present_count': len(presencias), 'total_lessons': total_lecciones}
            )
        messages.success(request, "Asistencia registrada correctamente.")
        return redirect('estudiantes_por_asignacion', assignment_id=assignment.id)

    context = {
        'assignment': assignment,
        'students': students
    }
    return render(request, 'escuela/registrar_asistencia.html', context)


# ------------------------------------------
# Registro de comunicaciones al hogar
# ------------------------------------------
@login_required
def registrar_comunicado(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    # Solo profesores asignados a ese grupo pueden registrar
    teacher_assignments = Assignment.objects.filter(teacher__user=request.user, group=student.group)
    if not teacher_assignments.exists():
        messages.error(request, "No tienes permiso para registrar comunicados para este estudiante.")
        return redirect('profesor_dashboard')

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        mensaje = request.POST.get('mensaje')
        Communication.objects.create(
            student=student,
            teacher=Teacher.objects.get(user=request.user),
            type=tipo,
            message=mensaje
        )
        messages.success(request, "Comunicado registrado correctamente.")
        return redirect('estudiantes_por_asignacion', assignment_id=teacher_assignments.first().id)

    context = {
        'student': student
    }
    return render(request, 'escuela/registrar_comunicado.html', context)
