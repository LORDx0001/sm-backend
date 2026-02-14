from django.db import models
from django.conf import settings

# Moved from api/models.py
class LessonAnalysis(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('flagged', 'Flagged'),
        ('inspected', 'Inspected'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]

    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    group = models.CharField(max_length=50, default='101-A')
    time = models.CharField(max_length=50, default='09:00') # e.g. "08:30 - 09:50"
    score = models.IntegerField() # 0-100
    
    summary = models.TextField(blank=True, null=True)
    suggestion = models.TextField(blank=True, null=True)
    
    # File Uploads for AI Analysis
    plan_file = models.FileField(upload_to='analysis/plans/', blank=True, null=True)
    video_file = models.FileField(upload_to='analysis/videos/', blank=True, null=True)
    result_file = models.FileField(upload_to='analysis/results/', blank=True, null=True)
    
    # Link to user who performed analysis (optional for now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    inspection_comment = models.TextField(blank=True, null=True)
    inspection_date = models.DateTimeField(blank=True, null=True)
    
    rector_approved = models.BooleanField(default=False)
    rector_comment = models.TextField(blank=True, null=True)
    rector_decision = models.CharField(max_length=50, blank=True, null=True) # e.g. 'warning', 'fine'
    
    hr_status = models.CharField(max_length=20, default='pending') # 'pending', 'confirmed'
    hr_comment = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.score}%"

class WorkPlan(models.Model):
    title_uz = models.CharField(max_length=200, default='')
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    
    description_uz = models.TextField(default='')
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    role = models.CharField(max_length=50) # e.g. 'prorektor', 'tyuter', 'bolim'
    
    file = models.FileField(upload_to='plans/', blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.title_uz}"
