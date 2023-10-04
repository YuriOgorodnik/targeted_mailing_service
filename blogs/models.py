from datetime import datetime

from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи')
    image = models.ImageField(upload_to='blogs/', verbose_name='изображение', null=True, blank=True)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    created_at = models.DateTimeField(verbose_name='дата публикации', default=datetime.now)
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')


    def __str__(self):
        return f'{self.title} {self.content}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
