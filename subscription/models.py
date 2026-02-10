
from django.db import models
from django.utils.translation import gettext_lazy as _

class SubscriptionPlan(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    image = models.ImageField(upload_to='subscription_plans/', verbose_name=_("Изображение"))
    hover_image = models.ImageField(upload_to='subscription_plans/hover/', verbose_name=_("Изображение при наведении"), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    active_sub_count = models.IntegerField(default=0, verbose_name=_("Количество активных подписок"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("План подписки")
        verbose_name_plural = _("Планы подписки")