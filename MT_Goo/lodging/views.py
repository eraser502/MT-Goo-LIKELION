from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import lodgingMain, lodgingPhoto, review, priceByDate, lodgingScrap
from .serializers import lodgingCreateSerializer, lodgingMainSerializer, lodgingDetailSerializer, reviewCreateSerializer, reviewSerializer, priceByDateSerializer, lodgingScrapSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.models import CustomUser

class createLodgingView(APIView):
    # parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = lodgingCreateSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            lodging = serializer.save()
            if request.FILES.getlist('photos'):
                photos = request.FILES.getlist('photos')
                for photo in photos:
                    lodgingPhoto.objects.create(lodging=lodging, image=photo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class lodgingMainView(APIView):
    def get(self, request, format=None):
        lodgings = lodgingMain.objects.all()
        serializer = lodgingMainSerializer(lodgings, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class lodgingDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            lodging = lodgingMain.objects.get(pk=pk)
            serializer = lodgingDetailSerializer(lodging)
            # 숙소에 해당하는 리뷰들 가져오기
            reviews = review.objects.filter(lodging=lodging)
            review_serializer = reviewSerializer(reviews, many=True)

            # 숙소 정보와 리뷰 정보를 합쳐서 응답
            data = {
                "lodging": serializer.data,
                "reviews": review_serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except lodgingMain.DoesNotExist:
            return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)


class createReviewView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 리뷰를 작성할 수 있도록 설정합니다.

    def post(self, request, format=None):
        serializer = reviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 숙박 정보의 pk를 요청 데이터에서 가져옵니다.
            lodging_id = request.data.get('lodging_id')
            try:
                lodging = lodgingMain.objects.get(pk=lodging_id)
                # 사용자의 세션에서 인증 정보를 확인하고 user에 할당합니다.
                if request.user.is_authenticated:
                    # lodging 정보와 user 정보를 serializer에 전달해줍니다.
                    serializer.save(user=request.user, lodging=lodging)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Authentication failed."}, status=status.HTTP_401_UNAUTHORIZED)
            except lodgingMain.DoesNotExist:
                return Response({"error": "Lodging not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class lodgingScrapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id
        lodging_pk = data.get('lodging')
        # lodging과 user가 같은 객체가 존재한다면 업데이트(덮어 쓰기)
        scrap, created = lodgingScrap.objects.update_or_create(
            lodging=lodgingMain.objects.get(pk=lodging_pk),
            user=CustomUser.objects.get(pk = request.user.id),
            defaults={'isScrap': data.get('isScrap')}
        )
        
        serializer = lodgingScrapSerializer(scrap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
