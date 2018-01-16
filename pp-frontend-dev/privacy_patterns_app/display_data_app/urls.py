from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('',views.CreateMyModelView.as_view(success_url=reverse_lazy('home')), name='home'),
    path('process/',views.process,name='process'),
]
