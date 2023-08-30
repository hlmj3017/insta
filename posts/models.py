from django.db import models

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='image/%Y/%m') # db에 저장을 해주세요 근데 사진은 저장이 안 됨 / 글자와 숫자만 가능