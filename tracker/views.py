from datetime import datetime

from django.shortcuts import get_list_or_404
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
