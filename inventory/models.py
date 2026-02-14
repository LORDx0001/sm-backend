from django.db import models

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('furniture', 'Jihoz'),
        ('electronics', 'Elektronika'),
        ('stationery', 'Kanselyariya'),
        ('other', 'Boshqa'),
    ]

    name_uz = models.CharField(max_length=200, default='')
    name_ru = models.CharField(max_length=200, blank=True)
    name_en = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, default='dona')
    
    description = models.TextField(blank=True)
    
    location = models.CharField(max_length=100, blank=True) # e.g. "Room 204"
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_uz
