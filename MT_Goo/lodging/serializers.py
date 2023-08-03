from rest_framework import serializers
from .models import lodgingMain, lodgingPhoto

# # class lodgingPhotoSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = lodgingPhoto
# #         fields = '__all__'
# class lodgingSerializer(serializers.ModelSerializer):
#     # photos = lodgingPhotoSerializer(many=True)

#     class Meta:
#         model = lodgingMain
#         fields = ['pk', 'name', 'address', 'place', 'price', 'phoneNumber', 'homePageURL', 'headCount', 'scrap', 'content', 'precaution', 'check_in_time', 'check_out_time']
class lodgingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = lodgingPhoto
        fields = '__all__'



class lodgingMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = lodgingMain
        fields = ['pk', 'name', 'place', 'price', 'headCount', 'mainPhoto']

class lodgingDetailSerializer(serializers.ModelSerializer):
    photos = lodgingPhotoSerializer(many=True)

    class Meta:
        model = lodgingMain
        fields = ['pk', 'name', 'address', 'place', 'price', 'phoneNumber', 'homePageURL', 'headCount', 'scrap', 'content', 'precaution', 'check_in_time', 'check_out_time', 'mainPhoto', 'photos']

class lodgingCreateSerializer(serializers.ModelSerializer):
    photos = lodgingPhotoSerializer(many=True, required=False)  # 필드를 선택적으로 입력 받도록 설정

    class Meta:
        model = lodgingMain
        fields = ('name', 'address', 'place', 'price', 'phoneNumber', 'homePageURL', 'headCount', 'scrap', 'content', 'precaution', 'check_in_time', 'check_out_time', 'mainPhoto','photos')

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        lodging = lodgingMain.objects.create(**validated_data)

        for photo_data in photos_data:
            lodgingPhoto.objects.create(lodging=lodging, **photo_data)

        return lodging
