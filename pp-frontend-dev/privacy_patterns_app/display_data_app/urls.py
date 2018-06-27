from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
	path('', views.index,name='home'), 
	path('about-us',views.AboutUs.as_view(), name='about_us'),
	
	path('data-search',views.data_search_info, name='data_search'),
	
	path('data-search/jurisdiction',views.choose_jurisdiction, name='jurisdiction'),
	path('data-search/ftc-form1',views.form1.as_view(), name='ftc-form1'),
	path('data-search/ftc-form2',views.form2.as_view(), name='ftc-form2'),
	path('data-search/ftc-form3',views.form3.as_view(), name='ftc-form3'),
	path('data-search/ftc-data',views.DataVisView.as_view(), name='ftc-data'),

	# path('data-search/data-vis',views.DataVisView.as_view(), name='data_vis'),

	path('faq',views.faq, name='faq'),
	path('glossary',views.glossary, name='glossary'),
]
