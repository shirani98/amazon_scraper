from .views import AmazonProductDetailView
from django.urls import path


urlpatterns = [
    path("amazon/", AmazonProductDetailView.as_view()),
]
