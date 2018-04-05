from display_data_app.models import DataEntry, UserModel, Recommendation
import csv 

'''
Export data as a safeguard in case of accidental deletion
Note: Subprinciples are saved instead of positive recommendation objects
'''

class Exporter: 
	def __init__(self, export_filename='exported_data.csv'): 
		self.export_filename = export_filename
	
	def _write(self, data): 
		with open(self.export_filename, 'w') as csvfile: 
			writer = csv.writer(csvfile)
			fieldnames = ['Case Name', 'Case URL', 'Last Updated', 'Tags', 'Specific Violation', 'Company Type Key', 'Location', 'Subprinciples', 'Data Useage']
			writer.writerow(fieldnames)
			for entry in data: 
				writer.writerow(entry)

	def export(self): 
		data = []
		for d in DataEntry.objects.all(): 
			entry = [d.case_name, str(d.case_url), str(d.last_updated), str(d.tags), str(d.specific_violation), str(d.company_type_key), str(d.location), str(d.subprinciples), str(d.data_usage)]
			data.append(entry)
		self._write(data)
