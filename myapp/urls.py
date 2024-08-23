from django.urls import path
from .views import DataView

urlpatterns = [
    path('api/data', DataView.as_view()),
    path('api/data/<int:data_id>', DataView.as_view()),
]
