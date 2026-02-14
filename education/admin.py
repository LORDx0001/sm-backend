from django.contrib import admin
from .models import LessonAnalysis, WorkPlan

@admin.register(LessonAnalysis)
class LessonAnalysisAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'group', 'score', 'time', 'status', 'created_at')
    list_filter = ('status', 'subject', 'group', 'teacher')
    search_fields = ('subject', 'teacher', 'group')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(WorkPlan)
class WorkPlanAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'role', 'deadline', 'is_completed', 'created_at')
    list_filter = ('role', 'is_completed', 'deadline')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'description_uz', 'role')
    list_editable = ('is_completed',)
