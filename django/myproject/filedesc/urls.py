from django.urls import path
from .views import FileDescriptionListView, FileDescriptionDetailView

urlpatterns = [
    path('descriptions/', FileDescriptionListView.as_view(), name='description-list'),
    path('descriptions/<str:file_name>/', FileDescriptionDetailView.as_view(), name='description-detail'),
]
