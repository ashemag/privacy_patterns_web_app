from django.shortcuts import render, redirect
from django.db import models
from django.views.generic import TemplateView, CreateView
from display_data_app.forms import FilterForm
from display_data_app.models import FilterModel

#from django.views import View

# Create your views here.
# class HomePage(TemplateView): 
# 	print("HERE!")
# 	template_name = 'index.html'

def process(request): 
	print("REACHED HERE!!!")
	print(request.POST.get('value'))
	# if request.method == 'POST':
	# 	form = FilterForm(request.POST)
	# 	print(form['choice'])
	return redirect('home')

class CreateMyModelView(CreateView):
    print("reached model")
    model = FilterModel
    form = FilterForm
    template_name = 'index.html'
    fields = ['filter_options'] #neccessary 
    def form_valid(self, form):
    	print(form['filter_options'].value().upper())    	
    	return redirect('home')
    	