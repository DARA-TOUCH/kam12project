from django.urls import path
from .views import ImportStatReport, DownloadAccReportForm, download_acc_report_form, upload_form

app_name = 'acc_report'


urlpatterns = [
    path('api/import-stat-report/', ImportStatReport.as_view(), name='import_stat_report_api'),
    # path('import-stat-report/', import_stat_report_view, name='import_stat_report_view'),
    path('download-acc-report-form/', download_acc_report_form, name='download_acc_report_form'),
    path('api/download-acc-report-form/', DownloadAccReportForm.as_view(), name='download_acc_report_form_api'),
    path('upload-form/', ImportStatReport.as_view(), name='upload_form'),

]

