from django.db import models

#tracks ftc case data and links to privacy principles
class DataEntry(models.Model): 
    case_name = models.TextField(default='')
    case_url = models.TextField(default='')
    last_updated = models.TextField(default='')
    tags = models.TextField(default='')
    jurisdiction = models.TextField(default='')
    specific_violation = models.TextField(default='')
    company_type = models.TextField(default='')
    company_type_key = models.TextField(default='')
    location = models.TextField(default='')

    #privacy 
    subprinciple = models.TextField(default='')
    note = models.TextField(default='')
    pos_rec = models.TextField(default='')
    data_type = models.TextField(default='')
  
#tracks user preferences   
class UserModel(models.Model): 
    data_type = models.TextField(default='')
    location = models.TextField(default='')
    industries = models.TextField(default='')