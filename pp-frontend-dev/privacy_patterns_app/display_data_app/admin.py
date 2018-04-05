from django.contrib import admin
from .models import DataEntry, UserModel, Recommendation
from django.db import models


# CONTENT_HELP_TEXT = ' '.join(['<p>Here is some multi-line help',
# 							  'which is a long string so put',
# 							  'into a list which is then joined',
# 							  'with spaces. I can do fun things',
# 							  'like have <strong>bold</strong>',
# 							  'and some line breaks.<br/>'])

class RecommendationInline(admin.StackedInline):
    model = DataEntry.positive_recommendations.through  

class DataEntryAdmin(admin.ModelAdmin): 
	list_display = ['case_name', 'case_url', 'last_updated']
	search_fields = ['case_name', 'data_usage', 'location', 'subprinciples']
	# inlines = [RecommendationInline]
	# exclude = ['positive_recommendations', 'subprinciples']
	filter_horizontal = ('positive_recommendations',) 

	class Meta: 
		model = DataEntry 

class UserModelAdmin(admin.ModelAdmin): 
	list_display=['data_usage', 'location', 'industries']

class RecommendationModelAdmin(admin.ModelAdmin): 
	list_display=['id', 'principle_id', 'subprinciple']

# Register your models here.
admin.site.register(DataEntry, DataEntryAdmin)
admin.site.register(UserModel, UserModelAdmin)
admin.site.register(Recommendation, RecommendationModelAdmin)
