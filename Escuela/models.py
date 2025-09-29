from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# Usuario con roles
# -----------------------------
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('TEACHER', 'Profesor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_teacher(self):
        return self.role == 'TEACHER'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.get_full_name()

# -----------------------------
# Grupo (Sección oficial MEP)
# -----------------------------
class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)  # Ej: "3-1"
    year = models.PositiveIntegerField()  # Ej: 2025

    def __str__(self):
        return f"{self.name} - {self.year}"

# -----------------------------
# Estudiante
# -----------------------------
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identification = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    contact_home = models.CharField(max_length=200, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# -----------------------------
# Materia
# -----------------------------
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ej: Matemáticas
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# -----------------------------
# Asignación Profesor-Materia-Grupo
# -----------------------------
class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assignments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'subject', 'group')

    def __str__(self):
        return f"{self.teacher} - {self.subject} - {self.group}"

# -----------------------------
# Elementos Evaluativos
# -----------------------------
class EvaluationElement(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="evaluation_elements")
    name = models.CharField(max_length=100)  # Ej: "Examen 1", "Proyecto"
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # porcentaje (debe sumar 100%)

    class Meta:
        unique_together = ('assignment', 'name')

    def __str__(self):
        return f"{self.name} ({self.weight}%)"

# -----------------------------
# Calificaciones por estudiante
# -----------------------------
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    evaluation_element = models.ForeignKey(EvaluationElement, on_delete=models.CASCADE, related_name="grades")
    score = models.DecimalField(max_digits=5, decimal_places=2)  # 0–100
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'evaluation_element')

    def __str__(self):
        return f"{self.student} - {self.evaluation_element}: {self.score}"

# -----------------------------
# Asistencia
# -----------------------------
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('T', 'Tarde'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'assignment', 'date')

    def __str__(self):
        return f"{self.student} - {self.assignment.subject} - {self.date} ({self.status})"

# -----------------------------
# Comunicaciones al hogar
# -----------------------------
class Communication(models.Model):
    TYPE_CHOICES = [
        ('POS', 'Observación positiva'),
        ('REC', 'Recomendación de mejora'),
        ('DIS', 'Reporte disciplinario'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="communications")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="communications")
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.get_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"
