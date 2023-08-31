from django.db import models
from django_resized import ResizedImageField

from django.conf import settings
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='image/%Y/%m') # db에 저장을 해주세요 근데 사진은 저장이 안 됨 / 글자와 숫자만 가능
    image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='image/%Y/%m'

    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # AUTH_USER_MODEL: 상수임을 의미하는 코드/ 변하지 않는 데이터를 의미


class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

