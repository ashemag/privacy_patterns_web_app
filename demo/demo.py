import sys
import os 
import urllib2
import time 
from collections import defaultdict, Counter 
import csv 

def get_industry_categories(filename): 
	categories = set() 
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			category = row['Company Type Key']
			categories.add(category.strip())
	return categories

def get_output(key, filename): 
	data = []
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for i, row in enumerate(reader):
			category = row['Company Type Key']
			if category == key: 
				case_name, case_url, last_updated, tags, jurisdiction = row['Case Name'], row['Case URL'], row['Last Updated'], row['Tags'], row['Jurisdiction']
				violation, location, description = row['Specific Violation'], row['Location'], row['Company Type']
				data.append([case_name, case_url, last_updated, tags, jurisdiction, location, description, violation])
	return data

def write_to_csv(data, filename, fieldnames): 
	print "Creating results.csv..."
	with open(filename, 'wb') as csvfile: 
		writer = csv.writer(csvfile)
		writer.writerow(fieldnames)
		for entry in data: 
			writer.writerow(entry)

if __name__ == "__main__":
	industry_categories = get_industry_categories("data_clean.csv")
	industry_choices = [x for x in industry_categories]
	print "\n \n === Demo Tool === \n \n "
	print "This tool outputs FTC case data, sorted by industry category. It details the case name, case tags, company description, and specific privacy-related violations cited by the FTC."
	print "\n ===Industry Categories==="
	print ", ".join(industry_choices)
	print "\n"
	industry = ''
	while industry not in industry_categories and industry != "quit": 
		industry = raw_input('Choose industry category or enter "quit": ')
	if industry != "quit": 
		data = get_output(industry, "data_clean.csv")
		write_to_csv(data, 'demo_output/results.csv', ['Case Name', 'Case URL', 'Last Updated', 'Tags', 'Jurisdiction', 'Location', 'Description', 'Violation'])



