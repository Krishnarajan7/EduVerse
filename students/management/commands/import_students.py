import csv
from django.core.management.base import BaseCommand
from students.models import Student
from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import students from a CSV file with login credentials'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            students = []
            for row in reader:
                username = row['roll_number'].lower()
                try:
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={'email': row['email']},
                    )
                    if created or not user.check_password('Student@123'):
                        user.set_password('Student@123')  # Hash the password
                        user.save()
                        logger.info(f"Created/updated user: {username}")
                    else:
                        logger.info(f"User exists: {username}")
                    student = Student(
                        user=user,
                        roll_number=row['roll_number'],
                        name=row['name'],
                        email=row['email'],
                        class_group_id=int(row['class_group_id']),
                        phone='',
                        address='',
                        dob=None,
                        profile_picture=None,
                        classes_attended=0,
                        total_classes=0,
                        changed_password=False,
                        gender=None,
                        father_name=None,
                        mother_name=None,
                        parent_phone=None,
                        community=None,
                        place_of_birth=None,
                        admission_date=None,
                        admission_type=None
                    )
                    students.append(student)
                except Exception as e:
                    logger.error(f"Error processing {username}: {str(e)}")
                    continue
            try:
                Student.objects.bulk_create(students)
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(students)} students with login credentials'))
            except Exception as e:
                logger.error(f"Bulk create failed: {str(e)}")
                self.stdout.write(self.style.ERROR(f'Failed to import students: {str(e)}'))