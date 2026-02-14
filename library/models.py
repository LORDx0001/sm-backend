from django.db import models

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('textbook', 'Darslik'),
        ('manual', "O'quv qo'llanma"),
        ('fiction', 'Badiiy'),
        ('journal', 'Jurnal'),
        ('other', 'Boshqa'),
    ]

    title_uz = models.CharField(max_length=200, default='')
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='textbook')
    
    isbn = models.CharField(max_length=20, blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)
    
    file = models.FileField(upload_to='books/', blank=True, null=True)
    cover_image = models.CharField(max_length=500, blank=True, null=True) # URL to image or path
    
    description = models.TextField(blank=True)
    
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_uz
