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
    
class Statistics(models.Model):
    students_count = models.PositiveIntegerField(
        verbose_name="Количество студентов", default=0
    )
    donated_money = models.PositiveIntegerField(
        verbose_name="Сумма пожертвований (₸)", default=0
    )
    donors_count = models.PositiveIntegerField(
        verbose_name="Количество жертвователей", default=0
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return f"Студенты: {self.students_count}, Донатеры: {self.donors_count}, Пожертвования: {self.donated_money}₸"


class About(models.Model):
    LOCALE_CHOICES = [
        ('kz', 'Казахский'),
        ('ru', 'Русский'),
    ]
    
    locale = models.CharField(
        max_length=2,
        choices=LOCALE_CHOICES,
        default='kz',
        verbose_name="Язык",
        unique=True
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    mission_title = models.CharField(
        max_length=255,
        verbose_name="Заголовок миссии"
    )
    mission_text = models.TextField(
        verbose_name="Текст миссии"
    )
    goals_title = models.CharField(
        max_length=255,
        verbose_name="Заголовок целей"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"
        ordering = ['locale']

    def __str__(self):
        return f"{self.title} ({self.get_locale_display()})"


class AboutParagraph(models.Model):
    about = models.ForeignKey(
        About,
        related_name='paragraphs',
        on_delete=models.CASCADE,
        verbose_name="О нас"
    )
    text = models.TextField(
        verbose_name="Текст параграфа"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Параграф"
        verbose_name_plural = "Параграфы"
        ordering = ['order']

    def __str__(self):
        return f"Параграф {self.order} ({self.about.title})"


class AboutGoal(models.Model):
    about = models.ForeignKey(
        About,
        related_name='goals',
        on_delete=models.CASCADE,
        verbose_name="О нас"
    )
    text = models.TextField(
        verbose_name="Текст цели"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"
        ordering = ['order']

    def __str__(self):
        return f"Цель {self.order} ({self.about.title})"


class Team(models.Model):
    LOCALE_CHOICES = [
        ('kz', 'Казахский'),
        ('ru', 'Русский'),
    ]
    
    locale = models.CharField(
        max_length=2,
        choices=LOCALE_CHOICES,
        default='kz',
        verbose_name="Язык",
        unique=True
    )
    team_title = models.CharField(
        max_length=255,
        verbose_name="Заголовок команды"
    )
    founders_title = models.CharField(
        max_length=255,
        verbose_name="Заголовок основателей"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команда"
        ordering = ['locale']

    def __str__(self):
        return f"Команда ({self.get_locale_display()})"


class TeamMember(models.Model):
    LOCALE_CHOICES = [
        ('kz', 'Казахский'),
        ('ru', 'Русский'),
    ]
    
    locale = models.CharField(
        max_length=2,
        choices=LOCALE_CHOICES,
        default='kz',
        verbose_name="Язык"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )
    role = models.CharField(
        max_length=255,
        verbose_name="Должность/Роль"
    )
    year = models.CharField(
        max_length=100,
        verbose_name="Год выпуска",
        help_text="Например: Есік БИЛ '06"
    )
    contact = models.CharField(
        max_length=50,
        verbose_name="Контактная информация",
        help_text="Телефон"
    )
    image = models.ImageField(
        upload_to='team_images/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Члены команды"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role} ({self.get_locale_display()})"


class Founder(models.Model):
    LOCALE_CHOICES = [
        ('kz', 'Казахский'),
        ('ru', 'Русский'),
    ]
    
    locale = models.CharField(
        max_length=2,
        choices=LOCALE_CHOICES,
        default='kz',
        verbose_name="Язык"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Имя основателя"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Основатель"
        verbose_name_plural = "Основатели"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_locale_display()})"