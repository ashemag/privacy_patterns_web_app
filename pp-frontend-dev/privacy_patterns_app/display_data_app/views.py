from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import models
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from display_data_app.forms import * 
from display_data_app.models import DataEntry, UserModel, Recommendation, OPCDataEntry
from display_data_app.import_data import Importer 
from display_data_app.export_data import Exporter 
import ast 

#homepage 
def index(request): 
	# Importer().populate_database()
	#Exporter().export()
	#exit() 
	return render(request, 'index.html')

#helper for DataVisView
def is_valid(data_entry, data_types, locations, industries): 
	if data_entry.location in locations and data_entry.company_type_key in industries: 
		# data_entry_data_types = ast.literal_eval(data_entry.data_usage)
		data_entry_data_types = data_entry.data_usage
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
		arr = ast.literal_eval(user.data_usage)
		return ', '.join(arr)

	def locations(self): 
		user = UserModel.objects.get(id=1)  
		arr = ast.literal_eval(user.location)
		return ', '.join(arr)

	def industries(self): 
		user = UserModel.objects.get(id=1)  
		arr = ast.literal_eval(user.industries)
		return ', '.join(arr)

	def data(self): 
		user = UserModel.objects.get(id=1)  
		data_type_list = ast.literal_eval(user.data_usage)
		locations_list = ast.literal_eval(user.location)
		industries_list = ast.literal_eval(user.industries)

		data = set() 
		for data_entry in DataEntry.objects.all(): 
			if is_valid(data_entry, data_type_list, locations_list, industries_list): 
				data.add(data_entry.id)
	
		return DataEntry.objects.filter(id__in = list(data)) 

def faq(request): 
	return render(request, 'faq.html')

def glossary(request): 
	return render(request, 'glossary.html')

def data_search_info(request): 
	return render(request, 'data_search_info.html')

def choose_jurisdiction(request): 
	return render(request, 'choose_jurisdiction.html')

class AboutUs(TemplateView): 
	template_name = 'about_us.html'

# FTC FORMS 
class form1(FormView): 
	form_class = DataTypeForm 
	template_name = 'data_search_form_1.html'
	success_url = 'ftc-form2'

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
	success_url = 'ftc-form3'

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
	success_url = 'ftc-data'

	def form_valid(self, form):
		industries_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') 

		#select user 
		user = UserModel.objects.get(id=1)      
		user.industries = industries_list
		user.save() 
		return super(form3, self).form_valid(form)

# OPC FORMS 
class opc_form1(FormView): 
	form_class = SectorsForm 
	template_name = 'data_search_opc_form_1.html'
	success_url = 'opc-form2'

	def form_valid(self, form):
		#create user 
		UserModel.objects.all().delete() 
		sectors_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2')
		new_user = UserModel(sectors=sectors_list)
		new_user.id = 1 
		new_user.save() 
		return super(opc_form1, self).form_valid(form)

class opc_form2(FormView): 
	form_class = TopicsForm 
	template_name = 'data_search_opc_form_2.html'
	success_url = 'opc-form3'

	def form_valid(self, form):
		topics_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') 

		#select user 
		user = UserModel.objects.get(id=1)      
		user.topics = topics_list
		user.save() 
		return super(opc_form2, self).form_valid(form)

class opc_form3(FormView): 
	form_class = ComplaintTypesForm 
	template_name = 'data_search_opc_form_3.html'
	success_url = 'opc-form4'

	def form_valid(self, form):
		complaint_types_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') 

		#select user 
		user = UserModel.objects.get(id=1)      
		user.complaint_types = complaint_types_list
		user.save() 
		return super(opc_form3, self).form_valid(form)

class opc_form4(FormView): 
	form_class = DispositionsForm 
	template_name = 'data_search_opc_form_4.html'
	success_url = 'opc-data'

	def form_valid(self, form):
		dispositions_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') 

		#select user 
		user = UserModel.objects.get(id=1)      
		user.dispositions = dispositions_list
		user.save() 
		return super(opc_form4, self).form_valid(form)

#helper for OPCDataVisView
def is_valid_opc(data_entry, sectors_list, topics_list, complaint_types_list, dispositions_list): 	
	for sector in data_entry.sectors.split(';'): #sectors in data entry 
		if sector in sectors_list: #if it matches something in list display it 
			return True 
	for topic in data_entry.topics.split(';'): 
		if topic in topics_list: 
			return True 
	for complaint_type in data_entry.complaint_types.split(';'): 
		if complaint_type in complaint_types_list: 
			return True 
	for disposition in data_entry.dispositions.split(';'): 
		if disposition in dispositions_list: 
			return True 
	return False 

class OPCDataVisView(TemplateView):
	template_name = "opc_data_vis.html"

	def sectors(self): 
		user = UserModel.objects.get(id=1) 
		arr = ast.literal_eval(user.sectors)
		return ', '.join(arr)

	def complaint_types(self): 
		user = UserModel.objects.get(id=1)  
		arr = ast.literal_eval(user.complaint_types)
		return ', '.join(arr)

	def topics(self): 
		user = UserModel.objects.get(id=1)  
		arr = ast.literal_eval(user.topics)
		return ', '.join(arr)

	def dispositions(self): 
		user = UserModel.objects.get(id=1)  
		arr = ast.literal_eval(user.dispositions)
		return ', '.join(arr)

	def data(self): 
		user = UserModel.objects.get(id=1)  
		sectors_list = ast.literal_eval(user.sectors)
		complaint_types_list = ast.literal_eval(user.complaint_types)
		topics_list = ast.literal_eval(user.topics)
		dispositions_list = ast.literal_eval(user.dispositions)

		data = set() 
		for data_entry in OPCDataEntry.objects.all(): 
			if is_valid_opc(data_entry, sectors_list, topics_list, complaint_types_list, dispositions_list): 
				data.add(data_entry.id)
	
		return OPCDataEntry.objects.filter(id__in = list(data)) 





