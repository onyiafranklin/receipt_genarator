
from django.conf import settings

import boto3
from botocore.exceptions import ClientError


from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password"
        ]

    def validate(self, attrs):
        if User.objects.filter(subscribe_arn=attrs["subscribe_arn"]).exists():
            raise serializers.ValidationError(
                "This Email Cannot be Added Contact Admin")

        return attrs

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        self.fields["id"].read_only = True
        self.fields["password"].write_only = True

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = self.Meta.model(**validated_data)
        client = boto3.client('sns', region_name=settings.AWS_REGION)
        try:
            response = client.subscribe(
                TopicArn=settings.SNS_TOPIC_ARN, Protocol='email', Endpoint=user.email)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameter':
                raise serializers.ValidationError(
                    {'email': 'Invalid email address'})
            elif e.response['Error']['Code'] == 'EndpointDisabled':
                raise serializers.ValidationError(
                    {'email': 'Email address is disabled'})
            elif e.response['Error']['Code'] == 'AuthorizationError':
                raise serializers.ValidationError(f'Authorization error: {e}')
            else:
                raise serializers.ValidationError(f'Unexpected error: {e}')

        user.subscribe_arn = response['SubscriptionArn']
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)

        if "email" in validated_data:
            # Code to Unsubscribe old email and subscribe new one
            ...

        instance.save()

        return instance


class LoginSerilizer(serializers.Serializer):

    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)

    def validate(self, attrs):

        user = authenticate(
            username=attrs["username"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("invalid Credentials")

        attrs["user"] = user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, max_length=100)
    new_password = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("Wrong Password")

        if attrs["new_password"] == attrs["old_password"]:
            raise serializers.ValidationError(
                "Old and New Password cannot be the same")

        return attrs
