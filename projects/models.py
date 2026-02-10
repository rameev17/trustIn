from django.db import models
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))
    image = models.ImageField(upload_to='projects/', verbose_name=_("Изображение"))
    donated_money = models.IntegerField(verbose_name=_("Собранные деньги"))  # Changed to IntegerField
    goal_money = models.IntegerField(verbose_name=_("Целевая сумма"))  # Remains IntegerField
    ending_at = models.DateField(verbose_name=_("Дата завершения"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")
        ordering = ['-ending_at']