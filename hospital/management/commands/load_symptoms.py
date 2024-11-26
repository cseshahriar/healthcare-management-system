import logging
import pandas as pd
from django.utils import timezone
from django.core.management.base import BaseCommand
from hospital.models import Speciality, Symptom

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Load symptom data from Excel file into the
        command: python manage.py load_symptom symptoms.xlsx
        """

    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str)

    def handle(self, *args, **options):
        file_name = options['file_name']
        excel_file_path = f'./fixtures/{file_name}'
        df = pd.read_excel(excel_file_path, header=None)  # Don't use header
        df.fillna("", inplace=True)  # Replace NaN values with empty strings
        for index, row in df.iterrows():
            if index > 1 and row[0] != '':  # titles skip
                speciality_text = row[0]
                speciality_obj = Speciality.objects.filter(name__iexact=speciality_text).first()
                symptoms = row[1].split(',')  # list
                if speciality_obj:
                    for symptom_name in symptoms:
                        symptom_obj, created = Symptom.objects.get_or_create(
                            speciality=speciality_obj, name=symptom_name
                        )
                        logger.info(f"symptom_obj created {symptom_obj}")
        self.stdout.write(
            self.style.SUCCESS(
                'Tubewell data entry script successfully close'
            )
        )
