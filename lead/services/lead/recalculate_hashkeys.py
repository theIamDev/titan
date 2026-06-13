from ..utils.hashing import Hashing 
from ...models import Lead
from django.db import transaction

def __calc_hash_key(*params):
    hash_key = Hashing(params).hash()
    return hash_key

def recalculate_hashkeys(test_limit=None, batch_size=500, logger=None):
    """Recalculate hashkeys for lead records based on valid_contact field."""
    # Only fetch records that actually have contact info to hash
    queryset = Lead.objects.filter(valid_contact__isnull=False).only('id', 'hash_key', 'valid_contact')

    if test_limit:
        queryset = queryset[:test_limit]
        
    # .iterator() keeps memory usage low by streaming records
    records = queryset.iterator(chunk_size=batch_size)
    batch = []
    total_processed = 0

    for lead in records:
        new_hash = __calc_hash_key(lead.valid_contact)
        
        # Only add to batch if an actual change is needed
        if lead.hash_key != new_hash:
            lead.hash_key = new_hash
            batch.append(lead)
        
        if len(batch) >= batch_size:
            with transaction.atomic():
                Lead.objects.bulk_update(batch, ['hash_key'])
            total_processed += len(batch)
            if logger:
                logger.write(f"Updated {total_processed} records...")
            batch = []

    # Final cleanup: Fixed the field name from 'valid_contact' to 'hash_key'
    if batch:
        with transaction.atomic():
            Lead.objects.bulk_update(batch, ['hash_key'])
        total_processed += len(batch)

    return total_processed
