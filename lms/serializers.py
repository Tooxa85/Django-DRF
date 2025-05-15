from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializers(serializers.ModelSerializer):

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

    class Meta:
        model = Course
        fields = ('title', 'preview_img', 'description', 'quantity_lesson', 'lessons')
