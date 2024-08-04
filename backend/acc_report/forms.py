from django import forms


class FileUploadForm(forms.Form):
    sad_file = forms.FileField()
    budget_file = forms.FileField()