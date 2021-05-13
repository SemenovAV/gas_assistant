from django.contrib import admin
from .models import Incident, OilField, Mining, Urgg, CountWells, Task, Employee


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_filter = ['incident_date']
    fields = ['incident_date', 'incident_count', 'incident_details']


@admin.register(OilField)
class OilFieldAdmin(admin.ModelAdmin):
    fields = ['name', 'asurg', 'gas_disposal']


@admin.register(Mining)
class MiningAdmin(admin.ModelAdmin):
    fields = ['name_oilfield', 'mining_date', 'mining_value']


@admin.register(Urgg)
class UrggAdmin(admin.ModelAdmin):
    fields = ['urgg_date', 'urgg_count']


@admin.register(CountWells)
class CountWellsAdmin(admin.ModelAdmin):
    fields = ['wells_status', 'wells_count']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['task_date', 'id_employee', 'task_details']


class TaskInlineAdmin(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ['id_employee', 'fio']
    inlines = [TaskInlineAdmin]
