from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Incident(models.Model):
    incident_date = models.DateField(
        verbose_name=_('Дата инцидента'),
    )
    incident_count = models.IntegerField(
        verbose_name=_('Количество'),
    )
    incident_details = models.TextField(
        verbose_name=_('Подробное описание'),
    )

    class Meta:
        verbose_name = _('Инцидент')
        verbose_name_plural = _('Инциденты')

    def __str__(self):
        return f'{self.incident_date}, количество {self.incident_count}'


class OilField(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Наименование'),
    )

    class Meta:
        verbose_name = _('Месторождение')
        verbose_name_plural = _('Месторождения')

    def __str__(self):
        return self.name


class Well(models.Model):
    class WellType(models.TextChoices):
        A = 0, _("Добывающая")
        B = 1, _("Нагнетательная")
        C = 2, _("Специальная")
        D = 3, _("Вспомогательная")

    class WellStatus(models.TextChoices):
        A = 0, _("Бурение")
        B = 1, _("Освоение")
        C = 2, _("Бездействие")
        D = 3, _("Простой")

    well_status = models.CharField(
        choices=WellStatus.choices,
        max_length=15,
        default=WellStatus.C,
        verbose_name=_("Статус скважины"),
    )

    well_type = models.CharField(
        choices=WellType.choices,
        max_length=15,
        default=WellType.A,
        verbose_name=_("Тип скважины")
    )

    ident_number = models.CharField(
        max_length=100,
        verbose_name=_("Идентификационный номер"),
    )

    oilfield = models.ForeignKey(
        OilField,
        on_delete=models.CASCADE,
        related_name='oilfield',
        verbose_name=_("Месторождение"),
    )
    asurg = models.BooleanField(
        default=False,
        verbose_name=_("Оснащение АСУРГ"),
    )

    class Meta:
        verbose_name = _('Скважина')
        verbose_name_plural = _('Скважины')

    def __str__(self):
        return self.ident_number


class Mining(models.Model):
    well = models.ForeignKey(
        Well,
        on_delete=models.CASCADE,
        verbose_name=_("Скважина"),
        related_name='mining',
    )
    mining_date = models.DateField(
        verbose_name=_('Дата'),
    )
    mining_count = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Количество'),
    )

    class Meta:
        verbose_name = _('Добыча')
        verbose_name_plural = _('Добыча')

    def __str__(self):
        return f'{self.mining_count}'


class Urgg(models.Model):
    well = models.ForeignKey(
        Well,
        on_delete=models.CASCADE,
        verbose_name=_("Скважина"),
        related_name='urgg',
    )
    urgg_date = models.DateField(
        verbose_name=_('Дата'),
    )
    urgg_count = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Количество'),
    )

    class Meta:
        verbose_name = _('Показатель УРГГ')
        verbose_name_plural = _('Показатели УРГГ')

    def __str__(self):
        return f'{self.urgg_date} - {self.urgg_count} м3'


class GasDisposal(models.Model):
    well = models.ForeignKey(
        Well,
        on_delete=models.CASCADE,
        verbose_name=_("Скважина"),
        related_name='gas_deposal',
    )
    gas_disposal_date = models.DateField(
        verbose_name=_("Дата"),
    )
    gas_disposal_count = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_("Количество"),
    )

    class Meta:
        verbose_name = _('Утилизация газа')
        verbose_name_plural = _('Утилизация газа')

    def __str__(self):
        return f'{self.gas_disposal_date} - {self.gas_disposal_count} м3'


class Employee(models.Model):
    id_employee = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name=_('Номер сотрудника'),
    )
    email = models.EmailField(
        _("Электронная почта"),
        max_length=40,
        unique=True,
    )
    first_name = models.CharField(
        _("Имя"),
        max_length=30,
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=30,
    )
    middle_name = models.CharField(
        _("Отчество"),
        max_length=30,
        blank=True,
    )
    phone_number = PhoneNumberField(
        _('Номер телефона'),
        unique=True,
    )

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')

    def get_full_name(self):
        return f'{self.first_name}{" " + self.middle_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()


class Task(models.Model):
    task_date = models.DateField(
        verbose_name=_('Дата задачи'),
    )
    id_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        to_field='id_employee',
        verbose_name=_('Сотрудник'),
        related_name='tasks',
    )
    task_details = models.CharField(
        max_length=255,
        verbose_name=_('Подробное описание'),
    )

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')

    def __str__(self):
        task_details_short = self.task_details[:10]
        return f'{self.task_date} - {task_details_short}'
