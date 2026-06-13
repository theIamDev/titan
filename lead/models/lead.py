from django.db import models
from .leadModelManager import LeadManager
from .workflowModels import Stage, Status

class Lead(models.Model):
    name = models.CharField(blank=False,null=True,max_length=1000)
    email = models.CharField(blank=False,null=True,max_length=1000)
    contact = models.CharField(blank=False,null=True,max_length=1000)
    valid_contact = models.CharField(blank=False,null=True,max_length=1000)
    lead_type = models.CharField(blank=False,null=True,max_length=1000)
    query = models.CharField(blank=False,null=True,max_length=1000)
    recieved_date = models.CharField(blank=False,null=True,max_length=1000)
    interested_in = models.CharField(blank=False,null=True,max_length=1000)
    assigned_to = models.IntegerField(blank = False, null = True)
    source_assigned = models.CharField(blank=False,null=True,max_length=1000)
    product_code  = models.CharField(blank=False,null=True,max_length=1000)
    product_type = models.CharField(blank=False,null=True,max_length=1000)
    follow_up_current_status = models.CharField(blank=False,null=True,max_length=1000)
    source = models.CharField(blank=False,null=True,max_length=1000)
    status = models.IntegerField(blank = False, null = True, default=1)
    priority = models.CharField(blank=False,null=True,max_length=10,default='cold')
    account = models.IntegerField(blank = False, null = True)
    organization = models.ForeignKey(
        'organization.Organizations', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column='organization'
    )
    location = models.ForeignKey(
        'organization.Locations', 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column='location'     
    )
    state = models.CharField(blank = False, null = True,max_length=20)
    created_by = models.CharField(blank = False, null = True,max_length=10)
    created_dt = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(blank = False, null = True,max_length=10)
    last_updated_dt = models.DateTimeField(auto_now=True)
    revenue = models.IntegerField(blank = False, null = True)
    brokerage = models.IntegerField(blank = False, null = True)
    hash_key = models.CharField(blank=False,null=True,max_length=100)
    golden = models.CharField(blank=False,null=True,max_length=10)
    sess_id = models.IntegerField(blank = False, null = True)
    lead_status = models.ForeignKey(
        Status, null=True, blank=True,
        on_delete=models.PROTECT, related_name='leads'
    )
    lead_stage = models.ForeignKey(
        Stage, null=True, blank=True,
        on_delete=models.PROTECT, related_name='leads'
    )

    objects = LeadManager()
    
    


        
    
    
    


