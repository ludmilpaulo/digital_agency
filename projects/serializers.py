from rest_framework import serializers
from .models import ProjectInquiry


from .models import (
    Project, ProjectStack, ProjectStat, ProjectCaseStudy, ProjectTrustedBy
)

class ProjectStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStack
        fields = ['tech']

class ProjectStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStat
        fields = ['label', 'value']

class ProjectTrustedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTrustedBy
        fields = ['logo']

class ProjectCaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCaseStudy
        fields = ['title', 'content']

class ProjectSerializer(serializers.ModelSerializer):
    stack = ProjectStackSerializer(many=True, read_only=True)
    stats = ProjectStatSerializer(many=True, read_only=True)
    trusted_by = ProjectTrustedBySerializer(many=True, read_only=True)
    case_study = ProjectCaseStudySerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'image', 'link', 'badge', 'badge_color',
            'stack', 'stats', 'case_study', 'trusted_by'
        ]


class ProjectInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInquiry
        fields = "__all__"