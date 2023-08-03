from django.db import models
from accounts.models import CustomUser
# Create your models here.

# class lodgingPhoto(models.Model):
#     image = models.ImageField(upload_to='photos/', null=True)
#     def __str__(self):
#         return f"Photo"
from django.db import models

class lodgingMain(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    price = models.IntegerField()
    phoneNumber = models.CharField(max_length=20)
    homePageURL = models.CharField(max_length=50)
    headCount = models.IntegerField()
    scrap = models.IntegerField(default=0)
    content = models.TextField()
    precaution = models.TextField()
    check_in_time = models.CharField(max_length=20)
    check_out_time = models.CharField(max_length=20)
    mainPhoto = models.ImageField(upload_to='photos/', blank=True, null=True)
    photos = models.ManyToManyField('lodgingPhoto')

    def __str__(self):
        return self.name

class lodgingPhoto(models.Model):
    # 사진과 관련된 필드를 여기에 추가하세요 (예: 이미지, 캡션 등)
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.caption or '사진'

class review(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1)
    image = models.ImageField(upload_to="review/", null=True)
    contents = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User 모델과 연결
    def __str__(self):
        return f"review"

class lodgingScrap(models.Model):
    scrap = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User 모델과 연결
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE) # lodgingMain 모델과 연결
    def __str__(self):
        return f"lodgingScrap"