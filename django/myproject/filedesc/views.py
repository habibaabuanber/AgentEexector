from rest_framework import generics
from .models import FileDescription
from .serializers import FileDescriptionSerializer

class FileDescriptionListView(generics.ListAPIView):
    queryset = FileDescription.objects.all()
    serializer_class = FileDescriptionSerializer

class FileDescriptionDetailView(generics.RetrieveAPIView):
    queryset = FileDescription.objects.all()
    serializer_class = FileDescriptionSerializer
    lookup_field = 'file_name'
