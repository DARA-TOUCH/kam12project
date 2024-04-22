from django.shortcuts import render
from shutil import copy2
from openpyxl import load_workbook

def acc_tool(request):
    return render(request, 'acc_tool_form.html', {})

def import_stat(request):
    if request.method == 'POST':
        sad_file = request.FILES['sad_file']
        budget_file = request.FILES['budget_file']

        acc_report_in = os.path.join(settings.STATIC_ROOT, 'excel/acc_report.xlsx')
        acc_report_out = os.path.join(settings.STATIC_ROOT, 'excel/Generated_Acc_Report.xlsx')

        copy2(acc_report_in, acc_report_out)

        acc_wb = load_workbook(acc_report_out)

        

    return render(request, 'acc_tool_form.html', {})