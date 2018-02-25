from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
	path('', views.index,name='home'), 
	path('data-search',views.data_search_info, name='data_search'),
	path('data-search/data',views.DataVisView.as_view(), name='data_vis'),
	path('about-us',views.AboutUs.as_view(), name='about_us'),

	path('data-search/form1',views.form1.as_view(), name='form1'),
	path('data-search/form2',views.form2.as_view(), name='form2'),
	path('data-search/form3',views.form3.as_view(), name='form3'),

	path('data-search/data-vis',views.DataVisView.as_view(), name='data_vis'),

	path('findings', views.bubble_plot, name='findings'),

	path('faq',views.faq, name='faq'),
	path('glossary',views.glossary, name='glossary'),

]
