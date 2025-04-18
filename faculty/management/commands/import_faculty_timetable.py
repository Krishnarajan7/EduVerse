import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from faculty.models import Faculty, FacultyTimetable
from students.models import Class, Subject

class Command(BaseCommand):
    help = 'Import faculty timetable from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update timetable if already assigned'
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
                day = row['day']
                period = row['period']
                subject_id = row['subject_id']

                # Get Faculty and Class
                try:
                    faculty = Faculty.objects.get(roll_number=faculty_roll)
                    class_group = Class.objects.get(id=class_id)
                    subject = Subject.objects.get(id=subject_id)  # Assuming Subject model exists
                except Faculty.DoesNotExist:
                    skipped.append({**row, 'reason': 'faculty_not_found'})
                    continue
                except Class.DoesNotExist:
                    skipped.append({**row, 'reason': 'class_not_found'})
                    continue
                except Subject.DoesNotExist:
                    skipped.append({**row, 'reason': 'subject_not_found'})
                    continue

                # Handle timetable creation or update
                try:
                    timetable, created = FacultyTimetable.objects.update_or_create(
                        faculty=faculty,
                        class_group=class_group,
                        day=day,
                        period=period,
                        subject=subject
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Assigned {faculty.name} to {class_group} on {day} for {subject.name}"))
                    else:
                        updated_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Updated timetable for {faculty.name} in {class_group} on {day}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating or updating timetable for {faculty.name}: {e}"))
                    skipped.append({**row, 'reason': 'error_creating_timetable'})

        # Logging skipped rows
        if skipped:
            log_path = Path("skipped_timetable_log.csv")
            with open(log_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=skipped[0].keys())
                writer.writeheader()
                writer.writerows(skipped)
            self.stdout.write(self.style.WARNING(f"Skipped {len(skipped)} rows. Logged to {log_path}"))

        # Final report
        self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
        if update_existing:
            self.stdout.write(self.style.SUCCESS(f"Updated: {updated_count}"))
