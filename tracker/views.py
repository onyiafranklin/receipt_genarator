import boto3
from botocore.exceptions import ClientError
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from .serializers import TrackSerializer, CreateTransactionSerializer
from .models import Track


class FetchTransactionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackSerializer

    def get_object(self):
        query = Track.objects.filter(user=self.request.user)

        if "month" in self.request.GET:
            month = self.request.GET["month"]
            if not month.isdigit():
                raise Http404("Invalid Month")

            month = int(month)
            if month < 1 or month > 12:
                raise Http404("Invalid Month")

            query = query.filter(date__month=month)

        if "year" in self.request.GET:
            year = self.request.GET["year"]
            if not year.isdigit():
                raise Http404("Invalid Year")

            year = int(year)
            curr_year = datetime.now().year
            if year < curr_year - 20 or year > curr_year:
                raise Http404("Invalid Year")

            query = query.filter(date__year=year)

        return query

    def get(self, request):

        query = self.get_object()

        serializer = self.get_serializer(many=True, instance=query)

        data = dict()

        for filter, category in Track.categories:
            data[category] = 0
            for amount in query.filter(category=filter).values_list("amount"):
                data[category] += amount[0]

        data["detail"] = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class AddTransactionView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CreateTransactionSerializer


class ListCategoriesView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = []
        for category, _ in Track.categories:
            categories += (category,)

        return Response(categories)


class GenerateReceiptView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(Track, id=id)
        return obj

    def get(self, request, *args, **kwargs):
        client = boto3.client('sns', region_name=settings.AWS_REGION)
        obj = self.get_object()
        try:

            # Specify the SNS topic ARN
            topic_arn = settings.SNS_TOPIC_ARN

            # Set the email address to check for
            email = request.user.email

            # List all subscriptions for the topic
            response = client.list_subscriptions_by_topic(TopicArn=topic_arn)

            # Filter the subscriptions by email address
            subscribe_arn = None

            for sub in response['Subscriptions']:
                if sub['Protocol'] == 'email' and sub['Endpoint'] == email:
                    subscribe_arn = sub['SubscriptionArn']

            # Check if there is a subscription for the email
            if subscribe_arn:
                response = client.publish(
                    Message=f'''
                        Requested Reciept For Finance Tracker

                    {request.user.username} Performed A Transaction of ${obj.amount}
                    Under the Category of {obj.category}

                    at {obj.date}
                    ''',
                    Subject="Recipet Report",
                    MessageStructure='string',
                    MessageAttributes={
                        'email': {
                            'DataType': 'String',
                            'StringValue': request.user.email,
                        }
                    },
                    TargetArn=subscribe_arn
                )
        except ClientError as e:
            error = e.response['Error']
            if error['Code'] == 'TargetNotSubscribed':
                # The TargetArn has not accepted the subscription
                error_message = 'The subscription confirmation has not been accepted. Please check your email for the confirmation link.'
                return Response({'success': False, 'error': error_message})
            else:
                # Other error occurred
                error_message = f'{error["Code"]}: {error["Message"]}'
                return Response({'success': False, 'error': error_message, "arn": subscribe_arn})

        return Response({"success": True, "message": "Reciept Has been Sent to your email"}, status=status.HTTP_200_OK)
