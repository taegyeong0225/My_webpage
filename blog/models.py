from django.db import models

# class PostManager(models.Manager):
    # pass

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # 새로운 PostManager를 매니저로 사용하도록 지정

    def __str__(self):
        return f'[{self.pk}] {self.title}'
