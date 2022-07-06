from django.contrib import admin

from dempster_shafer_structure.models import Diagnose, Symptom, FocalElement, FocalElementSymptomWeight


class DiagnoseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Diagnose, DiagnoseAdmin)


class SymptomAdmin(admin.ModelAdmin):
    list_display = ['position', 'name']
    ordering = ('position',)


admin.site.register(Symptom, SymptomAdmin)


class FocalElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'bpa', 'symptom_list')
    ordering = ('name',)

    def symptom_list(self, obj):
        return ', '.join(s.name for s in obj.symptoms.all())


admin.site.register(FocalElement, FocalElementAdmin)


class FocalElementSymptomWeightAdmin(admin.ModelAdmin):
    list_display = ('focal_element', 'symptom', 'weight')
    ordering = ('focal_element', 'symptom__position')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FocalElementSymptomWeightAdmin, self).get_form(request, obj, change, **kwargs)
        if obj:
            form.base_fields['symptom'].queryset = obj.focal_element.symptoms
        return form


admin.site.register(FocalElementSymptomWeight, FocalElementSymptomWeightAdmin)
