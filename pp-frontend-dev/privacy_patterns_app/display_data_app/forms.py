from django import forms
from .models import DataEntry

DATA_TYPES_1 = (
	("Collection", "Collection"),
	("Access" , "Access"), 
	("Use" , "Use"),
	("Disclosure" , "Disclosure"),
)

DATA_TYPES_2 = (
	("Retention" , "Retention"),
	("Archiving" , "Archiving"),
	("Backup" , "Backup"),
)

LOCATIONS_1 = (
	("Canada", "Canada"),
	("Oklahoma", "Oklahoma"), 
	("Wyoming", "Wyoming"), 
	("Minnesota", "Minnesota"), 
	("Illinois", "Illinois"), 
	("Washington", "Washington"), 
	("Indiana", "Indiana"), 
	("Maryland", "Maryland"), 
	("Texas", "Texas"), 
	("Iowa", "Iowa"), 
)

LOCATIONS_2 = (
	("Michigan", "Michigan"), 
	("Kansas", "Kansas"), 
	("Utah", "Utah"), 
	("Virginia", "Virginia"), 
	("Connecticut", "Connecticut"), 
	("Tennessee", "Tennessee"), 
	("California", "California"), 
	("Massachusetts", "Massachusetts"), 
	("Georgia", "Georgia"), 
	("Pennsylvania", "Pennsylvania"), 
)

LOCATIONS_3 = (
	("Florida", "Florida"), 
	("Rhode Island", "Rhode Island"), 
	("Kentucky", "Kentucky"), 
	("Missouri", "Missouri"), 
	("Ohio", "Ohio"), 
	("Alabama", "Alabama"), 
	("Colorado", "Colorado"), 
	("New Jersey", "New Jersey"), 
	("North Carolina", "North Carolina"), 
)

LOCATIONS_4 = {
	("New York", "New York"), 
	("Montana", "Montana"), 
	("Nevada", "Nevada"), 
	("Taiwan", "Taiwan"), 
	("Japan", "Japan"), 
	("Singapore", "Singapore"), 
	("United Kingdom", "United Kingdom"), 
}

INDUSTRIES_1 = (
	("Retail", "Retail"),
	("Entertainment", "Entertainment"), 
	("Food", "Food"), 
	("Marketing", "Marketing"), 
	("Mobile Applications", "Mobile Applications"), 
	("Sports", "Sports"), 
	("Hardware", "Hardware"), 
	("Education", "Education"), 
	("Health", "Health"), 
)

INDUSTRIES_2 = (
	("Social Platform", "Social Platform"), 
	("Real Estate", "Real Estate"), 
	("Automotive", "Automotive"), 
	("Hospitality", "Hospitality"), 
	("Consumer Reporting Agency", "Consumer Reporting Agency"), 
	("Software", "Software"), 
	("Telecommunications", "Telecommunications"), 
	("Financial Services", "Financial Services"), 
	("Other", "Other"), 
)
# OPC 
SECTORS_1 = (
	('Aboriginal Public Administration','Aboriginal Public Administration'), 
	('Accommodations', 'Accommodations'), 	
	('Computer Electronics Products', 'Computer Electronics Products'), 
	('Construction', 'Construction'), 
	('Consumer Goods Rental', 'Consumer Goods Rental'), 
	('Financial Institutions', 'Financial Institutions'), 
	('Health', 'Health'), 
	('Insurance', 'Insurance'), 
	('Marketing', 'Marketing'), 
	('Mobile Applications', 'Mobile Applications'),
)

SECTORS_2 = (
	('Nuclear', 'Nuclear'), 
	('Other','Other'), 
	('Professionals', 'Professionals'),  
	('Sales', 'Sales'), 
	('Security', 'Security'), 
	('Services', 'Services'), 
 	('Educational Support Services', 'Educational Support Services'), 
	('Social Networking', 'Social Networking'), 
	('Telecommunications', 'Telecommunications'), 
	('Transportation', 'Transportation'), 
)

COMPLAINT_TYPES_1 = (
	('Access', 'Access'), 
	('Accountability', 'Accountability'),  
	('Accuracy', 'Accuracy'), 
	('Appropriate Purposes', 'Appropriate Purposes'), 
	('Challenging Compliance', 'Challenging Compliance'), 
	('Collection', 'Collection'), 
	('Consent', 'Consent'), 
	('Correction', 'Correction'), 
)
COMPLAINT_TYPES_2 = (
	('Fee', 'Fee'),  
	('Identifying Purposes', 'Identifying Purposes'), 
	('Incident', 'Incident'), 
	('Openness', 'Openness'), 
	('Retention and Disposal', 'Retention and Disposal'), 
	('Safeguards', 'Safeguards'), 
	('Time Limit', 'Time Limit'), 
	('Use and Disclosure', 'Use and Disclosure'), 
)

TOPICS_1 = (
	('Access to personal information', 'Access to personal information'),  
	('Advertising and marketing', 'Advertising and marketing'),  
	('Biometrics', 'Biometrics'),  
	('Cloud computing', 'Cloud computing'), 
	('Consent', 'Consent'), 
	("Driver's licences", "Driver's licences"),  
	('Health/medical Information', 'Health/medical Information'),
	('Identity theft', 'Identity theft'),  
	('Internet and online', 'Internet and online'), 
	('Mobile devices and apps', 'Mobile devices and apps'), 
	('OPC Privacy Priorities', 'OPC Privacy Priorities'), 
)
TOPICS_2 = (
	('Personal information transferred across borders', 'Personal information transferred across borders'), 
	('Privacy and kids', 'Privacy and kids'), 
	('Privacy and society', 'Privacy and society'), 
	('Privacy at work', 'Privacy at work'), 
	('Privacy breaches', 'Privacy breaches'), 
	('Privacy policies', 'Privacy policies'), 
	('Public safety and law enforcement', 'Public safety and law enforcement'), 
	('Social Insurance Number (SIN)', 'Social Insurance Number (SIN)'), 
	('Social Networking', 'Social Networking'), 
	('Spam', 'Spam'),  
	('Surveillance and monitoring', 'Surveillance and monitoring'),
)

DISPOSITIONS_1 = (
	('Declined to investigate', 'Declined to investigate'),  
	('Discontinued', 'Discontinued'), 
	('Early resolved', 'Early resolved'), 
	('No jurisdiction', 'No jurisdiction'), 
	('Not well-founded', 'Not well-founded'), 
)
DISPOSITIONS_2 = (
	('Resolved', 'Resolved'),  
	('Settled', 'Settled'), 
	('Well-founded', 'Well-founded'), 
	('Well-founded and conditionally resolved', 'Well-founded and conditionally resolved'), 
	('Well-founded and resolved', 'Well-founded and resolved'), 
)

class DataTypeForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DATA_TYPES_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DATA_TYPES_2)

	def __init__(self, *args, **kwargs):
		super(DataTypeForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False

class LocationForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LOCATIONS_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LOCATIONS_2)
	field3 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LOCATIONS_3)
	field4 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LOCATIONS_4)

	def __init__(self, *args, **kwargs):
		super(LocationForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False

class IndustryForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=INDUSTRIES_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=INDUSTRIES_2)

	def __init__(self, *args, **kwargs):
		super(IndustryForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False

class SectorsForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SECTORS_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SECTORS_2)

	def __init__(self, *args, **kwargs):
		super(SectorsForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False

class ComplaintTypesForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=COMPLAINT_TYPES_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=COMPLAINT_TYPES_2)

	def __init__(self, *args, **kwargs):
		super(ComplaintTypesForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False


class DispositionsForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DISPOSITIONS_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DISPOSITIONS_2)

	def __init__(self, *args, **kwargs):
		super(DispositionsForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False


class ComplaintTypesForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=COMPLAINT_TYPES_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=COMPLAINT_TYPES_2)

	def __init__(self, *args, **kwargs):
		super(ComplaintTypesForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False


class TopicsForm(forms.Form):
	field1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TOPICS_1)
	field2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TOPICS_2)

	def __init__(self, *args, **kwargs):
		super(TopicsForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False





