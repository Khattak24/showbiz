from rest_framework import serializers
from users.models import User, Profession
from utils.baseauthentication import encode_jwt_token


class UserSerializer(serializers.ModelSerializer):
    professions = serializers.ListField(required=False)

    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if int(instance.role) == 1:
            ret["professions"] = list(Profession.objects.filter(user=instance).values_list("profession_name", flat=True))
        ret["access_token"] = encode_jwt_token(instance)
        ret.pop("password")
        ret.pop("user_permissions")
        ret.pop("groups")
        ret.pop("is_staff")
        ret.pop("is_superuser")
        return ret

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            validated_data.pop("password")
        professions = None
        if validated_data.get("professions"):
            professions = validated_data.pop("professions")
        instance = super().update(instance, validated_data)
        instance.save()

        if professions:
            profession_list = list()
            for profession_name in professions:
                profession_list.append(Profession(
                    user=instance,
                    profession_name=profession_name
                ))
            Profession.objects.filter(user=instance).delete()
            Profession.objects.bulk_create(profession_list)
        return instance

class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["professions"] = list(Profession.objects.filter(user=instance).values_list("profession_name", flat=True))
        ret.pop("password")
        ret.pop("user_permissions")
        ret.pop("groups")
        ret.pop("is_staff")
        ret.pop("is_superuser")
        return ret
