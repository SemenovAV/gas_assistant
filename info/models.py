from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class OilField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Наименование'))
    asurg = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                verbose_name=_('Оснащение АСУРГами'))
    gas_disposal = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                       verbose_name=_('Утилизация газа'))

    class Meta:
        verbose_name = _('Месторождение')
        verbose_name_plural = _('Месторождения')

    def __str__(self):
        return self.name


class Incident(models.Model):
    incident_date = models.DateField(verbose_name=_('Дата инцидента'))
    incident_count = models.IntegerField(verbose_name=_('Количество'))
    incident_details = models.TextField(verbose_name=_('Подробное описание'))

    class Meta:
        verbose_name = _('Инцидент')
        verbose_name_plural = _('Инциденты')

    def __str__(self):
        return f'{self.incident_date}, количество {self.incident_count}'


class Mining(models.Model):
    name_oilfield = models.ForeignKey(OilField, on_delete=models.CASCADE, verbose_name=_('Месторождение'),
                                      related_name='mining')
    mining_date = models.DateField(verbose_name=_('Дата'))
    mining_value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_('Количество добычи'))

    class Meta:
        verbose_name = _('Добыча')
        verbose_name_plural = _('Добыча')

    def __str__(self):
        return f'{self.name_oilfield.name} - {self.mining_date}'


class Urgg(models.Model):
    urgg_date = models.DateField()
    urgg_count = models.IntegerField()

    class Meta:
        verbose_name = _('Показатель УРГГ')
        verbose_name_plural = _('Показатели УРГГ')

    def __str__(self):
        return f'{self.urgg_date} - {self.urgg_count} м3'


class CountWells(models.Model):
    wells_status = models.CharField(max_length=255, verbose_name=_('Статус'))
    wells_count = models.IntegerField(verbose_name=_('Количество'))

    class Meta:
        verbose_name = _('Количество скважин')
        verbose_name_plural = _('Количество скважин')

    def __str__(self):
        return f'{self.wells_status} - {self.wells_count} скважин'


class Employee(models.Model):
    id_employee = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Номер сотрудника'))
    email = models.EmailField(_("Электронная почта"), max_length=40, unique=True)
    first_name = models.CharField(_("Имя"), max_length=30)
    last_name = models.CharField(_("Фамилия"), max_length=30)
    middle_name = models.CharField(_("Отчество"), max_length=30, blank=True)
    phone_number = PhoneNumberField(_('Номер телефона'), unique=True)

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')

    def __str__(self):
        return f'{self.id_employee}'


class Task(models.Model):
    task_date = models.DateField(verbose_name=_('Дата задачи'))
    id_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                    null=True, to_field='id_employee',
                                    verbose_name=_('Сотрудник'),
                                    related_name='tasks')
    task_details = models.CharField(max_length=255, verbose_name=_('Подробное описание'))

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')

    def __str__(self):
        task_details_short = self.task_details[:10]
        return f'{self.task_date} - {task_details_short}'
