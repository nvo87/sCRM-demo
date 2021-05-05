from rest_framework import serializers

from accounts.helpers import get_director_group
from clubs.models import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'title', 'logo']

    def create(self, validated_data):
        club_instance = super().create(validated_data)
        user = self.context['request'].user
        club_instance.add_user_group(user, group=get_director_group())
        return club_instance
