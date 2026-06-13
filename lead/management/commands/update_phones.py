from django.core.management.base import BaseCommand
from ...services.lead.format_update_bulk_contacts import normalize_leads_service

class Command(BaseCommand):
    help = 'Update lead phone numbers with custom parameters'

    def add_arguments(self, parser):
        # The two requested parameters
        parser.add_argument(
            '--test', 
            type=int, 
            help='Limit the number of records to process for testing'
        )
        parser.add_argument(
            '--batch_size', 
            type=int, 
            default=500, 
            help='Number of records to process per database write'
        )

    def handle(self, *args, **options):
        test_val = options['test']
        batch_val = options['batch_size']

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Starting: test_limit={test_val}, batch_size={batch_val}"
        ))

        # Call the decoupled service
        count = normalize_leads_service(
            test_limit=test_val,
            batch_size=batch_val,
            logger=self.stdout
        )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully processed total of {count} records."
        ))