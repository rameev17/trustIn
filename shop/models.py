from django.db import models
from django.utils.translation import gettext_lazy as _

class Shop(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    image = models.ImageField(upload_to='shop_images/', verbose_name=_("Изображение"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активно"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Магазин")
        verbose_name_plural = _("Магазины")



class Order(models.Model):
    shop_item = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='orders', verbose_name=_("Продукт"))
    name = models.CharField(max_length=100, verbose_name=_("Имя"))
    phone_number = models.CharField(max_length=15, verbose_name=_("Номер телефона"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return f"Order by {self.name} for {self.shop_item.title}"

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")