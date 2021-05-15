from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class OilField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    asurg = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                verbose_name=_('ASURG Equipment'))
    gas_disposal = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                       verbose_name=_('Gas utilization'))

    class Meta:
        verbose_name = _('Oil field')
        verbose_name_plural = _('Oil fields')

    def __str__(self):
        return self.name


class Incident(models.Model):
    incident_date = models.DateField(verbose_name=_('Date of the incident'))
    incident_count = models.IntegerField(verbose_name=_('Quantity'))
    incident_details = models.TextField(verbose_name=_('Detailed description'))

    class Meta:
        verbose_name = _('Incident')
        verbose_name_plural = _('Incidents')

    def __str__(self):
        return f'{self.incident_date}, quantity {self.incident_count}'


class Mining(models.Model):
    name_oilfield = models.ForeignKey(OilField, on_delete=models.CASCADE, verbose_name=_('Oil field'),
                                      related_name='mining')
    mining_date = models.DateField(verbose_name=_('Date'))
    mining_value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_('Production quantity'))

    class Meta:
        verbose_name = _('Minings')
        verbose_name_plural = _('Minings')

    def __str__(self):
        return f'{self.name_oilfield.name} - {self.mining_date}'


class Urgg(models.Model):
    urgg_date = models.DateField()
    urgg_count = models.IntegerField()

    class Meta:
        verbose_name = _('URGG indicator')
        verbose_name_plural = _('URGG indicators')

    def __str__(self):
        return f'{self.urgg_date} - {self.urgg_count} m3'


class CountWells(models.Model):
    wells_status = models.CharField(max_length=255, verbose_name=_('Status'))
    wells_count = models.IntegerField(verbose_name=_('Quantity'))

    class Meta:
        verbose_name = _('Count of wells')
        verbose_name_plural = _('Count of wells')

    def __str__(self):
        return f'{self.wells_status} - {self.wells_count} wells'


class Employee(models.Model):
    id_employee = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Employee number'))
    email = models.EmailField(_("email address"), max_length=40, unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    middle_name = models.CharField(_("middle name"), max_length=30, blank=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f'{self.id_employee}'


class Task(models.Model):
    task_date = models.DateField(verbose_name=_('Task date'))
    id_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                    null=True, to_field='id_employee',
                                    verbose_name=_('Employee'),
                                    related_name='tasks')
    task_details = models.CharField(max_length=255, verbose_name=_('Task details'))

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        task_details_short = self.task_details[:10]
        return f'{self.task_date} - {task_details_short}'
