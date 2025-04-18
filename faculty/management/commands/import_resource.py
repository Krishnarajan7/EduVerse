import csv
from django.core.management.base import BaseCommand
from faculty.models import Resource
from students.models import Class
from faculty.models import Faculty

class Command(BaseCommand):
    help = 'Import resources from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            resources = []
            for row in reader:
                faculty = Faculty.objects.get(roll_number=row['uploaded_by_roll_number'])
                class_group = Class.objects.get(id=row['class_group_id'])
                resource = Resource(
                    title=row['title'],
                    file=row['file'],
                    uploaded_by=faculty,
                    uploaded_at=row['uploaded_at'],
                    class_group=class_group
                )
                resources.append(resource)

            Resource.objects.bulk_create(resources)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(resources)} resources'))