from django.urls import path
from .controller.leadController import LeadList,LeadDetail, Export
from .controller.leadController import LeadActions,SearchLead
# workflow and status
from .controller.pipelineController import LeadPipeline
from .controller.timelineController import Timeline_V1
from .controller.ownersController import Owners

from .views import LDCNTRL
from .controller.analyticsController import (
    Leads_Generated,
    Home_Dashboard_Kpi,
    Stage_Pipeline,
    Stage_Velocity,
    Conversion_Distribution,
    Team_Performance,
    USER_ACTIONS
    )

urlpatterns = [
    path('', LeadList.as_view()),
    path('<int:id>', LeadDetail.as_view()),
    path('search', SearchLead.as_view()),
    path('export', Export.as_view()),
    path('timeline', Timeline_V1.as_view()),
    path('load-control', LDCNTRL.as_view()),

    # custom api - change to patch soon
    path('lead-action',LeadActions.as_view()),

    # workflow and status
    path('pipeline',LeadPipeline.as_view()),

    # lead user
    path('owners',Owners.as_view()),

    # analytics
    path('analytics/leads-generated', Leads_Generated.as_view()),
    path('analytics/stage-pipeline', Stage_Pipeline.as_view()),
    path('analytics/stage-velocity', Stage_Velocity.as_view()),
    path('analytics/conversion-distribution', Conversion_Distribution.as_view()),
    path('analytics/team-performance', Team_Performance.as_view()),
    path('analytics/user-actions', USER_ACTIONS.as_view()),




    # home dashboard
    path('analytics/dashboard-kpi', Home_Dashboard_Kpi.as_view()),
    

    # Lead API
    # path('api/lead',Lead.as_view()),
    #path('api/lead/<int:id>', Lead.as_view()),
    # path('api/getall<int:lead_id>', Lead_V1.as_view()),
    # path('api/getall', Lead_V1.as_view()),

    # path('api/search', SearchLead.as_view()),

    # path('api/lead/timeline',Timeline.as_view()),
    # path('api/v1/timeline',Timeline_V1.as_view()),
    # path('api/lead/ldcntrl',LDCNTRL.as_view()),

    # custom api - change to patch soon
    # path('api/lead/leadaction',LeadActions.as_view()),

    # workflow and status
    #path('api/v1/lead/stage',Stage.as_view()),
  

    # analytics
    # path('api/analytics/leadsgenerated',Leads_Generated.as_view()),
    # path('api/analytics/homedashboardkpi',Home_Dashboard_Kpi.as_view()),


    # investigate and remove 
    #path('api/lead/status',Status.as_view()),
    #path('api/lead/status/<int:id>', Status.as_view()),
]





