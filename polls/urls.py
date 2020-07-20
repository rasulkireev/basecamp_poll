from django.urls import path
from .views import CreatePollView

app_name = 'polls'
urlpatterns = [
    path('new/', CreatePollView.as_view(), name='create-poll'),
]
