from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('practice/', views.practice, name='practice'),
    path('practice/<int:pk>', views.practice_detail, name='practice_detail'),
    path('practice/update/<int:pk>', views.update_practice, name='update_practice'),
    path('stats/', views.stats, name='stats'),
]

