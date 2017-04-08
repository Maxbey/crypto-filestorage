from rest_framework import serializers
from ..models import File


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, entry):
        return entry.user.username

    class Meta(object):
        model = File
        fields = [
            'id',
            'owner',
            'name',
            'content'
        ]


class FileDownloadSerializer(serializers.Serializer):
    content = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    salt = serializers.CharField(write_only=True, max_length=16, min_length=16)
    file = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=File.objects
    )

