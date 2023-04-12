import boto3

from django.db.models.signals import pre_delete
from django.conf import settings
from django.dispatch import receiver

from django.contrib.auth import get_user_model

Account = get_user_model()


@receiver(pre_delete, sender=Account)
def unsubscribe_sns(sender, instance, **kwargs):
    sns_client = boto3.client('sns', region_name=settings.AWS_REGION)
    topic_arn = settings.SNS_TOPIC_ARN
    subscribe_arn = None

    # Set the email address to check for
    email = instance.email

    # List all subscriptions for the topic
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)

    # Filter the subscriptions by email address

    for sub in response['Subscriptions']:
        if sub['Protocol'] == 'email' and sub['Endpoint'] == email:
            subscribe_arn = sub['SubscriptionArn']

    # Check if there is a subscription for the email
    if subscribe_arn:
        sns_client.unsubscribe(SubscriptionArn=instance.subscribe_arn)
