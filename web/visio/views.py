from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CodeInputForm


def index(request):
    exception = None
    if request.method == 'POST':
        form = CodeInputForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
        else:
            exception = "Форма заполнена некорретно, либо прикрепленный файл - не код"
    else:
        form = CodeInputForm()

    return render(request, 'code_input.html', {"form": form, "exception": exception})
