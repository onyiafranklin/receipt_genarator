from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from .serializers import TrackSerializer, CreateTransactionSerializer
from .models import Track

class FetchTransactionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        year = serializer.validated_data["year"]
        month = serializer.validated_data["month"]

        query = Track.objects.filter(date__month=month, date__year=year, user=request.user)

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
