import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from students.models import Class, Student, Attendance
from faculty.models import Faculty

class Command(BaseCommand):
    help = 'Import attendance from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        created_count = 0
        skipped = []

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                faculty_roll = row['faculty_roll_number']
                class_group_id = row['class_group_id']
                date = row['date']
                is_present = row['is_present'] == 'True'  # Convert to boolean

                try:
                    # Fetch the class using the class_group_id
                    class_group = Class.objects.get(id=class_group_id)

                    # Fetch the student associated with the class
                    students_in_class = Student.objects.filter(class_group=class_group)

                    # Now associate attendance for each student in the class
                    for student in students_in_class:
                        try:
                            attendance, created = Attendance.objects.update_or_create(
                                student=student,
                                date=date,
                                defaults={'is_present': is_present}
                            )
                            if created:
                                created_count += 1
                                self.stdout.write(self.style.SUCCESS(f"Created attendance for {student.name} in {class_group}"))
                        except Exception as e:
                            skipped.append({**row, 'reason': str(e)})
                            continue

                except Class.DoesNotExist:
                    skipped.append({**row, 'reason': 'class_not_found'})
                    continue

            # Log skipped rows
            if skipped:
                log_path = Path("skipped_attendance_log.csv")
                with open(log_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=skipped[0].keys())
                    writer.writeheader()
                    writer.writerows(skipped)
                self.stdout.write(self.style.WARNING(f"Skipped {len(skipped)} rows. Logged to {log_path}"))

        self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
