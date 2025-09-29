from django.core.management.base import BaseCommand
from escuela.models import Subject, Group, User, Teacher
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Crea datos iniciales para la app Escuela'

    def handle(self, *args, **options):
        # ----- Materias -----
        subjects = ['Matemáticas', 'Ciencias', 'Estudios Sociales', 'Español']
        for s in subjects:
            Subject.objects.get_or_create(name=s)
        self.stdout.write(self.style.SUCCESS('Materias creadas'))

        # ----- Grupos -----
        grupos = ['1° A', '1° B', '2° A', '2° B']
        for g in grupos:
            Group.objects.get_or_create(name=g, year=2025)
        self.stdout.write(self.style.SUCCESS('Grupos creados'))

        # ----- Usuario administrador -----
        if not User.objects.filter(username='admin').exists():
            User.objects.create(
                username='admin',
                password=make_password('admin123'),
                role='ADMIN',
                is_superuser=True,
                is_staff=True,
                email='admin@colegio.cr'
            )
        self.stdout.write(self.style.SUCCESS('Usuario administrador creado'))

        # ----- Profesor de prueba -----
        if not User.objects.filter(username='profesor1').exists():
            prof_user = User.objects.create(
                username='profesor1',
                password=make_password('prof123'),
                role='TEACHER',
                is_staff=True,
                email='profesor1@colegio.cr'
            )
            Teacher.objects.create(user=prof_user, specialty='Matemáticas')
        self.stdout.write(self.style.SUCCESS('Profesor de prueba creado'))
