"""
Django management command for waiting for the postgres db to finish setting up.
"""
import time

from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for commands"""
        self.stdout.write("Waiting for database connection ... ")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])  # check for problems method
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    self.style.WARNING("Database unavailable, Waiting ...")
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available"))
