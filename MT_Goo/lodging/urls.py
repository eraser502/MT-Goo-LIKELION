from django.urls import path
from .views import lodgingMainView, CreateLodgingView, lodgingDetailView

urlpatterns = [
    path('main/', lodgingMainView.as_view(), name='lodgingMain'),
    path('create/', CreateLodgingView.as_view(), name='create-lodging'),
    path('detail/<int:pk>/', lodgingDetailView.as_view(), name='lodgingDetail'),
]
