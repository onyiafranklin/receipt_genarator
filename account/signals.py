import boto3

from django.db.models.signals import pre_delete
from django.conf import settings
from django.dispatch import receiver

from django.contrib.auth import get_user_model

Account = get_user_model()


@receiver(pre_delete, sender=Account)
def unsubscribe_sns(sender, instance, **kwargs):
    sns_client = boto3.client('sns', region_name=settings.AWS_REGION)
    sns_client.unsubscribe(SubscriptionArn=instance.subscription_arn)
