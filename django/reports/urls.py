from django.urls import path

from .views import home, report_detail

urlpatterns = [
    path('', home, name='root'),
    path('home/', home, name='home'),
    path('reports/<int:report_id>/', report_detail, name='report_detail'),
]