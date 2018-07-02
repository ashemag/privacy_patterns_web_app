from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
	path('', views.index,name='home'), 

	path('data-search',views.data_search_info, name='data_search'),
	path('data-search/jurisdiction',views.choose_jurisdiction, name='jurisdiction'),
	
	# ftc paths 
	path('data-search/ftc-form1',views.form1.as_view(), name='ftc-form1'),
	path('data-search/ftc-form2',views.form2.as_view(), name='ftc-form2'),
	path('data-search/ftc-form3',views.form3.as_view(), name='ftc-form3'),
	path('data-search/ftc-data',views.DataVisView.as_view(), name='ftc-data'),

	# opc paths 
	path('data-search/opc-form1',views.opc_form1.as_view(), name='opc-form1'),
	path('data-search/opc-form2',views.opc_form2.as_view(), name='opc-form2'),
	path('data-search/opc-form3',views.opc_form3.as_view(), name='opc-form3'),
	path('data-search/opc-form4',views.opc_form4.as_view(), name='opc-form4'),
	path('data-search/opc-data',views.OPCDataVisView.as_view(), name='opc-data'),

	# other pages 
	path('about-us',views.AboutUs.as_view(), name='about_us'),
	path('faq',views.faq, name='faq'),
	path('glossary',views.glossary, name='glossary'),
	
]
