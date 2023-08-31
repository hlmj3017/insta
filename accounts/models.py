from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size = [500, 500],
        crop = ['middle', 'center'],
        upload_to='profile',
    )
    # post_set =   작성한 목록인지
    # like_posts =   좋아요를 누른  -> 충돌이 나므로 이름 수정


    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False) # self: 자기 자신 참조
    # followers = 