from django import forms

FILTER_CHOICES = (
	('Retail','Retail'), #(value, label)
	('Entertainment','Entertainment'), 
	('Food', 'Food'),
	('Mobile Application','Mobile Application'),
	('Sports','Sports'),
	('Hardware','Hardware'),
	('Other','Other'),
	('Health','Health'),
	('Social Platform','Social Platform'),
	('Real estate','Real estate'),
	('Automotive','Automotive'),
	('Consumer Reporting Agency','Consumer Reporting Agency'),
	('Telecommunications','Telecommunications'),
	('Financial Services','Financial Services'),
)

class FilterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(FilterForm, self).__init__(*args, **kwargs)
		self.fields['filter_options'] = forms.ChoiceField(choices=FILTER_CHOICES)
