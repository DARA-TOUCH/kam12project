import shutil
import os
import glob
import pandas as pd
import openpyxl
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import FileResponse
from rest_framework import status
from rest_framework import status, viewsets

from baseoperations.kam12list01.list01 import List01
from baseoperations.kam12list01.salakabatt import AllSalakabatt

from django.http import HttpResponse

class List01View(View):
    """
    View to handle file uploads and generate a downloadable Excel file.
    Methods:
        get(request, *args, **kwargs):
            Renders the index.html template.
        post(request, *args, **kwargs):
            Handles the file upload, processes the files, and returns a downloadable Excel file.
    Attributes:
        None
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        sad_detail = request.FILES.get('sad_detail')
        budget = request.FILES.get('budget')
        salakabatt = request.FILES.get('salakabatt')

        list01_template = os.path.join(settings.BASE_DIR, 'staticfiles', 'excel', 'xlsx', 'List01_Template.xlsx')
        list01_copy = os.path.join(settings.BASE_DIR, 'staticfiles', 'excel', 'xlsx', 'List01.xlsx')
    
        # Ensure the directory exists
        os.makedirs(os.path.dirname(list01_copy), exist_ok=True)
        shutil.copy2(list01_template, list01_copy)

        # if not sad_detail or not budget:
        #     return Response({'error': 'Please upload both files'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a temporary directory if it doesn't exist
        temp_dir = os.path.join(settings.BASE_DIR, 'temp', 'list01')
        os.makedirs(temp_dir, exist_ok=True)

        sad_detail_path = os.path.join(temp_dir, 'sad_detail.xlsx')
        budget_path = os.path.join(temp_dir, 'budget.xlsx')
        salakabatt_path = os.path.join(temp_dir, 'salakabatt.xlsx')

        # Save the uploaded files to the temporary directory
        with open(sad_detail_path, 'wb+') as destination:
            for chunk in sad_detail.chunks():
                destination.write(chunk)

        with open(budget_path, 'wb+') as destination:
            for chunk in budget.chunks():
                destination.write(chunk)

        with open(salakabatt_path, 'wb+') as destination:
            for chunk in salakabatt.chunks():
                destination.write(chunk)

        list01 = List01(
            template_file=list01_copy, 
            budget_file=budget_path, 
            sad_detail_file=sad_detail_path, 
            list_of_salakabatt_path=[salakabatt_path]
            )
        list01.write()

        # Serve the file as a downloadable response
        response = FileResponse(open(list01_copy, 'rb'), as_attachment=True, filename='List01.xlsx')
        response['Content-Disposition'] = 'attachment; filename="List01.xlsx"'

        return response


class SalakabattDataView(View):
    file_labels = ['File 1', 'File 2', 'File 3', 'File 4', 'File 5', 'File 6', 'File 7', 'File 8', 'File 9', 'File 10', 'File 11', 'File 12']
    
    def get(self, request, *args, **kwargs):
        return render(request, 'salakabatt.html', {'file_labels': enumerate(self.file_labels, start=1)})

    def post(self, request, *args, **kwargs):
        # Get all uploaded files into a list
        files = [request.FILES.get(f'file{i}') for i in range(1, len(self.file_labels) + 1)]
        
        # Create the temp directory
        tem_dir = os.path.join(settings.BASE_DIR, 'temp', 'salakabatt')
        os.makedirs(tem_dir, exist_ok=True)  # Creates the directory if it doesn't exist

        existing_files = glob.glob(os.path.join(tem_dir, '*.xlsx'))
        for file_path in existing_files:
            os.remove(file_path)
        
        # Iterate over the files and save them with dynamic filenames
        for i, file in enumerate(files, start=1):
            if file:  # Check if the file exists
                file_path = os.path.join(tem_dir, f'file{i}.xlsx')
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
        
        uploaded_files = glob.glob(os.path.join(tem_dir, '*.xlsx'))

        salakabatt = AllSalakabatt(uploaded_files)
        tax_data = salakabatt.tax_data
        non_tax_data = salakabatt.non_tax_data

        # Create an Excel file with 2 sheets: tax_data and non_tax_data
        output_file = os.path.join(tem_dir, 'salakabatt_data.xlsx')
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            tax_data.to_excel(writer, sheet_name='Tax Data', index=False)
            non_tax_data.to_excel(writer, sheet_name='Non-Tax Data', index=False)
        
        # Save the path to the output file in the session or pass it as context
        request.session['output_file'] = output_file
        # Set a success message and redirect to the same page
        messages.success(request, "File has been successfully generated. Click the link below to download it.")

        return render(request, 'download.html')


class DownloadSalakabattDataView(View):
    def get(self, request, *args, **kwargs):
        # Get the file path from the session
        output_file = request.session.get('output_file')
        if output_file and os.path.exists(output_file):
            return FileResponse(open(output_file, 'rb'), as_attachment=True, filename='salakabatt_data.xlsx')
        else:
            messages.error(request, "File not found.")
        return render(request, 'salakabatt.html')

def cleanup(request):
    items = ['VPP', 'VOP', 'VAP', 'SPP', 'SOP', 'COP']
    if request.method == 'POST':
        for index, item in enumerate(items, start=1):
            text_value = request.POST.get(f'item_{i}')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'cleanup_list01.html', {'items': items})

class List01MakeUpView(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'makeup_list01.html')

    def post(self, request, *args, **kwargs):
        single_sheet_tempalte = request.FILES.get('single_sheet_template')
        wb = openpyxl.load_workbook(single_sheet_tempalte)
        ws = wb.active
        ws.title = 'List01'
        for sheet in wb.worksheets:
            print(sheet.title)
        return render(request, 'makeup_list01.html')