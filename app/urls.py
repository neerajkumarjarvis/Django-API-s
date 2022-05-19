from django.urls import path , include
from .views import GetVoters,GetVotes,UpdateVotes

urlpatterns = [
    path('voters', GetVoters.as_view(),name='voters'),
    path('get_votes', GetVotes.as_view(),name='get_votes'),
    path('update_votes', UpdateVotes.as_view(), name='update_votes')
]