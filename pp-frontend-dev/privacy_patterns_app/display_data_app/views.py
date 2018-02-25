from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import models
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from display_data_app.forms import DataTypeForm, LocationForm, IndustryForm
from display_data_app.models import DataEntry, UserModel
import csv 
import json 
import ast 
import collections

principle_id_to_counts = collections.Counter({'1.2.2': 43, '2.1.1': 21, '3.2.3': 20, '3.1.1': 20, '8.2.2': 18, '2.2.3': 18, '3.2.1': 16, '4.2.2': 16, '4.1.1': 14, '2.2.2': 14, '10.2.5': 13, '4.2.3': 13, '2.2.1': 13, '2.1.0': 13, '8.2.1': 12, '8.2.7': 11, '4.2.4': 10, '4.1.2': 10, '1.2.4': 9, '10.2.4': 9, '7.2.1': 9, '8.2.5': 9, '6.1.1': 8, '1.2.7': 8, '1.2.6': 8, '3.2.4': 8, '5.2.1': 7, '4.2.1': 7, '5.1.1': 6, '4.1.0': 6, '6.2.5': 5, '1.2.10': 5, '3.1.2': 5, '7.1.2': 5, '7.1.1': 5, '5.2.3': 5, '7.2.2': 5, '7.2.3': 4, '1.2.11': 4, '10.2.3': 4, '3.1.0': 4, '5.1.0': 4, '3.22.4': 3, '10.2.2': 3, '9.2.1': 3, '7.2.4': 3, '10.2.1': 3, '8.1.1': 3, '7.1.0': 2, '1.2.1': 2, '6.2.1': 2, '8': 2, '1.1.0': 2, '6.2.2': 2, '3.2.2': 2, '6.1.0': 2, '8.2.6': 2, '1.2.5': 2, '6.2.3': 2, '5.2.2': 1, '': 1, '7': 1, '8.2.3': 1, '3.2.3ñ 7.1..1': 1, '10.1.1': 1, '9.1.0': 1, '9.1.1': 1, '6.2.6': 1, '3.3.2': 1})


#helper method for populate_databases
def process_principles_for_entry(principle_ids, data): 
	tuples_list = []
	for principle in principle_ids: 
		tuples_list.append([principle, principle_id_to_counts[principle]])
	tuples_list = sorted(tuples_list, key=lambda tup: tup[1], reverse=True) 
	notes, subprinciples, pos_recs, data_types = [], [], [], []

	for principle, count in tuples_list: 
		if principle in data: 		
			subprinciple, note, pos_rec, data_type = data[principle]
			notes.append(note)
			subprinciples.append(subprinciple)
			pos_recs.append(pos_rec)
			data_types.append(data_type)
	return notes, subprinciples, pos_recs, data_types 
			
def populate_database(): 
	#get data from privacy_principles doc 
	filename = 'display_data_app/privacy_principles.csv'
	data = {}
	gap_principle_mapping = {}
	with open(filename) as csvfile: 
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader): 
			principle_id, subprinciple, note  = row['GAPP #'], row['GAPP Subprinciple'], row['GAPP Note']
			pos_rec, data_type = row['"Positive" Recommendation'], row['Actions with Data (from User Questionnaire)']
			data[principle_id] = [subprinciple, note, pos_rec, data_type]
			gap_principle_mapping[principle_id] = subprinciple

	processed_data = []
	filename2 = 'display_data_app/ftc_cases.csv'
	#count principles 
	ctr = []
	with open(filename2) as csvfile: 
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader): 
			principle_id, case_name = row['Privacy Principle - Primary'], row['Case Name']
			case_url, company_type_key, location, last_updated = row['Case URL'], row['Company Type Key'], row['Location'], row['Last Updated']
			principle_ids = [x.strip() for x in principle_id.split(';')]
			if principle_ids == ['']: 
				continue 
			if 'N/A' in principle_ids[0]: 
				continue 
			
			notes, subprinciples, pos_recs, data_types = process_principles_for_entry(principle_ids, data)

			data_type_temp = set() 
			for data_type in data_types: 
				if "," in data_type: 
					data_type_list = data_type.split(',')
					for data_type_entry in data_type_list: 
						data_type_temp.add(data_type)
				else: 
					data_type_temp.add(data_type)

			data_entry = [case_name, case_url, last_updated, location, company_type_key, ('\n\n').join(subprinciples), ('\n\n').join(notes), ('\n\n').join(pos_recs), list(data_type_temp)]
			processed_data.append(data_entry)
	
	ctr_dict = collections.Counter(ctr) #becomes principles_id_to_counts
	DataEntry.objects.all().delete() 

	#add data to model 
	for i, entry in enumerate(processed_data): 
		new_entry = DataEntry(case_name = entry[0], case_url = entry[1], last_updated=entry[2], location=entry[3], company_type_key=entry[4], subprinciple=entry[5], note=entry[6], pos_rec = entry[7], data_type=entry[8])
		new_entry.id = i + 1 
		new_entry.save() 
	print("completed data adding")
	exit() 

def index(request): 
	#populate_database()
	return render(request, 'index.html')

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
		print(DataEntry.objects.all())
		print("in data vis POST view")
		user = UserModel.objects.get(id=1)	
		data_type_list = ast.literal_eval(user.data_type)
		locations_list = ast.literal_eval(user.location)
		industries_list = ast.literal_eval(user.industries)

		data = set() 
		for data_entry in DataEntry.objects.all(): 
			if is_valid(data_entry, data_type_list, locations_list, industries_list): 
				data.add(data_entry.id)

	
		#return super(TemplateView, self).render_to_response(context)
		return DataEntry.objects.filter(id__in = list(data)) 

class form1(FormView): 
	form_class = DataTypeForm 
	template_name = 'data_search_form_1.html'
	success_url = 'form2'

	print("in form1 view")
	def form_valid(self, form):
		print("in form_valid")
		#create user 
		UserModel.objects.all().delete() 
		action_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2')
		print(action_list) 
		new_user = UserModel(data_type=action_list)
		new_user.id = 1 
		new_user.save() 
		return super(form1, self).form_valid(form)
	
	def form_invalid(self, form): 
		print("in form invalid")
		return super(form1, self).form_valid(form)

class form2(FormView): 
	form_class = LocationForm
	template_name = 'data_search_form_2.html'
	success_url = 'form3'

	def form_valid(self, form):
		locations_list = self.request.POST.getlist('field1') + self.request.POST.getlist('field2') + self.request.POST.getlist('field3') + self.request.POST.getlist('field4')
		print(locations_list) 

		#select user 
		user = UserModel.objects.get(id=1)		
		user.location = locations_list
		user.save() 
		return super(form2, self).form_valid(form)
	
	def form_invalid(self, form): 
		print("in form invalid")
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
	
	def form_invalid(self, form): 
		print("in form invalid")
		return super(form3, self).form_valid(form)

def faq(request): 
	return render(request, 'faq.html')

def glossary(request): 
	return render(request, 'glossary.html')

def bubble_plot(request): 
	return render(request, 'bubble_plot.html')

def data_search_info(request): 
	return render(request, 'data_search_info.html')

class AboutUs(TemplateView): 
	template_name = 'about_us.html'
