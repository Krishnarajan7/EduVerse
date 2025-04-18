import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faculty.models import Faculty
from pathlib import Path
from datetime import datetime

class Command(BaseCommand):
    help = 'Import faculty from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing faculty instead of skipping'
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
                email = row['email']
                username = row['username']
                roll_number = row['roll_number']

                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={'email': email}
                )
                if user_created:
                    user.set_password(row['password'])
                    user.save()

                try:
                    faculty = Faculty.objects.get(email=email)
                    if update_existing:
                        faculty.name = row['name']
                        faculty.roll_number = roll_number
                        faculty.department = row['department']
                        faculty.username = username
                        faculty.user = user
                        faculty.phone = row.get('phone') or None
                        faculty.dob = self.parse_date(row.get('dob'))
                        faculty.profile_picture = row.get('profile_picture') or None
                        faculty.save()
                        updated_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Updated: {email}"))
                    else:
                        skipped.append({**row, 'reason': 'duplicate_email'})
                        continue

                except Faculty.DoesNotExist:
                    if Faculty.objects.filter(roll_number=roll_number).exists():
                        skipped.append({**row, 'reason': 'duplicate_roll_number'})
                        continue

                    Faculty.objects.create(
                        user=user,
                        username=username,
                        name=row['name'],
                        roll_number=roll_number,
                        department=row['department'],
                        email=email,
                        phone=row.get('phone') or None,
                        dob=self.parse_date(row.get('dob')),
                        profile_picture=row.get('profile_picture') or None
                    )
                    created_count += 1

        # Log skipped entries
        if skipped:
            log_path = Path("skipped_faculty_log.csv")
            with open(log_path, 'w', newline='') as log_file:
                fieldnames = list(skipped[0].keys())
                writer = csv.DictWriter(log_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(skipped)
            self.stdout.write(self.style.WARNING(f"Skipped {len(skipped)} entries. Logged to '{log_path}'"))

        self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
        if update_existing:
            self.stdout.write(self.style.SUCCESS(f"Updated: {updated_count}"))

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        except ValueError:
            return None
