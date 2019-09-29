import csv
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .model_prediction import max_sequence_len, model, generate_text

from .forms import TextForm

# from .forms import DocumentForm
# from .models import Document


# Create your views here.
from .models import Text


def home(request):
    return render(request, 'index.html')


def open(request):
    return render(request, 'open.html')


'''
def openFile(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            print(newdoc.docfile)
            # text = pytesseract.image_to_string(Image.open(newdoc.docfile), lang='eng', config='digits')

            if newdoc.docfile:
                # strip leading path from file name to avoid
                # directory traversal attacks
                fn = os.path.basename(newdoc.docfile)
                # open('/tmp/' + fn, 'wb').write(newdoc.file.read())
                message = 'The file "' + fn + '" was uploaded successfully'
            # writing data in data.doc file
            handle = open('data.doc', 'w+')
            handle.write("aaaaa")
            handle.close()

            # writing data in data.txt file
            textFile = open('data.txt', 'w+')
            textFile.write("aaaaa")
            textFile.close()

            ll = []

            with open('data.txt', 'r') as readFile:
                rr = readFile.readline()
                ll.append(rr)

            readFile.close()

            f = open('data.doc', 'r')

            for x in f:
                ll.append(x)

            file_content = ll
            f.close()

            # writing data in data.csv file
            with open('data.csv', 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(ll)
            csvFile.close()

            context = {'file_content': file_content}

            # Redirect to the document list after POST
            return render(request, 'showText.html', context)
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

'''


@csrf_exempt
def all_text(request):

    if request.method == 'POST':
        data = (request.POST['text'])
        resultValue = generate_text(data, 1, max_sequence_len, model)
        res = data + " " + resultValue[0]
    return HttpResponse(res)



def new(request):
    return render(request, 'index.html')

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = (request.POST['text'])
        response = HttpResponse(data)
        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=DownloadedText.doc'
        return response
    else:
        return HttpResponse("Error occured")


def showText(request):
    return render(request, 'showText.html')


def about(request):
    return render(request, 'about.html')
