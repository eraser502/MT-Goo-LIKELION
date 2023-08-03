# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import lodgingMain
# from .serializers import lodgingCreateSerializer, lodgingSerializer


# class CreateLodgingView(APIView):
#     def post(self, request, format=None):
#         serializer = lodgingCreateSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ListAllLodgingView(APIView):
#     def get(self, request, format=None):
#         lodgings = lodgingMain.objects.all()
#         serializer = lodgingSerializer(lodgings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import lodgingMain, lodgingPhoto
from .serializers import lodgingCreateSerializer, lodgingMainSerializer, lodgingDetailSerializer

class CreateLodgingView(APIView):
    def post(self, request, format=None):
        serializer = lodgingCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class lodgingMainView(APIView):
    def get(self, request, format=None):
        lodgings = lodgingMain.objects.all()
        serializer = lodgingMainSerializer(lodgings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class lodgingDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            lodging = lodgingMain.objects.get(pk=pk)
            serializer = lodgingDetailSerializer(lodging)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except lodgingMain.DoesNotExist:
            return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)
