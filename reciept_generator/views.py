from rest_framework.response import Response
from rest_framework import generics, status


class HealthCheckView(generics.GenericAPIView):

    def get(self, request):
        return Response({"Status": "Ok"}, status=status.HTTP_200_OK)
