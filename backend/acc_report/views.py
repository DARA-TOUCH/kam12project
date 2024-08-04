import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from baseoperations.kam12filewriter.acc_operation import AccReport

from .serializers import FileUploadSerializer
from .forms import FileUploadForm

class ImportStatReport(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            sad_file = serializer.validated_data['sad_file']
            budget_file = serializer.validated_data['budget_file']

            # Save the files temporarily
            sad_file_path = os.path.join(settings.MEDIA_ROOT, sad_file.name)
            budget_file_path = os.path.join(settings.MEDIA_ROOT, budget_file.name)  

            with open(sad_file_path, 'wb+') as destination:
                for chunk in sad_file.chunks():
                    destination.write(chunk)
                    
            with open(budget_file_path, 'wb+') as destination:
                for chunk in budget_file.chunks():
                    destination.write(chunk)

            # Process the files
            acc_report = AccReport(sad_file_path, budget_file_path)
            acc_report.get_import_stat()

            # Path to the output excel file
            out_acc_report_path = os.path.join(settings.STATIC_ROOT, 'excel/xlsx/out_acc_report.xlsx')

            # Prepare the response to download the file
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="Acc_Report.xlsx"'
            
            with open(out_acc_report_path, 'rb') as f:
                response.write(f.read())

            # Cleanup: remove the uploaded files if needed
            os.remove(sad_file_path)
            os.remove(budget_file_path)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DownloadAccReportForm(APIView):
    def post(self, request, *args, **kwargs):
        acc_report_excel_file = os.path.join(settings.STATIC_ROOT, 'excel/xlsx/out_acc_report.xlsx')

        # Check if the file exists
        if not os.path.exists(acc_report_excel_file):
            return Response({'Error': 'File not fount'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the response to download the file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(acc_report_excel_file)}"'
        
        # Read the file and attach it to the response
        with open(acc_report_excel_file, 'rb') as f:
            response.write(f.read())
        
        return response

def upload_form(request):
    return render(request, 'acc_tool.html', {})
            
# def import_stat_report_view(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             sad_file = request.FILES['sad_file']
#             budget_file = request.FILES['budget_file']

#             # Save the files temporarily
#             sad_file_path = os.path.join(settings.MEDIA_ROOT, sad_file.name)
#             budget_file_path = os.path.join(settings.MEDIA_ROOT, budget_file.name)  

#             with open(sad_file_path, 'wb+') as destination:
#                 for chunk in sad_file.chunks():
#                     destination.write(chunk)
                    
#             with open(budget_file_path, 'wb+') as destination:
#                 for chunk in budget_file.chunks():
#                     destination.write(chunk)

#             # Process the files
#             acc_report = AccReport()
#             acc_report.get_import_stat()

#             # Path to the output excel file
#             out_acc_report_path = os.path.join(settings.STATIC_ROOT, 'excel/xlsx/out_acc_report.xlsx')

#             # Prepare the response to download the file
#             response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename="Acc_Report.xlsx"'
            
#             with open(out_acc_report_path, 'rb') as f:
#                 response.write(f.read())

#             # Cleanup: remove the uploaded files if needed
#             os.remove(sad_file_path)
#             os.remove(budget_file_path)

#             return response
#     else:
#         form = FileUploadForm()

#     return render(request, 'acc_tool_form.html', {'form': form})


def download_acc_report_form(request):
    if request.method == 'POST':
        acc_report_excel_file = os.path.join(settings.STATIC_ROOT, 'excel/xlsx/out_acc_report.xlsx')
        # Prepare the response to download the file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(acc_report_excel_file)}"'
        # Read the file and attach it to the response
        with open(acc_report_excel_file, 'rb') as f:
            response.write(f.read())
    
        return response
    
    return render(request, 'acc_custom_tool.html', {})