from django.core.management.base import BaseCommand
from django.db import connections, OperationalError
import psycopg2
from django.conf import settings

class Command(BaseCommand):
    help = "it checks the database and creates it if it doesn't exist."

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        try:
            # Try to connect DB
            conn = connections['default']
            conn.cursor()
            self.stdout.write(self.style.SUCCESS(f"✅ DB found: {db_name}"))

        except OperationalError:
            self.stdout.write(self.style.WARNING(f"⚠️ The DB is not found! '{db_name}' creating DB..."))

            # Create DB by connecting to PostgreSQL
            try:
                conn = psycopg2.connect(
                    dbname="postgres", user=db_user, password=db_password, host=db_host, port=db_port
                )
                conn.autocommit = True
                cursor = conn.cursor()
                cursor.execute(f'CREATE DATABASE {db_name};')
                self.stdout.write(self.style.SUCCESS(f"✅ DB is created: {db_name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error occurred while creating DB: {e}"))

            finally:
                if conn:
                    conn.close()
