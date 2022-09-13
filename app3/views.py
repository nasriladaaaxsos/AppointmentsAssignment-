from django.shortcuts import render,redirect
from . import models  # import model is important 
from django.contrib import messages
from django.shortcuts import render, HttpResponse

# Get
def index(request):
    print("Testtttttttttttttt")
    return render(request, "indexx.html")  
