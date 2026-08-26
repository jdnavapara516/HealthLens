from django.urls import path

from .views import home, login_view, logout_view, signup_view

urlpatterns = [
    path('', home, name='root'),
    path('home/', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]