
from ...models.ActivityTimelineLogModel import ActivityTimelineLog
    
def timeline_save(data):
    try:
        if isinstance(data, list):
            if not data:
                return {"success": True, "count": 0}
            # Use bulk_create for lists
            ActivityTimelineLog.objects.bulk_create(data)
            return {"success": True, "count": len(data)}
        else:
            # Handle single dictionary creation
            log = ActivityTimelineLog.objects.create(**data)
            return {"success": True, "id": log.id} # type: ignore
    except Exception as e:
        return {"success": False, "error": str(e)}