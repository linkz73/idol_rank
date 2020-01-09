from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Idol(models.Model):
    idol_id = models.AutoField(primary_key=True)
    idol_name = models.CharField('IDOL NAME', null=False, max_length=100, unique=True)
    idol_img = models.CharField('IDOL Image', max_length=200, blank=True)
    class Meta:
        verbose_name = 'idol'  # 이 이름을 이용해서 표시 가능
        verbose_name_plural = 'idol'
        db_table = 'idol'
        ordering = ('idol_name',)

    def __str__(self):
        return self.idol_name


class Chart(models.Model):
    chart_id = models.AutoField(primary_key=True)
    idol = models.ForeignKey(Idol, null=True, on_delete=models.CASCADE,)
    chart_music = models.IntegerField(default=0)
    chart_media = models.IntegerField(default=0)
    chart_portal = models.IntegerField(default=0)
    chart_total = models.IntegerField(null=False, default=0)
    chart_date = models.IntegerField(null=False, default=0)
    class Meta:
        verbose_name = 'chart'  # 이 이름을 이용해서 표시 가능
        verbose_name_plural = 'chart'
        db_table = 'chart'
        ordering = ('-chart_id',)

    def __str__(self):
        return self.chart_id

    # def get_absolute_url(self):
    #     return reverse('chart:post_detail', args=(self.slug,))
    #     # return reverse('blog:post_detail', kwargs={'slug': self.slug})
