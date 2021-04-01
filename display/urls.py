from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:twitterusers_id>/', views.detail, name='detail'),
    path('user/new/', views.user_new, name='user_new'),
    path('<int:twitterusers_id>/delete', views.delete, name='delete'),
]