from rest_framework import serializers
from .models import User
from education.models import LessonAnalysis, WorkPlan
from library.models import Book
from inventory.models import Item
from performance.models import KPIRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'avatar']
        read_only_fields = ['role']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.is_superuser:
            ret['role'] = 'admin'
        return ret


class MultilingualSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'uz')
            if '-' in lang:
                lang = lang.split('-')[0]
            if lang not in ['uz', 'ru', 'en']:
                lang = 'uz'

            for field in ['title', 'name', 'description']:
                field_lang = f"{field}_{lang}"
                if field_lang in ret:
                    ret[field] = ret[field_lang]
        return ret


class LessonAnalysisSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LessonAnalysis
        fields = '__all__'


class WorkPlanSerializer(MultilingualSerializer):
    class Meta:
        model = WorkPlan
        fields = '__all__'


class BookSerializer(MultilingualSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ItemSerializer(MultilingualSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class KPIRecordSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = KPIRecord
        fields = '__all__'
