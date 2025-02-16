"""DRF Serializers for user annotations in the ``svs`` app."""

from rest_framework import serializers

from svs.models import StructuralVariantComment, StructuralVariantFlags


class StructuralVariantCommentSerializer(serializers.ModelSerializer):
    """Serializer for the ``StructuralVariantComment` model."""

    case = serializers.ReadOnlyField(source="case.sodar_uuid")
    user_can_edit = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    def create(self, validated_data):
        """Make case and user writeable on creation."""
        validated_data["user"] = self.context["request"].user
        keys = ("case", "release", "chromosome", "start", "end", "sv_type", "sv_sub_type")
        for key in keys:
            validated_data[key] = self.context[key]
        return super().create(validated_data)

    def get_user_can_edit(self, instance):
        return (
            self.context["request"].user.is_superuser
            or self.context["request"].user == instance.user
        )

    class Meta:
        model = StructuralVariantComment
        fields = (
            "sodar_uuid",
            "date_created",
            "date_modified",
            "user",
            "case",
            "bin",
            "release",
            "chromosome",
            # "chromosome_no",
            "start",
            "end",
            "sv_type",
            "sv_sub_type",
            "text",
            "user_can_edit",
        )
        read_only_fields = ("sodar_uuid", "date_created", "date_modified", "case", "user")


class StructuralVariantFlagsSerializer(serializers.ModelSerializer):
    """Serializer for the ``StructuralVariantFlags` model."""

    case = serializers.ReadOnlyField(source="case.sodar_uuid")

    def create(self, validated_data):
        """Make case writeable on creation."""
        validated_data["case"] = self.context["case"]
        keys = ("case", "release", "chromosome", "start", "end", "sv_type", "sv_sub_type")
        for key in keys:
            validated_data[key] = self.context[key]
        return super().create(validated_data)

    class Meta:
        model = StructuralVariantFlags
        fields = (
            "sodar_uuid",
            "date_created",
            "date_modified",
            "case",
            "release",
            "chromosome",
            # "chromosome_no",
            "start",
            "end",
            "sv_type",
            "sv_sub_type",
            "bin",
            "flag_bookmarked",
            "flag_candidate",
            "flag_final_causative",
            "flag_for_validation",
            "flag_no_disease_association",
            "flag_segregates",
            "flag_doesnt_segregate",
            "flag_visual",
            "flag_molecular",
            "flag_validation",
            "flag_phenotype_match",
            "flag_summary",
        )
        read_only_fields = ("sodar_uuid", "date_created", "date_modified", "case")
