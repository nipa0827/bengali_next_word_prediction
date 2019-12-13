import csv
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .model_prediction import generate_text
from django.shortcuts import render_to_response
from .forms import TextForm
from django.http import JsonResponse
import json
import io

# Create your views here.
from .models import Text


def home(request):
    return render(request, 'index.html')


def open(request):
    return render(request, 'open.html')


global filedata

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
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""

    if request.method == 'POST':
        data = (request.POST['text'])
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&amp;', ' ')

        text = data

        text = text.split("। ")
        text = text[len(text) - 1]

        resultValue = generate_text(text)
        first = resultValue[0]
        second = resultValue[1]
        third = resultValue[2]
        fourth = resultValue[3]
        fifth = resultValue[4]

    with io.open("data.txt", 'w', encoding='utf-8', errors='ignore') as f:
        data = data.replace("&nbsp;", ' ')
        data = data.replace('&amp;', ' ')
        f.write(data)

    data = {'first': first, 'second': second,
            'third': third, 'fourth': fourth,
            'fifth': fifth}
    return JsonResponse(data)


@csrf_exempt
def first_select(request):
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""
    res = ""
    if request.method == 'POST':
        data = (request.POST['text'])
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&amp;', ' ')

        text = data

        text = text.split("। ")
        text = text[len(text) - 1]
        resultValue = generate_text(text)
        res = data + " " + resultValue[0]

        text = res

        text = text.split("। ")
        text = text[len(text) - 1]

        resultValue = generate_text(text)
        if len(resultValue) < 5:
            for i in range(len(resultValue), 5):
                resultValue[i] = ""
        first = resultValue[0]
        second = resultValue[1]
        third = resultValue[2]
        fourth = resultValue[3]
        fifth = resultValue[4]

    with io.open("data.txt", 'w', encoding='utf-8', errors='ignore') as f:
        f.write(res.replace('&nbsp;', ' '))

    data = {'first': first, 'second': second,
            'third': third, 'fourth': fourth,
            'fifth': fifth, 'res': res}
    return JsonResponse(data)


@csrf_exempt
def second_select(request):
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""
    res = ""
    if request.method == 'POST':
        data = (request.POST['text'])
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&amp;', ' ')

        text = data

        text = text.split("। ")
        text = text[len(text) - 1]
        resultValue = generate_text(text)
        res = data + " " + resultValue[1]

        text = res

        text = text.split("। ")
        text = text[len(text) - 1]

        resultValue = generate_text(text)
        if len(resultValue) < 5:
            for i in range(len(resultValue), 5):
                resultValue[i] = ""
        first = resultValue[0]
        second = resultValue[1]
        third = resultValue[2]
        fourth = resultValue[3]
        fifth = resultValue[4]

    with io.open("data.txt", 'w', encoding='utf-8', errors='ignore') as f:
        f.write(res.replace('&nbsp;', ' '))

    data = {'first': first, 'second': second,
            'third': third, 'fourth': fourth,
            'fifth': fifth, 'res': res}


    return JsonResponse(data)


@csrf_exempt
def third_select(request):
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""
    res = ""
    if request.method == 'POST':
        data = (request.POST['text'])
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&amp;', ' ')

        text = data

        text = text.split("। ")
        text = text[len(text) - 1]
        resultValue = generate_text(text)
        res = data + " " + resultValue[2]

        text = res

        text = text.split("। ")
        text = text[len(text) - 1]

        resultValue = generate_text(text)
        if len(resultValue) < 5:
            for i in range(len(resultValue), 5):
                resultValue[i] = ""
        first = resultValue[0]
        second = resultValue[1]
        third = resultValue[2]
        fourth = resultValue[3]
        fifth = resultValue[4]

    with io.open("data.txt", 'w', encoding='utf-8', errors='ignore') as f:
        f.write(res.replace('&nbsp;', ' '))

    data = {'first': first, 'second': second,
            'third': third, 'fourth': fourth,
            'fifth': fifth, 'res': res}
    return JsonResponse(data)


@csrf_exempt
def fourth_select(request):
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""
    res = ""
    if request.method == 'POST':
        data = (request.POST['text'])
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&amp;', ' ')

        text = data

        text = text.split("। ")
        text = text[len(text) - 1]
        resultValue = generate_text(text)
        res = data + " " + resultValue[3]

        text = res

        text = text.split("। ")
        text = text[len(text) - 1]

        resultValue = generate_text(text)
        if len(resultValue) < 5:
            for i in range(len(resultValue), 5):
                resultValue[i] = ""
        first = resultValue[0]
        second = resultValue[1]
        third = resultValue[2]
        fourth = resultValue[3]
        fifth = resultValue[4]

    with io.open("data.txt", 'w', encoding='utf-8', errors='ignore') as f:
        f.write(res.replace('&nbsp;', ' '))

    data = {'first': first, 'second': second,
            'third': third, 'fourth': fourth,
            'fifth': fifth, 'res': res}

    return JsonResponse(data)


@csrf_exempt
def fifth_select(request):
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""
    res = ""
    if request.method == 'POST':
        data = (request.POST['text'])
        data = data.replace('&nbsp;', ' ')
        data = data.replace('&amp;', ' ')

        text = data

        text = text.split("। ")
        text = text[len(text) - 1]
        resultValue = generate_text(text)
        res = data + " " + resultValue[4]

        text = res

        text = text.split("। ")
        text = text[len(text) - 1]

        resultValue = generate_text(text)
        if len(resultValue) < 5:
            for i in range(len(resultValue), 5):
                resultValue[i] = ""
        first = resultValue[0]
        second = resultValue[1]
        third = resultValue[2]
        fourth = resultValue[3]
        fifth = resultValue[4]

    with io.open("data.txt", 'w', encoding='utf-8', errors='ignore') as f:
        f.write(res.replace('&nbsp;', ' '))

    data = {'first': first, 'second': second,
            'third': third, 'fourth': fourth,
            'fifth': fifth, 'res': res}

    return JsonResponse(data)


def suggestion(request):
    if request.method == 'POST':
        data = (request.POST['text'])
        resultValue = generate_text(data)


def new(request):
    return render(request, 'index.html')


def download(request):
    with io.open("data.txt", 'r', encoding='utf-8', errors='ignore') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="untitled.doc"'
    return response


def showText(request):
    return render(request, 'showText.html')


def about(request):
    return render(request, 'about.html')

