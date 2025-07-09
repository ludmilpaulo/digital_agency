from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ProjectGroup, User
from .serializers import GroupSerializer, ProjectGroupSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

class BuiltinGroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"], url_path="assign_users")
    def assign_users(self, request, pk=None):
        group = self.get_object()
        user_ids = request.data.get("user_ids", [])
        group.user_set.set(User.objects.filter(id__in=user_ids))
        group.save()
        return Response(GroupSerializer(group, context={'request': request}).data)

class ProjectGroupViewSet(viewsets.ModelViewSet):
    queryset = ProjectGroup.objects.prefetch_related('users').all()
    serializer_class = ProjectGroupSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"], url_path="assign_users")
    def assign_users(self, request, pk=None):
        group = self.get_object()
        user_ids = request.data.get("user_ids", [])
        group.users.set(User.objects.filter(id__in=user_ids))
        group.save()
        return Response(ProjectGroupSerializer(group, context={'request': request}).data)

# You can also have a combined endpoint if needed:
from rest_framework.views import APIView

class AllGroupsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        builtins = GroupSerializer(Group.objects.all(), many=True).data
        projects = ProjectGroupSerializer(ProjectGroup.objects.all(), many=True).data
        return Response({'builtin_groups': builtins, 'project_groups': projects})


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('groups', 'profile').all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProjectGroupViewSet(viewsets.ModelViewSet):
    queryset = ProjectGroup.objects.prefetch_related('users').all()
    serializer_class = ProjectGroupSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"], url_path="assign_users")
    def assign_users(self, request, pk=None):
        group = self.get_object()
        user_ids = request.data.get("user_ids", [])
        users = User.objects.filter(id__in=user_ids)
        group.users.set(users)
        group.save()
        return Response(ProjectGroupSerializer(group, context={'request': request}).data)
