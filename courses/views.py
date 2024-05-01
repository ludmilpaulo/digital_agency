from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Module, Content, Subject
from .serializers import CourseSerializer, ModuleSerializer, SubjectSerializer


class OwnerAPIViewMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(owner=user)

class OwnerEditAPIViewMixin:
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

class CourseCreateView(OwnerEditAPIViewMixin, generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseUpdateView(OwnerEditAPIViewMixin, generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseListView(OwnerAPIViewMixin, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(OwnerAPIViewMixin, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer