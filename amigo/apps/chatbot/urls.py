from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api')
]