from display_data_app.models import DataEntry, UserModel, Recommendation
import collections
import csv 
import json 
import ast 

'''
Class to import data from csv format to 
Django Database 
'''

class Importer: 
	def __init__(self, privacy_principles_csv = 'display_data_app/privacy_principles.csv', cases_csv = 'display_data_app/ftc_cases.csv'): 
		self.principle_id_to_counts = collections.Counter({'1.2.2': 43, '2.1.1': 21, '3.2.3': 20, '3.1.1': 20, '8.2.2': 18, '2.2.3': 18, '3.2.1': 16, '4.2.2': 16, '4.1.1': 14, '2.2.2': 14, '10.2.5': 13, '4.2.3': 13, '2.2.1': 13, '2.1.0': 13, '8.2.1': 12, '8.2.7': 11, '4.2.4': 10, '4.1.2': 10, '1.2.4': 9, '10.2.4': 9, '7.2.1': 9, '8.2.5': 9, '6.1.1': 8, '1.2.7': 8, '1.2.6': 8, '3.2.4': 8, '5.2.1': 7, '4.2.1': 7, '5.1.1': 6, '4.1.0': 6, '6.2.5': 5, '1.2.10': 5, '3.1.2': 5, '7.1.2': 5, '7.1.1': 5, '5.2.3': 5, '7.2.2': 5, '7.2.3': 4, '1.2.11': 4, '10.2.3': 4, '3.1.0': 4, '5.1.0': 4, '3.22.4': 3, '10.2.2': 3, '9.2.1': 3, '7.2.4': 3, '10.2.1': 3, '8.1.1': 3, '7.1.0': 2, '1.2.1': 2, '6.2.1': 2, '8': 2, '1.1.0': 2, '6.2.2': 2, '3.2.2': 2, '6.1.0': 2, '8.2.6': 2, '1.2.5': 2, '6.2.3': 2, '5.2.2': 1, '': 1, '7': 1, '8.2.3': 1, '3.2.3ñ 7.1..1': 1, '10.1.1': 1, '9.1.0': 1, '9.1.1': 1, '6.2.6': 1, '3.3.2': 1})
		self.filename1 = privacy_principles_csv
		self.filename2 = cases_csv 
		print(self.filename2)
	#populates recommendations database 
	#maps principle_id to recommendation object id 
	def _recommendations_list(self, filename): 
		principle_mapping = {} 
		with open(filename) as csvfile: 
			reader = csv.DictReader(csvfile)
			for i, row in enumerate(reader): 
				principle_id, pos_rec = row['GAPP #'], row['"Positive" Recommendation']
				subprinciple, note = row["GAPP Subprinciple"], row["GAPP Note"]
				ref = row['GAPP Ref']
				principle_mapping[principle_id] = i 
				priority_number = self.principle_id_to_counts[principle_id]
				rec = Recommendation(id=i, priority_number=priority_number, text = pos_rec, principle_id = principle_id, note=note, subprinciple=subprinciple, ref=ref)
				rec.save() 
		return principle_mapping 
	
	@staticmethod 
	def _process_data_types(principle_ids, data):
		data_types_raw = [data[i] for i in principle_ids if i in data] 
		data_types = set()
		for data_type in data_types_raw: 
			if "," in data_type: 
				data_type_list = data_type.split(',')
				for data_type_entry in data_type_list: 
					data_types.add(data_type)
			else: 
				data_types.add(data_type)
		return data_types

	#extract data from csvs and populate database 
	def populate_database(self, REPLACE=True): 
		if REPLACE: 
			Recommendation.objects.all().delete() 
		principle_mapping = self._recommendations_list(self.filename1)

		data = {}
		gap_principle_mapping = {}
		with open(self.filename1) as csvfile: 
			reader = csv.DictReader(csvfile)
			for i, row in enumerate(reader): 
				principle_id, data_type = row['GAPP #'], row['Actions with Data (from User Questionnaire)']
				data[principle_id] = data_type

		processed_data = []
		#count principles - only call for populating principles_id_to_counts
		# ctr = []
		#NEEDS PRINCIPLE IDS to be added to database 
		with open(self.filename2) as csvfile: 
			reader = csv.DictReader(csvfile)
			for i, row in enumerate(reader): 
				principle_ids_raw, case_name = row['Privacy Principle - Primary'], row['Case Name']
				case_url, company_type_key, location, last_updated = row['Case URL'], row['Company Type Key'], row['Location'], row['Last Updated']
				tags, specific_violation = row['Tags'], row['Specific Violation ']

				principle_ids = [x.strip() for x in principle_ids_raw.split(';')]
				if principle_ids == ['']: 
					continue 
				if 'N/A' in principle_ids[0]:
					continue 
				
				data_types = self._process_data_types(principle_ids, data)
				pos_recs = [principle_mapping[i] for i in principle_ids if i in principle_mapping] 
				subprinciples = [i for i in principle_ids]

				data_entry = [case_name, case_url, last_updated, location, company_type_key, list(data_types), tags, specific_violation, subprinciples, pos_recs]
				processed_data.append(data_entry)
		
		# ctr_dict = collections.Counter(ctr) #becomes principles_id_to_counts
		if REPLACE: 
			DataEntry.objects.all().delete() 

		#add data to data entry model 
		for i, entry in enumerate(processed_data):
			new_entry = DataEntry(case_name = entry[0], case_url = entry[1], last_updated=entry[2], location=entry[3], company_type_key=entry[4], data_usage=entry[5], tags=entry[6], specific_violation=entry[7], subprinciples = entry[8])
			new_entry.id = i + 1 
			new_entry.save() 
			pos_recs = [Recommendation.objects.get(id=i) for i in entry[9]]
			pos_recs1 = [(rec.id, int(rec.priority_number)) for rec in pos_recs]
			pos_recs2 = sorted(pos_recs1, key=lambda tup: tup[1], reverse=True) 

			for (rec_id, priority) in pos_recs2: 
				new_entry.positive_recommendations.add(Recommendation.objects.get(id=rec_id))
				new_entry.save() 

		print("=== Completed Data Transfer to Database ===")

