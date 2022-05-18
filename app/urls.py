from django.urls import path , include
from .views import GetVoters

urlpatterns = [
    path('voters', GetVoters.as_view(),name='voters')
]