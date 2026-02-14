from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, LessonAnalysisViewSet, DashboardStatsView,
    WorkPlanViewSet, BookViewSet, ItemViewSet, KPIRecordViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'analysis', LessonAnalysisViewSet)
router.register(r'work-plans', WorkPlanViewSet)
router.register(r'books', BookViewSet)
router.register(r'items', ItemViewSet)
router.register(r'kpi', KPIRecordViewSet)
router.register(r'dashboard/stats', DashboardStatsView, basename='dashboard-stats')

urlpatterns = [
    path('', include(router.urls)),
]
