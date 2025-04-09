from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
import csv
from django.db import transaction

class Command(BaseCommand):
    help = 'Import students from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    if 'roll_number' in row:
                        user = User.objects.create_user(
                            username=row['username'],
                            password=row['password'],
                            email=row.get('email', f"{row['username']}@example.com"), 
                            first_name=row['name'].split()[0],
                            last_name=row['name'].split()[-1] if len(row['name'].split()) > 1 else ''
                        )
                        Student.objects.create(
                            user=user,
                            name=row['name'],
                            roll_number=row['roll_number'],
                            class_group=row['class_group'],
                            email=row.get('email', f"{row['username']}@example.com")  
                        )
        self.stdout.write(self.style.SUCCESS('Successfully imported students'))