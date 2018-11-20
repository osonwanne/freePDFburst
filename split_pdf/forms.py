from django import forms
from django.core.validators import validate_email

from PyPDF2 import PdfFileReader, utils

class UploadPDF(forms.Form):
    file = forms.FileField()
    email = forms.CharField(
        max_length=250, help_text='Multiple email address should be seperated with a comma')

    def clean_file(self):
        data = self.cleaned_data['file']
        try:
            PdfFileReader(data.file)
        except utils.PdfReadError:
            raise forms.ValidationError('File must be in PDF format.')

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        email_list = data.split(',')
        total_number_of_emails = len(email_list)

        if len(email_list) > 1:
            validate_email.message = 'One or more email address(es) is not valid'

        for index in range(total_number_of_emails):
            email_list[index] = email_list[index].replace(' ','')
            validate_email(email_list[index])

        return data
