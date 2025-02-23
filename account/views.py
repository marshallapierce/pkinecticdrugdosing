
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
#from .forms import LoginForm, UserRegistrationForm
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from .models import Patient, Age, Weight, Demographics, Creatinine
from .utils import bsa, leanbodyweightcalc, dosingweightcalc, creatinineclearancecalc
from django.utils import timezone
from .forms import PatientForm, AgeForm, WeightForm, DemographicsForm, CreatinineForm, DrugForm, CreatinineForm2

#added 2/11/25

from decimal import Decimal, InvalidOperation
from django.utils import timezone
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .utils import leanbodyweightcalc

#added 2/7/25
#from .forms import SignUpForm
#from .views import send_welcome_email


# Create youfrom djasngo.contrib.auth import authenr views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

#added 2/11/25
# @login_required
# def patient_create_view(request):
#     if request.method == 'POST':
#         patient_form = PatientForm(request.POST)
#         age_form = AgeForm(request.POST)
#         weight_form = WeightForm(request.POST)
#         demographics_form = DemographicsForm(request.POST)
#         creatinine_form = CreatinineForm(request.POST)

#         #added 2/14/15
#         context = {
#             'patient_form': patient_form,
#             'age_form': age_form,
#             'weight_form': weight_form,
#             'demographics_form': demographics_form,
#             'creatinine_form': creatinine_form,
#             'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media,
#         }
        
#         try:
#             if all([patient_form.is_valid(), age_form.is_valid(), weight_form.is_valid(), demographics_form.is_valid(), creatinine_form.is_valid()]):
#                 patient = patient_form.save(commit=False)
#                 patient.user = request.user  # Set the user field
#                 patient.save()
            
                
#                 age = age_form.save(commit=False)
#                 weight = weight_form.save(commit=False)
#                 demographics = demographics_form.save(commit=False)
#                 creatinine = creatinine_form.save(commit=False)
                
#                 age.patient = patient
#                 age.agedate = timezone.now().date()
#                 weight.patient = patient
#                 weight.weightdate = timezone.now().date()
#                 demographics.patient = patient
#                 creatinine.patient = patient
                
#                 age.save()
#                 weight.save()
#                 demographics.save()
#                 creatinine.save()

#                 # added 2/16/25
#                 # Calculate LBW
#                 height = demographics.heightinches
#                 weight_value = weight.weight
#                 height_unit = demographics.height_unit
#                 weight_unit = request.POST.get('weight_unit') #weight.weight_unit
#                 age_value = age.age
#                 sex = demographics.sex

#                 #debugging print statements
#                 print(f"Patient_Edit_View")
#                 print(f"Height: {height}")
#                 print(f"Height Units: {height_unit}")
#                 print(f"Weight: {weight_value}")
#                 print(f"Weight Units: {weight_unit}")
#                 print(f"Age: {age_value}")
#                 print(f"Sex: {sex}")

#                 if height and weight_value and height_unit and weight_unit and age_value and sex:
#                     try:
#                         lbw = leanbodyweightcalc(height, weight_value, height_unit, weight_unit, age_value, sex)
#                         patient.lbw = lbw  # Set the lbw field in the patient instance
            
#                         patient.save()  # Save the patient instance to update lbw
#                         print(f"Lean Body Weight (LBW): {lbw}")
#                     except Exception as e:
#                         messages.error(request, f"Error calculating LBW in patient_create_view: {e}")


#                 print("Form submitted successfully")
#                 return render(request,'account/patient_form.html', context)  # Redirect to a success page or another view
#             else:
#                 print("Form Patient Create View submission failed")
#                 print(patient_form.errors, age_form.errors, weight_form.errors, demographics_form.errors, creatinine_form.errors)
#                 messages.error(request, "Form submission failed")
#                 messages.error(request, patient_form.errors)
#                 messages.error(request, age_form.errors)
#                 messages.error(request, weight_form.errors)
#                 messages.error(request, demographics_form.errors)
#                 messages.error(request, creatinine_form.errors)
#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")
#             print(f"An error occurred: {e}")
    
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         patient_form = PatientForm()
#         age_form = AgeForm()
#         weight_form = WeightForm()
#         demographics_form = DemographicsForm()
#         creatinine_form = CreatinineForm()
    
#     context = {
#         'patient_form': patient_form,
#         'age_form': age_form,
#         'weight_form': weight_form,
#         'demographics_form': demographics_form,
#         'creatinine_form': creatinine_form,
#         'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media,
#     }
    
#     return render(request, 'account/patient_form.html', context)

@login_required
def patient_list_view(request):
    patients = Patient.objects.filter(user=request.user)
    context = {
        'patients': patients
    }
    return render(request, 'account/patient_list.html', context)

# @login_required
# def patient_edit_view(request, patient_id):
#     # obtain the patient instance using the patient_id and user, instances of other models created
#     patient = get_object_or_404(Patient, patient_id=patient_id, user=request.user)
#     age = Age.objects.filter(patient=patient).latest('agedate')
#     weight = Weight.objects.filter(patient=patient).latest('weightdate')
#     demographics = Demographics.objects.filter(patient=patient).latest('demo_id')
#     creatinine = Creatinine.objects.filter(patient=patient).latest('scrtime')
    
#     if request.method == 'POST':
#         # Create forms with the instance of the patient and related models
#         patient_form = PatientForm(request.POST, instance=patient)
#         age_form = AgeForm(request.POST, instance=age)
#         weight_form = WeightForm(request.POST, instance=weight)
#         demographics_form = DemographicsForm(request.POST, instance=demographics)
#         creatinine_form = CreatinineForm(request.POST, instance=creatinine)
        
#         context = {
#             'patient_form': patient_form,
#             'age_form': age_form,
#             'weight_form': weight_form,
#             'demographics_form': demographics_form,
#             'creatinine_form': creatinine_form,
#             'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media,
#         }

#         try: 

#             if all([patient_form.is_valid(), age_form.is_valid(), weight_form.is_valid(), demographics_form.is_valid(), creatinine_form.is_valid()]):
#                 patient_form.save()
#                 #If is_valid() is True, we’ll now be able to find all the validated form data in its cleaned_data attribute.
#                 # We can use this data to update the database or do other processing before sending an HTTP redirect to the browser telling it where to go next.
#                 #added2/12/25
#                 age = age_form.save(commit=False)
#                 weight = weight_form.save(commit=False)
#                 demographics = demographics_form.save(commit=False)
#                 creatinine = creatinine_form.save(commit=False)
                
#                 age.agedate = timezone.now().date()  # Set the agedate
#                 weight.weightdate = timezone.now().date()  # Set the weightdate
#                 #end added 2/12/25

#                 age_form.save()
#                 weight_form.save()
#                 demographics_form.save()
#                 creatinine_form.save()

#                 #added 2/16/25
#                 # Calculate LBW
#                 height = demographics.heightinches
#                 weight_value = weight.weight
#                 height_unit = demographics.height_unit
#                 weight_unit = request.POST.get('weight_unit') #weight.weight_unit
#                 age_value = age.age
#                 sex = demographics.sex

#                 print(f"Patient_Edit_View")
#                 print(f"Height: {height}")
#                 print(f"Height Units: {height_unit}")
#                 print(f"Weight: {weight_value}")
#                 print(f"Weight Units: {weight_unit}")
#                 print(f"Age: {age_value}")
#                 print(f"Sex: {sex}")

#                 if height and weight_value and height_unit and weight_unit and age_value and sex:
#                     try:
#                         lbw = leanbodyweightcalc(height, weight_value, height_unit, weight_unit, age_value, sex)
                
#                         patient.lbw = lbw  # Set the lbw field in the patient instance
#                         patient.save()  # Save the patient instance to update lbw
#                         print(f"Lean Body Weight (LBW): {lbw}")
#                     except Exception as e:
#                         messages.error(request, f"Error calculating LBW in Patient_Edit_View: {e}")
                
#                 messages.success(request, "Form submitted successfully")
#                 #return redirect('my_patients')  # Redirect to the patient list view
#                 #return redirect('dashboard')  # Redirect to the patient list view
#                 return render(request, 'account/patient_form.html', context)
#             else:
#                 print("Form Patient Edit View submission failed")
#                 print(patient_form.errors, age_form.errors, weight_form.errors, demographics_form.errors, creatinine_form.errors)
#                 messages.error(request, "Form submission failed")
#                 messages.error(request, patient_form.errors)
#                 messages.error(request, age_form.errors)
#                 messages.error(request, weight_form.errors)
#                 messages.error(request, demographics_form.errors)
#                 messages.error(request, creatinine_form.errors)
#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")
#             print(f"An error occurred: {e}")    
#             return render(request, 'account/patient_form.html', context)
#     else:
#         patient_form = PatientForm(instance=patient)
#         age_form = AgeForm(instance=age)
#         weight_form = WeightForm(instance=weight)
#         demographics_form = DemographicsForm(instance=demographics)
#         creatinine_form = CreatinineForm(instance=creatinine)

#     context = {
#         'patient_form': patient_form,
#         'age_form': age_form,
#         'weight_form': weight_form,
#         'demographics_form': demographics_form,
#         'creatinine_form': creatinine_form,
#         'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media,
#     }
    
#     return render(request, 'account/patient_form.html', context)

@login_required
def patient_create_view(request):
    if request.method == 'POST':
        # Create forms with the instance of the patient and related models with the submitted data
        patient_form = PatientForm(request.POST)
        age_form = AgeForm(request.POST)
        weight_form = WeightForm(request.POST)
        demographics_form = DemographicsForm(request.POST)
        creatinine_form = CreatinineForm(request.POST)
        creatinine_form2 = CreatinineForm2(request.POST)
        drug_form = DrugForm(request.POST)

        #The code snippet you provided is creating a context dictionary that will be passed to the template when rendering the form. 
        #This context dictionary contains the form instances and their associated media, which are necessary for rendering the forms correctly in the template
        #Adds the patient_form instance to the context. The purpose of this context dictionary is to pass the form instances and their associated media to the template. 
        # This allows the template to render the forms correctly and include any necessary JavaScript and CSS files.
        context = {
            'patient_form': patient_form,
            'age_form': age_form,
            'weight_form': weight_form,
            'demographics_form': demographics_form,
            'creatinine_form': creatinine_form,
            'creatinine_form2': creatinine_form2,
            'drug_form': drug_form,
            'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media + creatinine_form2.media + drug_form.media,
        }

        # see if all forms are valid
        try:
            if all([patient_form.is_valid(), age_form.is_valid(), weight_form.is_valid(), demographics_form.is_valid(), creatinine_form.is_valid(), creatinine_form2.is_valid(), drug_form.is_valid()]):
               
                print(f"Received Most Recent Creatinine line 334: {creatinine_form.cleaned_data['scr']} at {creatinine_form.cleaned_data['scrtime']}")
                print(f"Received Second Most Recent Creatinine: {creatinine_form2.cleaned_data['scr']} at {creatinine_form2.cleaned_data['scrtime']}")
                
                patient = patient_form.save(commit=False) # Save the patient instance without committing to the database
                patient.user = request.user  # Set the user field to the current user
                patient.save() # Save the patient instance to the database
              
                # If is_valid() is True, we’ll now be able to find all the validated form data in its cleaned_data attribute.
                # We can use this data to update the database or do other processing before sending an HTTP redirect to the browser telling it where to go next.
                age = age_form.save(commit=False) # Save the age_form data to create and age instance without committing to the database
                weight = weight_form.save(commit=False)
                demographics = demographics_form.save(commit=False)
                creatinine = creatinine_form.save(commit=False)
                creatinine2 = creatinine_form2.save(commit=False)  # Save the second creatinine form
                #drug_form does not need to be saved here as it is not tied to the model
                print(f"Most Recent Creatinine line 349: {creatinine.scr} at {creatinine.scrtime}")
                print(f"Second Most Recent Creatinine: {creatinine2.scr} at {creatinine2.scrtime}")
                #start here
                # Set the patient field for related models
                age.patient = patient #Sets the patient field of the Age instance to the newly created Patient instance.
                age.agedate = timezone.now().date()
                weight.patient = patient
                weight.weightdate = timezone.now().date()
                demographics.patient = patient
                creatinine.patient = patient
                creatinine2.patient = patient  # Set the patient field for the second creatinine form
                # Save the related models
                print(f"Most Recent Creatinine line 361: {creatinine.scr} at {creatinine.scrtime}")
                print(f"Second Most Recent Creatinine: {creatinine2.scr} at {creatinine2.scrtime}")
               
                #This line saves the Age instance to the database. The age instance was created 
                # earlier in the code using the age_form and associated with the patient instance.
                age.save()
                weight.save()
                demographics.save()
                creatinine.save()
                creatinine2.save()  # Save the second creatinine form

                # Print the values of creatinine_form and creatinine_form2
                print(f"Most Recent Creatinine: {creatinine.scr} at {creatinine.scrtime}")
                print(f"Second Most Recent Creatinine: {creatinine2.scr} at {creatinine2.scrtime}")

                # Calculate LBW
                height = demographics.heightinches
                weight_value = weight.weight
                height_unit = demographics.height_unit
                weight_unit = request.POST.get('weight_unit')  # Get weight_unit from the form data
                age_value = age.age
                sex = demographics.sex

                if height and weight_value and height_unit and weight_unit and age_value and sex:
                    try:
                        lbw = leanbodyweightcalc(height, weight_value, height_unit, weight_unit, age_value, sex)
                        #patient.lbw = lbw  # Set the lbw field in the patient instance
                        #patient_form.fields['lbw'].initial = lbw  # Set the lbw field in the form
                        context['lbw_label'] = 'Lean Body Weight (kg)'
                        context['lbw_value'] = lbw

                       # patient.save()  # Save the patient instance to update lbw
                        print(f"Lean Body Weight (LBW): {lbw}")
                    except Exception as e:
                        messages.error(request, f"Error calculating LBW in patient_create_view: {e}")
                    
                    try:
                        dosingweight = dosingweightcalc(weight_value, lbw, drug_form.cleaned_data['drug'])
                        context['dosingweight_label'] = 'Dosing Weight (kg)'
                        context['dosingweight_value'] = dosingweight
                        print(f"Dosing Weight: {dosingweight}")
                    except Exception as e:
                        messages.error(request, f"Error calculating dosing weight in patient_create_view: {e}")

                    try:
                        bsa_value = bsa(weight_value, height)
                        context['bsa_label'] = 'BSA (m²)'
                        context['bsa_value'] = bsa_value
                        print(f"Body Surface Area (BSA): {bsa_value}")
                    except Exception as e:
                        messages.error(request, f"Error calculating BSA in patient_select_drug_view: {e}") 

                    try:
                        clcr = creatinineclearancecalc(lbw, creatinine.scr, age_value, sex, height, bsa_value)
                        context['creatinineclearance_label'] = 'Creatinine Clearance (mL/min)'
                        context['creatinineclearance_value'] = clcr
                        print(f"Creatinine Clearance (Clcr): {clcr}")
                    except Exception as e:
                        messages.error(request, f"Error calculating creatinine clearance in patient_select_drug_view: {e}") 
                
                # Obtain the second most recent creatinine value
                creatinine_queryset = Creatinine.objects.filter(patient=patient).order_by('-scrtime')
                if creatinine_queryset.count() > 1:
                    creatinine2 = creatinine_queryset[1]
                    creatinine = creatinine_queryset.first()  # Update the first creatinine value
                else:
                    creatinine2 = creatinine_queryset.first()

                context['creatinine2'] = creatinine2  # Add creatinine2 to the context
                context['creatinine'] = creatinine  # Add creatinine to the context
                print(f"Creatinine: {creatinine}")
                print(f"Creatinine2: {creatinine2}")

                messages.success(request, "Form submitted successfully")
                return render(request, 'account/patient_form.html', context)
            else:
                print("Form Patient Create View submission failed")
                print(patient_form.errors, age_form.errors, weight_form.errors, demographics_form.errors, creatinine_form.errors, drug_form.errors)
                messages.error(request, "Form submission failed")
                messages.error(request, patient_form.errors)
                messages.error(request, age_form.errors)
                messages.error(request, weight_form.errors)
                messages.error(request, demographics_form.errors)
                messages.error(request, creatinine_form.errors)
                messages.error(request, creatinine_form2.errors)  # Add this line to display errors for the second creatinine form
                messages.error(request, drug_form.errors)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            print(f"An error occurred: {e}")

    else:
        patient_form = PatientForm()
        age_form = AgeForm()
        weight_form = WeightForm()
        demographics_form = DemographicsForm()
        creatinine_form = CreatinineForm()
        creatinine_form2 = CreatinineForm2()  # Initialize the second creatinine form
        drug_form = DrugForm()

    #creatinine2 = None  # Initialize creatinine2 to None
    #creatinine = None  # Initialize creatinine to None
    #creatinine2= None  # Initialize creatinine2 to None
    # # Obtain the second most recent creatinine value
    # creatinine_queryset = Creatinine.objects.filter(patient=patient).order_by('-scrtime')
    # if creatinine_queryset.count() > 1:
    #     creatinine2 = creatinine_queryset[1]
    # else:
    #     creatinine2 = creatinine_queryset.first()

    context = {
        'patient_form': patient_form,
        'age_form': age_form,
        'weight_form': weight_form,
        'demographics_form': demographics_form,
        'creatinine_form': creatinine_form,
        'creatinine_form2': creatinine_form2,  # Add the second creatinine form to the context
        'drug_form': drug_form,
    #    'creatinine': creatinine,  # Add creatinine to the context
    #    'creatinine2': creatinine2,  # Add creatinine2 to the context 
        'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media + creatinine_form2.media + drug_form.media,
    }

    return render(request, 'account/patient_form.html', context)

@login_required
def patient_edit_view(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id, user=request.user)
    age = Age.objects.filter(patient=patient).latest('agedate')
    weight = Weight.objects.filter(patient=patient).latest('weightdate')
    demographics = Demographics.objects.filter(patient=patient).latest('demo_id')
    creatinine = Creatinine.objects.filter(patient=patient).latest('scrtime')
    creatinine_queryset = Creatinine.objects.filter(patient=patient).order_by('-scrtime')
    if creatinine_queryset.count() > 1:
        creatinine2 = creatinine_queryset[1]
    else:
        creatinine2 = creatinine_queryset.first()

    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=patient)
        age_form = AgeForm(request.POST, instance=age)
        weight_form = WeightForm(request.POST, instance=weight)
        demographics_form = DemographicsForm(request.POST, instance=demographics)
        creatinine_form = CreatinineForm(request.POST, instance=creatinine)
        drug_form = DrugForm(request.POST)

        context = {
            'patient_form': patient_form,
            'age_form': age_form,
            'weight_form': weight_form,
            'demographics_form': demographics_form,
            'creatinine_form': creatinine_form,
            'drug_form': drug_form,
            'creatinine2': creatinine2,  # Add creatinine2 to the context
            'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media + drug_form.media,
        }

        try:
            if all([patient_form.is_valid(), age_form.is_valid(), weight_form.is_valid(), demographics_form.is_valid(), creatinine_form.is_valid(), drug_form.is_valid]):
                patient_form.save()
                # If is_valid() is True, we’ll now be able to find all the validated form data in its cleaned_data attribute.
                # We can use this data to update the database or do other processing before sending an HTTP redirect to the browser telling it where to go next.    
                age = age_form.save(commit=False)
                weight = weight_form.save(commit=False)
                demographics = demographics_form.save(commit=False)
                creatinine = creatinine_form.save(commit=False)
                # drug_form does not need to be saved here as it is not tied to the model
                # Set the patient field for related models  
                age.agedate = timezone.now().date()  # Set the agedate
                weight.weightdate = timezone.now().date()  # Set the weightdate
                # Save the related models
                age.save()
                weight.save()
                demographics.save()
                creatinine.save()

                # Calculate LBW
                height = demographics.heightinches
                weight_value = weight.weight
                height_unit = demographics.height_unit
                weight_unit = request.POST.get('weight_unit')  # Get weight_unit from the form data
                age_value = age.age
                sex = demographics.sex

                if height and weight_value and height_unit and weight_unit and age_value and sex:
                    try:
                        lbw = leanbodyweightcalc(height, weight_value, height_unit, weight_unit, age_value, sex)
                        #patient.lbw = lbw  # Set the lbw field in the patient instance
                        #patient_form.fields['lbw'].initial = lbw  # Set the lbw field in the form
                        context['lbw_label'] = 'Lean Body Weight (kg)'
                        context['lbw_value'] = lbw
                        #patient.save()  # Save the patient instance to update lbw
                        print(f"Lean Body Weight (LBW): {lbw}")
                    except Exception as e:
                        messages.error(request, f"Error calculating LBW in Patient_Edit_View: {e}")

                    try:
                        dosingweight = dosingweightcalc(weight_value, lbw, drug_form.cleaned_data['drug'])
                        context['dosingweight_label'] = 'Dosing Weight (kg)'
                        context['dosingweight_value'] = dosingweight
                        print(f"Dosing Weight: {dosingweight}")
                    except Exception as e:
                        messages.error(request, f"Error calculating dosing weight in Patient_Edit_View: {e}")    
                    
                    try:
                        bsa_value = bsa(weight_value, height)
                        context['bsa_label'] = 'BSA (m²)'
                        context['bsa_value'] = bsa_value
                        print(f"Body Surface Area (BSA): {bsa_value}")
                    except Exception as e:
                        messages.error(request, f"Error calculating BSA in patient_select_drug_view: {e}") 

                    try:
                        clcr = creatinineclearancecalc(lbw, creatinine.scr, age_value, sex, height, bsa_value)
                        context['creatinineclearance_label'] = 'Creatinine Clearance (mL/min)'
                        context['creatinineclearance_value'] = clcr
                        print(f"Creatinine Clearance (Clcr): {clcr}")
                    except Exception as e:
                        messages.error(request, f"Error calculating dosing weight in patient_select_drug_view: {e}")
                
                messages.success(request, "Form submitted successfully")
                return render(request, 'account/patient_form.html', context)
            else:
                print("Form Patient Edit View submission failed")
                print(patient_form.errors, age_form.errors, weight_form.errors, demographics_form.errors, creatinine_form.errors, drug_form.errors)
                messages.error(request, "Form submission failed")
                messages.error(request, patient_form.errors)
                messages.error(request, age_form.errors)
                messages.error(request, weight_form.errors)
                messages.error(request, demographics_form.errors)
                messages.error(request, creatinine_form.errors)
                messages.error(request, drug_form.errors)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            print(f"An error occurred: {e}")
            return render(request, 'account/patient_form.html', context)
    else:
        patient_form = PatientForm(instance=patient)
        age_form = AgeForm(instance=age)
        weight_form = WeightForm(instance=weight)
        demographics_form = DemographicsForm(instance=demographics)
        creatinine_form = CreatinineForm(instance=creatinine)
        #drug_form = DrugForm  # Initialize the drug form with the current drug value
        drug_form = DrugForm()
        #drug_form = DrugForm(initial={'drug': patient.drug})  # Initialize the drug form with the current drug value

    context = {
        'patient_form': patient_form,
        'age_form': age_form,
        'weight_form': weight_form,
        'demographics_form': demographics_form,
        'creatinine_form': creatinine_form,
        'drug_form': drug_form,
        'creatinine2': creatinine2,  # Add creatinine2 to the context
        'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media + drug_form.media,
    }

    return render(request, 'account/patient_form.html', context)


@login_required
def patient_select_drug_view(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id, user=request.user)
    age = Age.objects.filter(patient=patient).latest('agedate')
    weight = Weight.objects.filter(patient=patient).latest('weightdate')
    demographics = Demographics.objects.filter(patient=patient).latest('demo_id')
    creatinine = Creatinine.objects.filter(patient=patient).latest('scrtime')

     # Obtain the second most recent creatinine value
    creatinine_queryset = Creatinine.objects.filter(patient=patient).order_by('-scrtime')
    if creatinine_queryset.count() > 1:
        creatinine2 = creatinine_queryset[1]
    else:
        creatinine2 = creatinine_queryset.first()

    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=patient)
        age_form = AgeForm(request.POST, instance=age)
        weight_form = WeightForm(request.POST, instance=weight)
        demographics_form = DemographicsForm(request.POST, instance=demographics)
        creatinine_form = CreatinineForm(request.POST, instance=creatinine)
        drug_form = DrugForm(request.POST)

        context = {
            'patient_form': patient_form,
            'age_form': age_form,
            'weight_form': weight_form,
            'demographics_form': demographics_form,
            'creatinine_form': creatinine_form,
            'drug_form': drug_form,
            'creatinine2': creatinine2,  # Add creatinine2 to the context
            'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media + drug_form.media,
        }

        try:
            if all([patient_form.is_valid(), age_form.is_valid(), weight_form.is_valid(), demographics_form.is_valid(), creatinine_form.is_valid(), drug_form.is_valid()]):
                # Process the selected drug without saving it to the Patient model
                selected_drug = drug_form.cleaned_data['drug']
                print(f"Selected Drug: {selected_drug}")

                #added from patient_edit_view
                patient_form.save()
                # If is_valid() is True, we’ll now be able to find all the validated form data in its cleaned_data attribute.
                # We can use this data to update the database or do other processing before sending an HTTP redirect to the browser telling it where to go next.    
                age = age_form.save(commit=False)
                weight = weight_form.save(commit=False)
                demographics = demographics_form.save(commit=False)
                creatinine = creatinine_form.save(commit=False)
                # drug_form does not need to be saved here as it is not tied to the model
                # Set the patient field for related models  
                age.agedate = timezone.now().date()  # Set the agedate
                weight.weightdate = timezone.now().date()  # Set the weightdate
                # Save the related models
                age.save()
                weight.save()
                demographics.save()
                creatinine.save()

                # end of added from patient_edit_view

                # Calculate LBW
                height = demographics.heightinches
                weight_value = weight.weight
                height_unit = demographics.height_unit
                weight_unit = request.POST.get('weight_unit')  # Get weight_unit from the form data
                age_value = age.age
                sex = demographics.sex

                if height and weight_value and height_unit and weight_unit and age_value and sex:
                    try:
                        lbw = leanbodyweightcalc(height, weight_value, height_unit, weight_unit, age_value, sex)
                        context['lbw_label'] = 'Lean Body Weight (kg)'
                        context['lbw_value'] = lbw
                        print(f"Lean Body Weight (LBW): {lbw}")
                    except Exception as e:
                        messages.error(request, f"Error calculating LBW in patient_select_drug_view: {e}")

                    try:
                        dosingweight = dosingweightcalc(weight_value, lbw, selected_drug)
                        context['dosingweight_label'] = 'Dosing Weight (kg)'
                        context['dosingweight_value'] = dosingweight
                        print(f"Dosing Weight: {dosingweight}")
                    except Exception as e:
                        messages.error(request, f"Error calculating dosing weight in patient_select_drug_view: {e}")
                    
                    try:
                        bsa_value = bsa(weight_value, height)
                        context['bsa_label'] = 'BSA (m²)'
                        context['bsa_value'] = bsa_value
                        print(f"Body Surface Area (BSA): {bsa_value}")
                    except Exception as e:
                        messages.error(request, f"Error calculating BSA in patient_select_drug_view: {e}") 

                    try:
                        clcr = creatinineclearancecalc(lbw, creatinine.scr, age_value, sex, height, bsa_value)
                        context['creatinineclearance_label'] = 'Creatinine Clearance (mL/min)'
                        context['creatinineclearance_value'] = clcr
                        print(f"Creatinine Clearance (Clcr): {clcr}")
                    except Exception as e:
                        messages.error(request, f"Error calculating dosing weight in patient_select_drug_view: {e}")



                messages.success(request, "Form submitted successfully")
                return render(request, 'account/patient_form.html', context)
            else:
                print("Form Patient Select Drug View submission failed")
                print(patient_form.errors, age_form.errors, weight_form.errors, demographics_form.errors, creatinine_form.errors, drug_form.errors)
                messages.error(request, "Form submission failed")
                messages.error(request, patient_form.errors)
                messages.error(request, age_form.errors)
                messages.error(request, weight_form.errors)
                messages.error(request, demographics_form.errors)
                messages.error(request, creatinine_form.errors)
                messages.error(request, drug_form.errors)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            print(f"An error occurred: {e}")
            return render(request, 'account/patient_form.html', context)
    else:
        patient_form = PatientForm(instance=patient)
        age_form = AgeForm(instance=age)
        weight_form = WeightForm(instance=weight)
        demographics_form = DemographicsForm(instance=demographics)
        creatinine_form = CreatinineForm(instance=creatinine)
        drug_form = DrugForm()

    context = {
        'patient_form': patient_form,
        'age_form': age_form,
        'weight_form': weight_form,
        'demographics_form': demographics_form,
        'creatinine_form': creatinine_form,
        'creatinine2': creatinine2,  # Add creatinine2 to the context
        'drug_form': drug_form,
        'form_media': patient_form.media + age_form.media + weight_form.media + demographics_form.media + creatinine_form.media + drug_form.media,
    }

    return render(request, 'account/patient_form.html', context)
#added 2/7/25
#def signup(request): #pretty much the same as register but uses the SignUpForm
#    if request.method == 'POST':
#        form = SignUpForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            send_welcome_email(user.email)
#            return redirect('login')
#    else:
#        form = SignUpForm()
#    return render(request, 'account/signup.html', {'form': form})

            