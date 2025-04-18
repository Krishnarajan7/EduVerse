import csv
from django.core.management.base import BaseCommand
from faculty.models import Faculty, FacultyTimetable  # Make sure FacultyTimetable is the model you're working with
from students.models import Class, Subject
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Imports faculty period assignments from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        skipped = []

        # Open the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                faculty_roll_number = row['faculty_roll_number'].strip()
                class_group_id = row['class_group_id'].strip()
                subject_id = row['subject_id'].strip()
                day = row['day'].strip()
                period_number = row['period_number'].strip()

                # Fetch Faculty, Class, and Subject objects
                try:
                    faculty = Faculty.objects.get(roll_number=faculty_roll_number)
                    class_group = Class.objects.get(id=class_group_id)
                    subject = Subject.objects.get(id=subject_id)

                    # Create a new FacultyTimetable entry
                    FacultyTimetable.objects.create(
                        faculty=faculty,
                        class_group=class_group,
                        subject=subject,
                        day=day,
                        period_number=period_number
                    )
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported period for {faculty_roll_number}, {day}, Period {period_number}"))

                except Faculty.DoesNotExist:
                    skipped.append({**row, 'reason': 'faculty_not_found'})
                    self.stdout.write(self.style.WARNING(f"Faculty with roll number {faculty_roll_number} not found"))
                except Class.DoesNotExist:
                    skipped.append({**row, 'reason': 'class_not_found'})
                    self.stdout.write(self.style.WARNING(f"Class with ID {class_group_id} not found"))
                except Subject.DoesNotExist:
                    skipped.append({**row, 'reason': 'subject_not_found'})
                    self.stdout.write(self.style.WARNING(f"Subject with ID {subject_id} not found"))
                except IntegrityError as e:
                    skipped.append({**row, 'reason': f'integrity_error: {e}'})
                    self.stdout.write(self.style.ERROR(f"Integrity error while importing {row}: {e}"))

        # Optional: Output skipped rows
        if skipped:
            self.stdout.write(self.style.ERROR(f"Skipped {len(skipped)} rows"))
            for row in skipped:
                self.stdout.write(self.style.WARNING(f"Skipped row: {row}"))
