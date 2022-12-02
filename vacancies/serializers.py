from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from vacancies.models import Vacancy, Skill


class NotInStatusValidator:
    def __init__(self, statuses):
        if not isinstance(statuses, list):
            statuses = [statuses]
        self.statuses = statuses

    def __call__(self, value):
        if value in self.statuses:
            raise serializers.ValidationError("Incorrect status")


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = ["id", "text", "slug", "status", "created", "username", "skills"]


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )
    slug = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=Vacancy.objects.all())]
    )
    status = serializers.CharField(max_length=8, validators=[NotInStatusValidator(['closed', 'opened'])])

    class Meta:
        model = Vacancy
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._skills =  self.initial_data.pop("skills", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)
        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    creates = serializers.DateField(read_only=True)

    class Meta:
        model = Vacancy
        fields = ["id", "text", "status", "slug", "skills", "user", "created"]

    def is_valid(self, *, raise_exception=False):
        self._skills = self.initial_data.pop("skills", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)
        vacancy.save()
        return vacancy


class VacancyDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ["id"]
