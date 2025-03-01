from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
class Report(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Название"))
    file = models.FileField(upload_to='reports/%Y/%m/', verbose_name=_("PDF файл"))
    month = models.PositiveIntegerField(
        verbose_name=_("Месяц"),
        choices=[(i, _(f"{i}")) for i in range(1, 13)],
        null=True, blank=True
    )
    year = models.PositiveIntegerField(verbose_name=_("Год"), default=date.today().year)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата загрузки"))
    is_yearly = models.BooleanField(default=False, verbose_name=_("Годовой отчет"))
    
    class Meta:
        verbose_name = _("Отчет")
        verbose_name_plural = _("Отчеты")
        unique_together = ('month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        if self.is_yearly:
            return f"{self.title} (Годовой отчет {self.year})"
        return f"{self.title} ({self.month}/{self.year})"



class Calendar(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Название"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))
    image = models.ImageField(upload_to='calendar_images/', verbose_name=_("Изображение"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Календарь")
        verbose_name_plural = _("Календари")

class YearCalendar(models.Model):
    year = models.PositiveIntegerField(verbose_name=_("Год"))
    image = models.ImageField(upload_to='year_calendar_images/', verbose_name=_("Изображение"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    def __str__(self):
        return f"Календарь {self.year}"

    class Meta:
        verbose_name = _("Годовой календарь")
        verbose_name_plural = _("Годовые календари")
        unique_together = ('year',)

class Sponsor(models.Model):
    image = models.ImageField(upload_to='sponsors/', verbose_name=_("Изображение"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    def __str__(self):
        return f"Спонсор {self.id} ({'Активен' if self.is_active else 'Неактивен'})"

    class Meta:
        verbose_name = _("Спонсор")
        verbose_name_plural = _("Спонсоры")


class Vacancy(models.Model):
    company_info = models.TextField("О компании", blank=False)
    position = models.TextField("Позиция", blank=False)
    candidate_requirements = models.TextField("Требования к кандидату", blank=False)
    responsibilities = models.TextField("Обязанности", blank=False)
    conditions = models.TextField("Условия", blank=False)
    contact_info = models.TextField("Контактные данные", blank=False)
    is_active = models.BooleanField("Активная вакансия", default=False)


    def __str__(self):
        return f"{self.position} - {self.company_info[:30]}..."


from django.db import models

class News(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    image = models.ImageField(
        upload_to='news_images/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title