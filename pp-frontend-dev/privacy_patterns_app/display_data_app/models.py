from django.db import models

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

class FilterModel(models.Model):
  	filter_options = models.CharField(max_length=100, choices=FILTER_CHOICES, default='Retail')
