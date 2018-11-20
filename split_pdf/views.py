from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadPDF
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.utils import  PdfReadError
from django.core.mail import get_connection
from django.conf import settings
from django.core.mail.message import EmailMessage
import os

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = UploadPDF(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            recipient_list = data['email']
            try:
                get_email_message(request.FILES.get('file'), recipient_list)
                messages.success(request, 'PDF burst and sent successfully!')
            except PdfReadError:
                messages.error(request, 'Oops! Something seems to be wrong with the PDF file.')
            form = UploadPDF()

        return render(request, 'freePDFburst/index.html', {'form': form})
        
    form = UploadPDF()
    return render(request, 'freePDFburst/index.html', {'form': form})


def get_email_message(pdf_to_be_split, recipient_list):
    subject = 'Test'
    body = 'Hello,\n\nThis is an automated email message.\n\nPlease see attached.'
    from_email = 'info@school-lms.site'
    to_email = recipient_list
    infile = PdfFileReader(pdf_to_be_split)
    total_pages = infile.getNumPages()
    email_messages = []
    attached_files = []
    for i in range(total_pages):
        p = infile.getPage(i)
        outfile = PdfFileWriter()
        outfile.addPage(p)
        filename = 'Page {i} of {total_num_pages} - {file_name}'.format(i=str(i + 1), total_num_pages=total_pages, file_name=pdf_to_be_split.name)
        attached_files.append(filename)
        #to_email must be a list or tuple
        email = EmailMessage(subject, body, from_email, [to_email])
        
        with open(filename, 'wb') as f:
            outfile.write(f)
        f.close()

        email.attach_file(path=filename, mimetype=pdf_to_be_split.content_type)
        email_messages.append(email)

    connection = get_connection(
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        fail_silently=False,
    )
    connection.send_messages(email_messages)
    for file in attached_files:
        os.remove(file)

    return 'aaa'