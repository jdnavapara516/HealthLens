from django.urls import path

from .views import delete_report, home, report_detail, reports_index

urlpatterns = [
    path('', home, name='root'),
    path('home/', home, name='home'),
    path('reports/', reports_index, name='reports_index'),
    path('reports/<int:report_id>/', report_detail, name='report_detail'),
    path('reports/<int:report_id>/delete/', delete_report, name='delete_report'),
]