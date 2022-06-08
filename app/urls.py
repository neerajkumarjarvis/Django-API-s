from django.urls import path , include
from .views import GetVoters,GetVotes,UpdateVotes,Home,send_files,modules
from . import views

urlpatterns = [
    path('', Home.as_view(), name='Home'),
    path('upload', send_files.as_view(), name="uploads"),
    path('modules/', views.modules, name='modules'),
    path('voters', GetVoters.as_view(),name='voters'),
    path('get_votes', GetVotes.as_view(),name='get_votes'),
    path('update_votes', UpdateVotes.as_view(), name='update_votes')
]