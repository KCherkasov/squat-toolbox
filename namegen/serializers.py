# -*- coding: utf-8 -*-

from rest_framework import serializers


class NamegenApiRequestData:
    def __init__(self, lang, gender, nobility, count):
        self.lang = lang,
        self.gender = gender
        self.nobility = nobility
        self.count = count


class NARDSerializer(serializers.Serializer):
    lang = serializers.CharField(max_length=4)
    gender = serializers.CharField(max_length=1)
    nobility = serializers.CharField(max_length=1)
    count = serializers.IntegerField(default=1, max_value=50, min_value=1)

    def create(self, validated_data):
        return NamegenApiRequestData(**validated_data)

    def update(self, instance, validated_data):
        instance.lang = validated_data.get('lang', instance.lang)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.nobility = validated_data.get('nobility', instance.nobility)
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        return instance


class SplitName:
    def __init__(self, name, middle_name, surname, gender_tail, noble_tail):
        self.name = name
        self.middle_name = middle_name
        self.surname = surname
        self.gender_tail = gender_tail
        self.noble_tail = noble_tail


class NameSerializerSplit(serializers.Serializer):
    id = serializers.IntegerField(default=1)
    name = serializers.CharField(max_length=30)
    middle_name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=30)
    gender_tail = serializers.CharField(max_length=30)
    noble_tail = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return SplitName(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.gender_tail = validated_data.get('gender_tail', instance.gender_tail)
        instance.noble_tail = validated_data.get('noble_tail', instance.noble_tail)
        instance.save()
        return instance


class SimpleName:
    def __init__(self, name):
        self.name = name


class NameSerializerSimple(serializers.Serializer):
    id = serializers.IntegerField(default=1)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return SimpleName(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
