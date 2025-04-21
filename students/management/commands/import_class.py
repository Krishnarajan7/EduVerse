import csv
from django.core.management.base import BaseCommand
from students.models import Class

class Command(BaseCommand):
    help = 'Import classes from a CSV with name like "1st Year A" and department field'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            classes = []
            for row in reader:
                try:
                    
                    name_parts = row['name'].strip().split()
                    year = name_parts[0]      
                    section = name_parts[-1]  
                    department = row.get('department', 'CSE')

                    class_obj = Class(
                        year=year,
                        section=section,
                        department=department
                    )
                    classes.append(class_obj)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error parsing row {row}: {e}"))

        Class.objects.bulk_create(classes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(classes)} classes'))
