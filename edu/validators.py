from rest_framework import serializers


class VideoValidator:
    def __call__(self, value: str):
        print(value.split('/'))
        if 'www.youtube.com' not in value.split('/'):
            raise serializers.ValidationError("Видео может быть только с YouTube")
