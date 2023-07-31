from django.db import models


class CheckList(models.Model):
    proxy_list = models.TextField()


class CheckSingle(models.Model):
    ip_addr = models.CharField(max_length=16)
    port = models.IntegerField()
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)


class OutputFile(models.Model):
    output = models.FileField(default='proxy_geoip.csv')
    status = models.BooleanField(default=True)