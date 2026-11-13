from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>AgroFeira Paragominas</h1>")
