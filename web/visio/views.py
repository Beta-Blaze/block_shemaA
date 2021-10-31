from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CodeInputForm


def index(request):
    if request.method == 'POST':
        form = CodeInputForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = CodeInputForm()

    return render(request, 'code_input.html', {"form": form})
