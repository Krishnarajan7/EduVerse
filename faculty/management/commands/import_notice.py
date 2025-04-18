import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from faculty.models import Faculty, Notice

class Command(BaseCommand):
    help = 'Import notices from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = row['title']
                    content = row['content']
                    posted_by_roll_number = row['posted_by_roll_number']
                    posted_at = datetime.strptime(row['posted_at'], "%Y-%m-%d %H:%M:%S")  # Ensure the format is correct

                    # Debugging: Log the row to see the content
                    self.stdout.write(self.style.SUCCESS(f"Processing row: {row}"))

                    try:
                        faculty = Faculty.objects.get(roll_number=posted_by_roll_number)
                    except Faculty.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Faculty with roll number {posted_by_roll_number} does not exist"))
                        continue

                    # Create the notice
                    Notice.objects.create(
                        title=title,
                        content=content,
                        posted_by=faculty,
                        posted_at=posted_at
                    )

                    self.stdout.write(self.style.SUCCESS(f"Successfully imported notice: {title}"))

                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f"Error parsing row: {row}, Error: {e}"))
