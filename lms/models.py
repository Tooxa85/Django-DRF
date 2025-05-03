from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=160,
        verbose_name="Название курса",
        help_text="Введите название курса.",
    )
    preview_img = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите изображение для превью курса.",
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса."
    )

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится данный урок.",
    )
    title = models.CharField(
        max_length=160,
        verbose_name="Название урока",
        help_text="Введите название урока.",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите описание урока."
    )
    preview_img = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите изображение для превью урока.",
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Введите URL-адрес видео для урока.",
    )

    def __str__(self):
        return f"{self.course} {self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
