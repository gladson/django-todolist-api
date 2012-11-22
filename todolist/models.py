from django.db import models


class List(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    list = models.ForeignKey(List, related_name='items')
    name = models.CharField(max_length=255, blank=False, null=False)
    done = models.BooleanField()

    def __unicode__(self):
        return self.name
