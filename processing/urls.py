from django.urls import path
from .views import UploadView, StatusView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('status/<str:request_id>/', StatusView.as_view(), name='status'),
]
