from django.contrib.auth.models import Group
from rest_framework import serializers

from authentication.api.serializers import GroupSerializer
from ..models import File


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    def get_owner(self, entry):
        return entry.user.username

    class Meta(object):
        model = File
        fields = [
            'id',
            'owner',
            'name',
            'content',
            'groups'
        ]


class FileDownloadSerializer(serializers.Serializer):
    content = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    salt = serializers.CharField(write_only=True, max_length=16, min_length=16)
    file = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=File.objects
    )


class FileGroupsSerializer(serializers.Serializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects, write_only=True, many=True
    )

    def update(self, instance, validated_data):
        groups = validated_data.get('groups')

        instance.groups.set(groups)
        instance.save()

        return instance
