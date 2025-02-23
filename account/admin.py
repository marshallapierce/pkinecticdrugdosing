from django.contrib import admin
#from .models import Profile 
from .models import Profile, Patient, Level, Dose, Demographics, Creatinine, Age, Weight

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'user', 'date_of_birth']
    raw_id_fields = ['user']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level', 'leveltime', 'patient', 'drug']
    raw_id_fields = ['patient']

@admin.register(Dose)
class DoseAdmin(admin.ModelAdmin):
    list_display = ['dose', 'dosetime', 'patient', 'drug']
    raw_id_fields = ['patient']

@admin.register(Demographics)
class DemographicsAdmin(admin.ModelAdmin):
    list_display = ['heightinches', 'sex', 'patient']
    raw_id_fields = ['patient']

@admin.register(Creatinine)
class CreatinineAdmin(admin.ModelAdmin):
    list_display = ['scr', 'scrtime', 'patient']
    raw_id_fields = ['patient']

@admin.register(Age)
class AgeAdmin(admin.ModelAdmin):
    list_display = ['age', 'agedate', 'patient']
    raw_id_fields = ['patient']

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ['weight', 'weightdate', 'patient']
    raw_id_fields = ['patient']