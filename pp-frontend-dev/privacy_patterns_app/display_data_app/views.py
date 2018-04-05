from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import models
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from display_data_app.forms import DataTypeForm, LocationForm, IndustryForm
from display_data_app.models import DataEntry, UserModel, Recommendation
from display_data_app.import_data import Importer 
from display_data_app.export_data import Exporter 

#homepage 
def index(request): 
	# Importer(cases_csv='display_data_app/ftc_cases_to_add.csv').populate_database(REPLACE=False)
	Exporter().export() 
	exit() 

	#populate_database()
	return render(request, 'index.html')

#helper for DataVisView
def is_valid(data_entry, data_types, locations, industries): 
	if data_entry.location in locations and data_entry.company_type_key in industries: 
		data_entry_data_types = ast.literal_eval(data_entry.data_type)
		for data_type in data_entry_data_types: 
			if data_type in data_types: 
				return True # return if they share at least one data type 
		return True 
	else: 
		return False 

class DataVisView(TemplateView):
	template_name = "data_vis.html"

	def data_types(self): 
		user = UserModel.objects.get(id=1)  
		return ast.literal_eval(user.data_type)

	def locations(self): 
		user = UserModel.objects.get(id=1)  
		return ast.literal_eval(user.location)

	def industries(self): 
		user = UserModel.objects.get(id=1)  
		return ast.literal_eval(user.industries)

	def data(self): 
		user = UserModel.objects.get(id=1)  
		data_type_list = ast.literal_eval(user.data_type)
		locations_list = ast.literal_eval(user.location)
		industries_list = ast.literal_eval(user.industries)

		data = set() 
		for data_entry in DataEntry.objects.all(): 
			if is_valid(data_entry, data_type_list, locations_list, industries_list): 
				data.add(data_entry.id)
	
		return DataEntry.objects.filter(id__in = list(data)) 

class form1(FormView): 
	form_class = DataTypeForm 
	template_name = 'data_search_form_1.html'
	success_url = 'form2'

	def form_valid(self, form):
		#create user 
		UserModel.objects.all().delete() 
		action_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2')
		new_user = UserModel(data_usage=action_list)
		new_user.id = 1 
		new_user.save() 
		return super(form1, self).form_valid(form)

class form2(FormView): 
	form_class = LocationForm
	template_name = 'data_search_form_2.html'
	success_url = 'form3'

	def form_valid(self, form):
		locations_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') + self.request.POST.getlist('field3') + self.request.POST.getlist('field4')

		#select user 
		user = UserModel.objects.get(id=1)      
		user.location = locations_list
		user.save() 
		return super(form2, self).form_valid(form)

class form3(FormView): 
	form_class = IndustryForm
	template_name = 'data_search_form_3.html'
	success_url = 'data-vis'

	def form_valid(self, form):
		industries_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') 
		print(industries_list) 

		#select user 
		user = UserModel.objects.get(id=1)      
		user.industries = industries_list
		user.save() 
		return super(form3, self).form_valid(form)

def faq(request): 
	return render(request, 'faq.html')

def glossary(request): 
	return render(request, 'glossary.html')

def data_search_info(request): 
	return render(request, 'data_search_info.html')

class AboutUs(TemplateView): 
	template_name = 'about_us.html'
