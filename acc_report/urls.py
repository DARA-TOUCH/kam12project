from django.urls import path
from .views import acc_tool

app_name = 'acc_report'

urlpatterns = [
    path('Accounting Tool', view=acc_tool, name='acc_tool')
]