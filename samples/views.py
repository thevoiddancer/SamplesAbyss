from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>SamplesAbyss Home</h1><p>This will be the landing page. It will hold basic info and last added samples.</p>')

def browse(request):
    return HttpResponse('<h1>Browse SamplesAbyss</h1><p>This is browse landing page, showing an alphabetical list of bands.</p>')

def search(request):
    return HttpResponse('<h1>Search SamplesAbyss</h1><p>This is search landing page, showing fields to input text in.</p>')

def contribute(request):
    return HttpResponse('<h1>Contribute to SamplesAbyss</h1><p>This is contribute landing page, showing a field to add more samples.</p>')

