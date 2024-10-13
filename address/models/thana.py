from django.db import models

from address.models import District


class Thana(models.Model):
    '''Thana Model'''
    district = models.ForeignKey(
        District, on_delete=models.PROTECT, related_name='thana_objects'
    )
    name_english = models.CharField(max_length=120)
    name_bangla = models.CharField(max_length=120, blank=True, null=True)
    code = models.PositiveIntegerField(primary_key=True, blank=True)

    class Meta:
        ordering = ['name_english']


    def __str__(self):
        return self.name_english
