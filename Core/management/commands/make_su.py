"""Core > management > commands > wait_for_db.py"""
# PYTHON IMPORTS
import time
# DJANGO IMPORTS
from django.core.management.base import BaseCommand
from Core.models import User


class Command(BaseCommand):
    """Command to pause execution until database is available"""

    def handle(self, *args, **options):
        """handler function"""
        username = "01710835653"
        password = "admin123#"
        user, created = User.objects.get_or_create(phone=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Superuser created {user.__dict__}"))
