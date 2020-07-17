from django.urls import path
from .views import SignUpView, UpgradeView, create_customer_and_subscription

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('upgrade/', UpgradeView.as_view(), name='upgrade'),
    path('create_subscription/', create_customer_and_subscription, name='create_customer_and_subscription'),
]
