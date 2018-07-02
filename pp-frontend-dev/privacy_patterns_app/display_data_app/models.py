from django.db import models
from multiselectfield import MultiSelectField
from django import forms


DATA_USAGE = (
    ("Collection", "Collection"),
    ("Access" , "Access"), 
    ("Use" , "Use"),
    ("Disclosure" , "Disclosure"),
)
#tracks ftc case data and links to privacy principles
class Recommendation(models.Model): 
    text = models.TextField(default='', null=True, blank=True)
    principle_id = models.TextField(default='', null=True, blank=True)
    priority_number = models.IntegerField(default=0)
    note = models.TextField(default='')
    subprinciple = models.TextField(default='')
    ref = models.TextField(default='')
    url = models.TextField(default='')
    def __str__(self): 
        return self.ref + " (" + self.principle_id + ")" + ' - ' + self.subprinciple

class DataEntry(models.Model): 
    case_name = models.TextField(default='')
    case_url = models.TextField(default='')
    last_updated = models.TextField(default='')
    tags = models.TextField(default='')
    specific_violation = models.TextField(default='')
    company_type_key = models.TextField(default='')
    location = models.TextField(default='')

    #privacy 
    subprinciples = models.TextField(default='')  
    positive_recommendations = models.ManyToManyField(Recommendation, blank=True, symmetrical=False)
    data_usage = MultiSelectField(max_length=100,choices=DATA_USAGE, null=True, blank=True,help_text="<div style='float:right;font-size:12px;color:red'> HELP TEXT DISPLAYED HERE</div>")

class OPCDataEntry(models.Model):
    case_name = models.TextField(default='')
    case_url = models.TextField(default='')
    last_updated = models.TextField(default='')
    case_number = models.TextField(default='')
    last_updated = models.TextField(default='')
    sectors = models.TextField(default='')
    complaint_types = models.TextField(default='')
    topics = models.TextField(default='')
    dispositions = models.TextField(default='')
    principle = models.TextField(default='')
    positive_recommendations = models.ManyToManyField(Recommendation, blank=True, symmetrical=False)

#tracks user preferences   
class UserModel(models.Model): 
    #ftc 
    data_usage = models.TextField(default='')
    location = models.TextField(default='')
    industries = models.TextField(default='')

    #opc 
    topics = models.TextField(default='')
    complaint_types = models.TextField(default='')
    sectors = models.TextField(default='')
    dispositions = models.TextField(default='')


