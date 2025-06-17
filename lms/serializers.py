from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_video_url


class LessonSerializers(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    quantity_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializers(many=True, read_only=True)

    def get_quantity_lesson(self, course):
        return Lesson.objects.filter(course=course).count()


    def get_is_subscription(self, obj):
        """Проверяет наличие подписки."""
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()


    class Meta:
        model = Course
        fields = ('title', 'preview_img', 'description', 'quantity_lesson', 'lessons')
