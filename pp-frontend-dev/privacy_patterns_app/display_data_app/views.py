from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import models
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from display_data_app.forms import FilterForm
from display_data_app.models import DataEntry
import csv 
#from django.views import View

def index(request): 
	return render(request, 'index.html')

def populate_database(): 
	print("populating database")
	data = []
	filename = "display_data_app/data_clean.csv"
	#get case data from file 
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			case_name, case_url, last_updated, tags, jurisdiction = row['Case Name'], row['Case URL'], row['Last Updated'], row['Tags'], row['Jurisdiction']
			specific_violation, location, company_type, company_type_key = row['Specific Violation'], row['Location'], row['Company Type'], row['Company Type Key']
			data.append([case_name, case_url, last_updated, tags, jurisdiction, location, company_type, company_type_key, specific_violation])
	
	DataEntry.objects.all().delete() 
	#add data to model 
	for i, entry in enumerate(data): 
		new_entry = DataEntry(case_name = entry[0], case_url = entry[1], last_updated=entry[2], tags=entry[3], jurisdiction = entry[4], location=entry[5], company_type=entry[6], company_type_key=entry[7], specific_violation=entry[8])
		new_entry.id = i + 1 
		new_entry.save() 
	exit()

class DataVisView(TemplateView):
	template_name = "data_vis.html"

	def post(self, request, *args, **kwargs):
		value = request.POST['filter_options']
		context={'data': DataEntry.objects.filter(company_type_key = value), 'title': value}
		return super(TemplateView, self).render_to_response(context)

class CreateMyModelView(FormView):
	template_name = 'data_search_info.html'
	form_class = FilterForm
	fields = ['filter_options']
	#populate_database()  #should only be called once to populate django db 
	
class AboutUs(TemplateView): 
	template_name = 'about_us.html'

