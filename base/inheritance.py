import sys
from django.db import models


class ProxySuper(models.Model):
    """Общий класс операций (расходов и доходов)"""

    class Meta:
        abstract = True

    proxy_name = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        """ automatically store the proxy class name in the database """
        self.proxy_name = type(self).__name__
        super().save(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        """ create an instance corresponding to the proxy_name """
        proxy_class = cls
        try:
            field_name = ProxySuper._meta.get_fields()[0].name
            proxy_name = kwargs.get(field_name)
            if proxy_name is None:
                proxy_name_field_index = cls._meta.fields.index(
                    cls._meta.get_field(field_name))
                proxy_name = args[proxy_name_field_index]
            proxy_class = getattr(sys.modules[cls.__module__], proxy_name)
        finally:
            return super().__new__(proxy_class)


class ProxyManager(models.Manager):
    def get_queryset(self):
        """ only include objects in queryset matching current proxy class """
        return super().get_queryset().filter(proxy_name=self.model.__name__)
