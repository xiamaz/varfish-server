from projectroles.app_settings import AppSettingAPI
from projectroles.serializers import (
    ProjectSerializer,
    SODARProjectModelSerializer,
    SODARUserSerializer,
)
from rest_framework import serializers

from cases.serializers import CaseSerializer
from cohorts.models import Cohort, CohortCase
from variants.models import Case

_app_settings = AppSettingAPI()


class CohortSerializer(SODARProjectModelSerializer):
    """Serializer for the ``Cohort`` model."""

    #: Serialize ``user``.
    user = SODARUserSerializer(read_only=True)
    #: Add serialized ``inaccessible_cases``.
    inaccessible_cases = serializers.SerializerMethodField()
    #: Serialize filtered ``cases`` ForeignKey field.
    cases = serializers.SerializerMethodField()

    class Meta:
        model = Cohort
        exclude = ("id",)
        read_only_fields = (
            "sodar_uuid",
            "project",
            "date_created",
            "date_modified",
            "user",
            "cases",
        )

    def create(self, validated_data):
        """Override create() to add user to validated data"""
        if "user" not in validated_data and hasattr(self.context["request"], "user"):
            validated_data["user"] = self.context["request"].user

        return super().create(validated_data)

    def get_inaccessible_cases(self, obj):
        """Corresponds to the ``inaccessible_cases`` field defined above."""
        if self.context["request"].user.is_superuser:
            return 0

        return obj.cases.exclude(project__roles__user=self.context["request"].user).count()

    def get_cases(self, obj):
        """Corresponds to the ``cases`` field defined above."""
        if self.context["request"].user.is_superuser:
            return CaseSerializer(obj.cases, many=True).data

        return CaseSerializer(
            obj.cases.filter(project__roles__user=self.context["request"].user), many=True
        ).data


class CohortCaseSerializer(serializers.ModelSerializer):
    """Serializer for the ``CohortCase`` model."""

    #: Serialize the case into its ``sodar_uuid``.
    case = serializers.SlugRelatedField(slug_field="sodar_uuid", queryset=Case.objects.all())
    #: Serialize the cohort into its ``sodar_uuid``.
    cohort = serializers.SlugRelatedField(slug_field="sodar_uuid", queryset=Cohort.objects.all())

    class Meta:
        model = CohortCase
        exclude = ("id",)
        read_only_fields = ("sodar_uuid",)


class ProjectCasesSerializer(ProjectSerializer):
    """Serializer for the ``Project`` model and its cases."""

    #: Serialize the cases that reference the project
    case_set = serializers.SerializerMethodField()

    class Meta:
        model = ProjectSerializer.Meta.model
        fields = ProjectSerializer.Meta.fields + ["case_set"]

    def get_case_set(self, obj):
        """Corresponds to the ``case_set`` field defined above.

        The purpose is to filter the cases by active smallvariantset and serialize them as
        the default serializer would just fetch all cases which is not what we want.
        """
        return CaseSerializer(obj.case_set.filter(smallvariantset__state="active"), many=True).data
