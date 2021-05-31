from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Incident, OilField, Well, Task, Employee, GasDisposal, Mining, Urgg


@admin.register(GasDisposal)
class GasDisposalAdmin(admin.ModelAdmin):
    list_filter = ['gas_disposal_date']
    list_display = ['gas_disposal_count', 'gas_disposal_date']


@admin.register(Mining)
class MinningAdmin(admin.ModelAdmin):
    list_filter = ['mining_date']
    list_display = ['mining_count', 'mining_date']


@admin.register(Urgg)
class UrggAdmin(admin.ModelAdmin):
    list_filter = ['urgg_date']
    list_display = ['urgg_count', 'urgg_date']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_filter = ['incident_date']
    list_display = ['incident_date', 'incident_count', 'incident_details']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['task_date', 'id_employee', 'task_details']


class TaskInlineAdmin(admin.TabularInline):
    model = Task
    extra = 1


class GasDisposalInline(admin.TabularInline):
    model = GasDisposal
    list_filter = ['gas_disposal_date']
    extra = 1


class UrggInline(admin.TabularInline):
    model = Urgg
    list_filter = ['urgg_date']
    extra = 1


class MiningInline(admin.TabularInline):
    model = Mining
    list_filter = ['mining_date']
    extra = 1


@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    list_filter = ['oilfield']
    fields = ['oilfield', 'ident_number', 'well_type']
    inlines = (GasDisposalInline, UrggInline, MiningInline)


class WellInline(admin.TabularInline):
    model = Well
    extra = 1


@admin.register(OilField)
class OilFieldAdmin(admin.ModelAdmin):
    fields = ['name']
    inlines = (WellInline,)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    ordering = ("email",)
    list_display = ("id_employee", "email", "phone_number", "full_name")
    search_fields = ("id_employee", "email", "full_name")
    fieldsets = (
        (None, {"fields": ("phone_number", "email")}),
        (_("Персональная информация"), {"fields": ("first_name", "last_name", "middle_name")}),
    )

    def full_name(self, obj):
        return obj.get_full_name
