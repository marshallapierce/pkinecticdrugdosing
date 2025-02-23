from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

#added 2/11/25
from .models import Patient, Age, Weight, Demographics, Creatinine
from .utils import leanbodyweightcalc
from django.utils import timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     # if User.objects.filter(email=data).exists():
    #     #     raise forms.ValidationError('This email is already in use.')
    #     if get_user_model().objects.filter(email=data).exists():
    #         raise forms.ValidationError('This email is already in use.')
    #     return data
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     qs =get_user_model().objects.exclude(id=self.instance.id).filter(email=data)
    #     if qs.exists():
    #         raise forms.ValidationError('This email is already in use.')
    #     return data
        
   
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

#added 2/1125
# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ['patient_name', 'date_of_birth']


class PatientForm(forms.ModelForm):
    # lbw = forms.DecimalField(label='Lean Body Weight (kg)', required=False, disabled=True)
    # height = forms.DecimalField(label='Height', required=False)
    # weight = forms.DecimalField(label='Weight', required=False)
    # height_units = forms.ChoiceField(choices=[('in', 'Inches'), ('cm', 'Centimeters')], initial='in', label='Height Units')
    # weight_unit = forms.ChoiceField(choices=[('kg', 'Kilograms'), ('lbs', 'Pounds')], initial='kg', label='Weight Units')
    # age = forms.IntegerField(label='Age', required=False)
    # sex = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], label='Sex', required=False)
    #lbw = forms.DecimalField(label='Lean Body Weight (kg)', required=False, disabled=True) #2/19/25 commented out

    class Meta:
        model = Patient
        #fields = ['patient_name', 'date_of_birth', 'lbw']  # Add other fields as needed
        #fields = ['patient_name', 'date_of_birth', 'height', 'weight', 'height_units', 'weight_unit', 'lbw']  # Add other fields as needed
        #fields = ['patient_name', 'date_of_birth', 'lbw']  # Removed 'lbw' 2.16.25
        fields = ['patient_name', 'date_of_birth']  

    # def __init__(self, *args, **kwargs):
    #     demographics = kwargs.pop('demographics', None)
    #     weight = kwargs.pop('weight', None)
    #     age = kwargs.pop('age', None)
    #     super().__init__(*args, **kwargs)
    #     if demographics:
    #         self.fields['height'].initial = demographics.heightinches
    #         self.fields['height_unit'].initial = demographics.height_unit
    #         self.fields['sex'].initial = demographics.sex
    #     if weight:
    #         self.fields['weight'].initial = weight.weight
    #         self.fields['weight_unit'].initial = weight.weight_unit
    #     if age:
    #         self.fields['age'].initial = age.age    

    # def clean(self):
    #     cleaned_data = super().clean()
    #     height = cleaned_data.get('height')
    #     weight = cleaned_data.get('weight')
    #     height_units = cleaned_data.get('height_units')
    #     weight_unit = cleaned_data.get('weight_unit')
    #     age = cleaned_data.get('age')
    #     sex = cleaned_data.get('sex')

    #     # Debugging print statements
   

        

class AgeForm(forms.ModelForm):
    #agedate = forms.DateField(initial=timezone.now().date())
    class Meta:
        model = Age
        fields = ['age']
        labels = {
            'age': 'Age',
            #'agedate': 'Date of Age Measurement',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        

        # Debugging print statements
        print(f"AgeForm Class")
        print(f"Weight: {age}")
        
        


class WeightForm(forms.ModelForm):
   # weightdate = forms.DateField(initial=timezone.now().date())
    weight_unit = forms.ChoiceField(choices=[('kg', 'Kilograms'), ('lbs', 'Pounds')], initial='kg', label='Weight Units')#, label='Weight Unit'
    class Meta:
        model = Weight
        fields = ['weight', 'weight_unit'] 
        labels = {
            'weight': 'Weight',
            #'weightdate': 'Date of Weight Measurement',
        }

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        weight_unit = cleaned_data.get('weight_unit')

        # Debugging print statements
        print(f"WeightForm Class")
        print(f"Weight: {weight}")
        print(f"Weight Units: {weight_unit}")
        

        if weight_unit == 'lbs':
            try:
                
                # Convert weight from pounds to kilograms
                converted_weight = Decimal(weight) * Decimal('0.453592')
                # Round the converted weight to a maximum of 5 digits
                cleaned_data['weight'] = converted_weight.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except (TypeError, ValueError, InvalidOperation) as e:
                raise forms.ValidationError(f"Error converting weight: {e}")
        return cleaned_data

class DemographicsForm(forms.ModelForm):
    height_unit = forms.ChoiceField(choices=[('in', 'Inches'), ('cm', 'Centimeters')], initial='in', label='Height Unit')#, label='Height Unit'

    class Meta:
        model = Demographics
        fields = ['heightinches', 'sex', 'height_unit'] #, 'height_unit'
        labels = {
            'heightinches': 'Height',
            'sex': 'Sex',
        }

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('heightinches')
        height_unit = cleaned_data.get('height_unit')

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('heightinches')
        height_unit = cleaned_data.get('height_unit')
        sex = cleaned_data.get('sex')

        # Debugging print statements
        print(f"DemographicForm Class")
        print(f"height: {height}")
        print(f"height Unit: {height_unit}")
        print(F"Sex: {sex}")

        if height and height_unit == 'cm':
            try:
                # Convert height from centimeters to inches
                cleaned_data['heightinches'] = Decimal(height) * Decimal('0.393701')
                # Round the converted height to 2 decimal places
                cleaned_data['heightinches'] = cleaned_data['heightinches'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except (TypeError, ValueError, InvalidOperation) as e:
                raise forms.ValidationError(f"Error converting height: {e}")

        return cleaned_data
    

class CreatinineForm(forms.ModelForm):
    scrtime = forms.DateTimeField(
        widget=DateTimePickerInput(),
        label='Date of Creatinine Measurement'
    )
    class Meta:
        model = Creatinine
        fields = ['scr', 'scrtime']
        labels = {
            'scr': 'Serum Creatinine (mg/dL)',
            'scrtime': 'Date of Creatinine Measurement',
        }

class CreatinineForm2(forms.ModelForm):
    scrtime = forms.DateTimeField(
        widget=DateTimePickerInput(),
        label='Date of Second Most Recent Creatinine Measurement'
    )
    class Meta:
        model = Creatinine
        fields = ['scr', 'scrtime']
        labels = {
            'scr': 'Second Most Recent Serum Creatinine (mg/dL)',
            'scrtime': 'Date of Second Most Recent Creatinine Measurement',
        }

class DrugForm(forms.Form):
    DRUG_CHOICES = [
        ('gentamicin', 'Gentamicin'),
        ('tobramycin', 'Tobramycin'),
        ('amikacin', 'Amikacin'),
        ('vancomycin', 'Vancomycin'),
    ]

    drug = forms.ChoiceField(choices=DRUG_CHOICES, label='Select Drug')