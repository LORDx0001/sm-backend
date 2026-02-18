from django.db import models
from django.conf import settings


class LessonAnalysis(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending — AI analyzed, awaiting grading'),
        ('graded', 'Graded — O\'quv Bo\'limi graded (Internal)'),
        ('sent_to_inspection', 'Sent to Inspection - Awaiting approval'),
        ('returned_to_edu', 'Returned to Edu Dept - Inspection rejected'),
        ('sent_to_dekanat', 'Sent to Dekanat - Inspection approved (Punishment)'),
        ('dekanat_ready', 'Dekanat Ready — document prepared for Rektor'),
        ('ready_for_rector', 'Ready for Rector - Inspection approved (No Punishment)'),
        ('rector_signed', 'Rector Signed — executed'),
        ('archived', 'Archived — no action needed'),
    ]

    GRADE_CHOICES = [
        ('alo', "A'lo"),
        ('yaxshi', 'Yaxshi'),
        ('qoniqarli', 'Qoniqarli'),
        ('hayfsan', 'Hayfsan'),
        ('shtraf', 'Shtraf'),
        ('haydash', 'Haydash'),
    ]

    # Core fields from AI analysis
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    group = models.CharField(max_length=50, default='101-A')
    time = models.CharField(max_length=50, default='09:00')
    score = models.IntegerField()  # 0-100 from AI

    summary = models.TextField(blank=True, null=True)
    suggestion = models.TextField(blank=True, null=True)

    # File Uploads for AI Analysis
    plan_file = models.FileField(upload_to='analysis/plans/', blank=True, null=True)
    video_file = models.FileField(upload_to='analysis/videos/', blank=True, null=True)
    result_file = models.FileField(upload_to='analysis/results/', blank=True, null=True)

    # Link to user who performed analysis
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    # Workflow status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # --- O'quv Bo'limi (Educational Dept) grading ---
    grade = models.CharField(max_length=15, choices=GRADE_CHOICES, blank=True, null=True)
    edu_comment = models.TextField(blank=True, null=True)
    fine_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # For shtraf

    # --- Dekanat ---
    dekanat_document = models.TextField(blank=True, null=True)  # Official document text
    dekanat_comment = models.TextField(blank=True, null=True)

    # --- Rektor ---
    rector_signed = models.BooleanField(default=False)
    rector_comment = models.TextField(blank=True, null=True)
    rector_signed_at = models.DateTimeField(blank=True, null=True)

    # --- Inspection ---
    inspection_comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.score}% ({self.get_grade_display() or 'ungraded'})"

    @staticmethod
    def calculate_grade(score):
        """Calculate grade from score percentage."""
        if score >= 86:
            return 'alo'
        elif score >= 71:
            return 'yaxshi'
        elif score >= 56:
            return 'qoniqarli'
        elif score >= 41:
            return 'hayfsan'
        elif score >= 21:
            return 'shtraf'
        else:
            return 'haydash'

    @staticmethod
    def needs_action(grade):
        """Returns True if grade requires forwarding to Dekanat."""
        return grade in ('hayfsan', 'shtraf', 'haydash')


class WorkPlan(models.Model):
    title_uz = models.CharField(max_length=200, default='')
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)

    description_uz = models.TextField(default='')
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    role = models.CharField(max_length=50)  # e.g. 'prorektor', 'tyuter', 'bolim'

    file = models.FileField(upload_to='plans/', blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.title_uz}"
