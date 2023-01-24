from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login, name='login'),
    path('studentHome/', views.studentHome, name='studentHome'),
    path('studentEdit/', views.studentEdit, name='studentEdit'),
    path('userHome/', views.userHome, name='userHome'),
    path('advisor/<int:id>', views.advisor, name='advisor'),
    path('supervisor/<int:id>', views.supervisor, name='supervisor'),
    path('karshenas/<int:id>', views.karshenas, name='karshenas'),
    path('head_of_department/<int:id>', views.head_of_department, name='head_of_department'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)