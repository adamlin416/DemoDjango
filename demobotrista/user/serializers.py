# serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    groups = serializers.StringRelatedField(many=True, required=False, read_only=True)
    is_manager = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "age",
            "phone",
            "groups",
            "password",
            "is_manager",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        is_manager = validated_data.pop("is_manager", False)
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email"),
            age=validated_data.get("age"),
            phone=validated_data.get("phone"),
            is_staff=is_manager,
        )

        # Assign user to either 'Manager' or 'Customer' group
        group_name = "Manager" if is_manager else "Customer"
        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(user)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating User model.
    """

    groups = serializers.StringRelatedField(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "age",
            "phone",
            "groups",
            "password",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "password": {"required": False, "write_only": True},
        }

    def update(self, instance, validated_data):
        if not validated_data:
            raise serializers.ValidationError(
                {"detail": "No data provided to update user."}
            )
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.age = validated_data.get("age", instance.age)
        instance.phone = validated_data.get("phone", instance.phone)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance
