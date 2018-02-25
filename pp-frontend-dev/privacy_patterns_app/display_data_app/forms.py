from django import forms

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
