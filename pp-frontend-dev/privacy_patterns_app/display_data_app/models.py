from django.db import models

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

    # Case Name,Case URL,Case Number,Last Updated,Tags,Jurisdiction,
    # Enforcement Authority,Case URL,
    # Specific Violation,Company Type,Company Type Key,Location