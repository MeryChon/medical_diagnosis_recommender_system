from django.core.exceptions import ValidationError
from django.db import models


class Diagnose(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256)

    class Meta:
        db_table = 'diagnoses'

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256)
    position = models.IntegerField(null=False)

    class Meta:
        db_table = 'symptoms'

    def __str__(self):
        return self.name


class FocalElement(models.Model):
    name = models.CharField(null=False, blank=False, max_length=64)
    symptoms = models.ManyToManyField(Symptom, related_name='focal_elements')
    bpa = models.DecimalField(null=False, decimal_places=3, max_digits=4)

    class Meta:
        db_table = 'focal_elements'

    def __str__(self):
        return self.name


class FocalElementSymptomWeight(models.Model):
    focal_element = models.ForeignKey(FocalElement, related_name='symptom_weights', on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, related_name='focal_element_weights', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"{self.focal_element.name} - {self.symptom.name}"

    def symptom_position(self):
        return self.symptom.position

    def clean(self):
        if self.symptom not in self.focal_element.symptoms.all():
            raise ValidationError({
                'symptom': [f'Must be one of {[", ".join(s.name for s in self.focal_element.symptoms.all())]}']
            })
