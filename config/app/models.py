from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class UserFile(models.Model):
    FILE_TYPES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('document', 'Документ'),
        ('other', 'Другое'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='files', verbose_name="Владелец"
    )
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name="Файл")
    title = models.CharField(max_length=200, blank=True, verbose_name="Название")
    file_type = models.CharField(
        max_length=20, choices=FILE_TYPES,
        default='other', verbose_name="Тип файла"
    )
    size = models.PositiveBigIntegerField(default=0, verbose_name="Размер, байт")
    is_public = models.BooleanField(default=False, verbose_name="Публичный")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружен")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or self.file.name

    def get_absolute_url(self):
        return reverse('file_detail', kwargs={'pk': self.pk})

    @property
    def is_image(self):
        return self.file_type == 'image'

    @property
    def is_video(self):
        return self.file_type == 'video'

    def save(self, *args, **kwargs):
        if self.file and not self.size:
            self.size = self.file.size
        if self.file and (not self.file_type or self.file_type == 'other'):
            name = self.file.name.lower()
            if name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                self.file_type = 'image'
            elif name.endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                self.file_type = 'video'
            elif name.endswith(('.pdf', '.doc', '.docx', '.txt', '.xlsx')):
                self.file_type = 'document'
        super().save(*args, **kwargs)

    def size_display(self):
        size = self.size
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} ТБ"