import csv
from django.core.management.base import BaseCommand
from students.models import Subject, Student

class Command(BaseCommand):
    help = 'Import subjects from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            subjects = []
            for row in reader:
                try:
                    student = Student.objects.get(roll_number=row['student_roll_number'])
                    subject = Subject(
                        student=student,
                        name=row['name'],
                        marks=float(row['marks'])
                    )
                    subjects.append(subject)
                except Student.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f"Student {row['student_roll_number']} does not exist: {e}"))
                    continue
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f"Invalid marks for {row['name']}: {e}"))
                    continue

            if subjects:
                Subject.objects.bulk_create(subjects)
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(subjects)} subjects'))
            else:
                self.stdout.write(self.style.WARNING('No valid subjects imported'))