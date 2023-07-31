from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', views.check_list, name="check_list"),
    path('single/', views.single_check, name="single_check")
]