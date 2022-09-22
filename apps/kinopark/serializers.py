from rest_framework import serializers
from apps.kinopark.models import *
from apps.kinopark.models import Movie_details


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'description',
            'producer',
            'rating',
            'published'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password"
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_details
        fields = '__all__'



