from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
	path('', views.index,name='home'), 
	path('data-search',views.CreateMyModelView.as_view(success_url="data_vis"), name='data_search'),
	path('data-search/data',views.DataVisView.as_view(), name='data_vis'),
	path('about-us',views.AboutUs.as_view(), name='about_us'),

]
