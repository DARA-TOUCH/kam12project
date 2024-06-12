from django.shortcuts import render
from django.http import HttpResponse
from shutil import copy2
from openpyxl import load_workbook
from django.conf import settings
import os
from baseoperations.kam12filewriter.acc_operation import AccReport


def import_stat_report(request):
    if request.method == 'POST':
        sad_file = request.FILES['sad_file']
        budget_file = request.FILES['budget_file']

        plain_acc_report_in = os.path.join(settings.STATIC_ROOT, 'excel/xlsx/acc_report.xlsx')
        plain_acc_report_out = os.path.join(settings.STATIC_ROOT, 'excel/xlsx/copied_acc_report_form.xlsx')

        copy2(plain_acc_report_in, plain_acc_report_out)

        acc_test = AccReport()
        acc_test.import_stat()

        acc_wb = load_workbook(plain_acc_report_out)

        acc_wb.save(plain_acc_report_out)
        acc_wb.close()

        # Prepare the response to download the file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Acc_Report.xlsx"'
        
        with open(plain_acc_report_out, 'rb') as f:
            response.write(f.read())
        os.remove(plain_acc_report_out)
        return response
    return render(request, 'acc_tool_form.html', {})


# def export_stat_report(request):
#     return render(request, 'acc_tool_form.html', {})