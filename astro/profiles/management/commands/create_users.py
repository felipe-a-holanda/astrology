from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('users.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                u = User()

                u.username = row['username']
                u.email = row['email']
                u.first_name = row['first_name']
                u.last_name = row['last_name']
                u.set_password(row['password'])

                u.save()
                print "User <%s> created" % u
