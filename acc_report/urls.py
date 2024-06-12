from django.urls import path
from .views import import_stat_report

app_name = 'acc_report'

urlpatterns = [
    # path('Accounting Tool', view=acc_tool, name='acc_tool'), 
    path('Acc report processing', view=import_stat_report, name='import_stat_report'),
]