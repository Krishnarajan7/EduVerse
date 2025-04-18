import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from faculty.models import Faculty, FacultyIncharge
from students.models import Class

class Command(BaseCommand):
    help = 'Import faculty incharges from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update incharge if already assigned'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        update_existing = options['update_existing']

        created_count = 0
        updated_count = 0
        skipped = []

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                faculty_roll = row['faculty_roll_number']
                class_id = row['class_group_id']

                try:
                    # Fetch the faculty using roll_number and the class using class_id
                    faculty = Faculty.objects.get(roll_number=faculty_roll)
                    class_group = Class.objects.get(id=class_id)
                except Faculty.DoesNotExist:
                    skipped.append({**row, 'reason': 'faculty_not_found'})
                    continue
                except Class.DoesNotExist:
                    skipped.append({**row, 'reason': 'class_not_found'})
                    continue

                try:
                    # Check if the FacultyIncharge exists for this class_group
                    incharge = FacultyIncharge.objects.get(class_group=class_group)
                    if update_existing:
                        # Update the incharge faculty if --update-existing is passed
                        incharge.faculty = faculty
                        incharge.save()
                        updated_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Updated incharge for Class {class_group}"))
                    else:
                        # Skip if incharge already exists and --update-existing is not passed
                        skipped.append({**row, 'reason': 'already_assigned'})
                except FacultyIncharge.DoesNotExist:
                    # If no incharge exists, create a new assignment
                    FacultyIncharge.objects.create(faculty=faculty, class_group=class_group)
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Assigned {faculty.name} to {class_group}"))

        # If there are skipped rows, log them to a CSV
        if skipped:
            log_path = Path("skipped_incharge_log.csv")
            with open(log_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=skipped[0].keys())
                writer.writeheader()
                writer.writerows(skipped)
            self.stdout.write(self.style.WARNING(f"Skipped {len(skipped)} rows. Logged to {log_path}"))

        # Final success count output
        self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
        if update_existing:
            self.stdout.write(self.style.SUCCESS(f"Updated: {updated_count}"))
