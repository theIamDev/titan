from django.db import transaction
from ...models.lead import Lead
from packages.formatParsers.phoneNumberParser import validate_and_format_phone_number

def normalize_leads_service(test_limit=None, batch_size=500, logger=None):
    """
    Decoupled service logic for phone normalization.
    """
    # 1. Fetch only NULL records (Resumable)
    queryset = Lead.objects.filter(valid_contact__isnull=True).only('id', 'contact', 'valid_contact')
    
    if test_limit:
        queryset = queryset[:test_limit]
    
    # 2. Generator-based iterator (Memory efficient)
    records = queryset.iterator(chunk_size=batch_size)
    batch = []
    total_processed = 0

    for lead in records:
        raw_contact = str(lead.contact).strip() if lead.contact else ""
        
        try:
            formatted = validate_and_format_phone_number(raw_contact)
            # If invalid, we store raw_contact to clear the NULL state
            lead.valid_contact = formatted if formatted else raw_contact
        except Exception as e:
            lead.valid_contact = raw_contact
            if logger:
                logger.write(f"Error on ID {lead.id}: {e}") # type: ignore

        batch.append(lead)

        # 3. Batch processing
        if len(batch) >= batch_size:
            with transaction.atomic():
                Lead.objects.bulk_update(batch, ['valid_contact'])
            total_processed += len(batch)
            if logger:
                logger.write(f"Updated {total_processed} records...")
            batch = []

    # Final cleanup
    if batch:
        with transaction.atomic():
            Lead.objects.bulk_update(batch, ['valid_contact'])
        total_processed += len(batch)

    return total_processed