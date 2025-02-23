# Create your models here.
from django.db import models
from django.conf import settings

# added 2/7/25
from django.core.mail import send_mail

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

# Create your models here.

#added 2/10/25
# Define the Patient model
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hippa = models.CharField(max_length=100) #one of these need to be removed
    patient_name = models.CharField(max_length=100) #one of these need to be removed
    date_of_birth = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return f'Patient {self.patient_name} for user {self.user.username}'
    
# Define the Level model
class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    level = models.DecimalField(max_digits=5, decimal_places=2)
    leveltime = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    drug = models.CharField(max_length=100)

    def __str__(self):
        return f'Level {self.level} for patient {self.patient.patient_name} at {self.leveltime}'
    
# Define the Dose model
class Dose(models.Model):
    dose_id = models.AutoField(primary_key=True)
    dose = models.DecimalField(max_digits=6, decimal_places=2)
    dosetime = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    drug = models.CharField(max_length=100)

    def __str__(self):
        return f'Dose {self.dose} for patient {self.patient.patient_name} at {self.dosetime}'
    
# Define the Demographics model
class Demographics(models.Model):
    demo_id = models.AutoField(primary_key=True)
    heightinches = models.DecimalField(max_digits=5, decimal_places=2)
    #sex = models.CharField(max_length=1)
    height_unit = models.CharField(max_length=2, choices=[('in', 'Inches'), ('cm', 'Centimeters')], default='in')
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'Demographics for patient {self.patient.patient_name}'
    
# Define the Creatinine model
class Creatinine(models.Model):
    scr_id = models.AutoField(primary_key=True)
    scr = models.DecimalField(max_digits=5, decimal_places=2)
    scrtime = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'Creatinine {self.scr} for patient {self.patient.patient_name} at {self.scrtime}'   
    
# Define the Age model
class Age(models.Model):
    age_id = models.AutoField(primary_key=True)
    age = models.DecimalField(max_digits=5, decimal_places=2)
    agedate = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'Age {self.age} for patient {self.patient.patient_name} at {self.agedate}'
    
# Define the Weight model
class Weight(models.Model):
    weight_id = models.AutoField(primary_key=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    weightdate = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'Weight {self.weight} for patient {self.patient.patient_name} on {self.weightdate}'

#add 2/7/25
def send_welcome_email(user_email):
    subject = 'Welcome to PkineticDrugDosing'
    message = 'Thank you for signing up to PkineticDrugDosing.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)