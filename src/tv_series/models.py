from django.db import models

class TVSeries(models.Model):
    name = models.TextField(default='')
    release_year = models.IntegerField()
    tvdb_id = models.IntegerField()
