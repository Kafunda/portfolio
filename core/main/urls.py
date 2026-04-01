from django.urls import path
from .views import home
from .api_views import project_list

urlpatterns = [
    path('', home, name='home'),
    path('api/projects/', project_list),
]