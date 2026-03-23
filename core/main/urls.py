from django.urls import path
from .views import home, dashboard
from .api_views import project_list

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard),
    path('api/projects/', project_list),
]