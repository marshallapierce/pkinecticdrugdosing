import traceback
import math, decimal
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

#Dont use function names as the name of the returned variable
#This is because the function name will be used as the key in the dictionary
#and if the function name is the same as the returned variable, it will cause a conflict

def bsacalc(weight, height):
    try:
         # Convert height and weight to float
        height = float(height)
        weight = float(weight)
       
        # weight in kg, height in inches
        bsa = 0.007184 * (weight**0.425) * ((height*2.54)**0.725)
        # Round the BSA to 2 decimal places
        bsa = Decimal(bsa).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return bsa
    except(TypeError, ValueError, ZeroDivisionError) as e:
        # Log the error or handle it as needed
        print(f"Error calculating BSA: {e}")
        return None

def leanbodyweightcalc(height,weight,height_units, weight_units, age, sex):
    try:
        # Convert height and weight to inches and kg respectively
         # Convert height and weight to float
        height = float(height)
        weight = float(weight)
        age = float(age)

        if height_units == 'cm':
            height = height / 2.54  # Convert cm to inches, inches is default height
            print(f"Height in inches: {height}")
        if weight_units == 'lb':
            weight = weight * 0.453592  # Convert pounds to kg, kg is default weight
            print(f"Weight in kgs: {weight}")
        lbw = None  # Initialize lbw variable

        if sex=='M':
            if age >=18:
                lbw = 50 + 2.3*(height-60)
                print(f"Age: {age}")
        elif age < 18 and height < 22:
            lbw = weight
        elif age < 18 and height < 48: #lener, Peck, Brown, Perlin Formula 
            lbw = (-59.6035 + (5.2878*height) -(0.123939*(height**2))+ (0.00128936*(height**3)) )/2.2
        if sex=='F':
            if age >=18:
                lbw = 45.5 + 2.3*(height-60)
        elif age < 18 and height < 22:
            lbw = weight
        elif age < 18 and height < 48:
            lbw =(-77.55796 + (6.93728*height) - (0.171703*(height**2)) + (0.001726*(height**3)))/2.2
        if lbw is not None and lbw > weight:
            lbw = weight
        # Round the Lean Body Weight (LBW) to 2 decimal places
        lbw = Decimal(lbw).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return lbw  # Return the calculated Lean Body Weight (LBW)
        # Calculate Lean Body Weight (LBW) based on
    except (TypeError, ValueError, ZeroDivisionError) as e:
        # Log the error or handle it as needed
        print(f"Error calculating Lean Body Weight in lbw function: {e}")
        print(traceback.format_exc())
        return None
    
def dosingweightcalc (weight, lbw, drug):
    try:
        # Convert weight and lbw to float
        weight = float(weight)
        lbw = float(lbw)

         # Calculate dosing weight based on the drug
        if drug in ['gentamicin', 'tobramycin', 'amikacin']:
            if weight < lbw:
                dosingweight=weight
                #return dosingweight
            else:
                dosingweight = lbw + 0.4* (weight - lbw)
                #return dosingweight
            dosingweight = Decimal(dosingweight).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return dosingweight
        elif drug == 'vancomycin':
            if weight <= lbw:
                dosingweight = weight
                #return dosingweight
            else:
                dosingweight = weight
                #return dosingweight
            # round dosing wight to 2 decimal places
            dosingweight = Decimal(dosingweight).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return dosingweight
        else:
            return None  # Return None for unsupported drugs
    except (TypeError, ValueError, ZeroDivisionError) as e:
        # Log the error or handle it as needed
        print(f"Error calculating dosing weight: {e}")
        print(traceback.format_exc())
        return None
    
def creatinineclearancecalc(lbw, scr, age, sex, height, bsa):
    try:
    # Convert lbw, scr, age, height to float
        lbw = float(lbw)
        scr = float(scr)
        age = float(age)
        height = float(height)
        if sex=='M':
            if age >= 18:
                crcl = (140 - age) * lbw / (72 * scr)
            elif age < 2:
                crcl = 0.45*height*2.54*bsa/(scr*1.73)
            elif age >=2 and age <13:
                crcl = 0.55*height*2.54*bsa/(scr*1.73)
            elif age >=13 and age <18:
                crcl = 0.7*height*2.54*bsa/(scr*1.73)
        elif sex=='F':
            if age >= 18:
                crcl = (140 - age) * 0.85 * lbw / (72 * scr)
            elif age < 2:
                crcl = 0.45*height*2.54*bsa / (scr*1.73)
            elif age >=2 and age <13:
                crcl = 0.55*height*2.54*bsa / (scr*1.73)
            elif age >=13 and age <18:
                crcl = 0.55*height*2.54*bsa / (scr*1.73)
        # Round the Creatinine Clearance (CrCl) to 2 decimal places
        crcl = Decimal(crcl).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return crcl  # Return the calculated Creatinine Clearance (CrCl)
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating Creatinine Clearance: {e}")
        print(traceback.format_exc())
        return None
        
def creatininecalc(creatinineold, k, hoursdiff, age, sex, lbw, height):
    try:
        # Convert creatininenew, k, hoursdiff, age, lbw, height to float
        #k is L/hours (cleearance) and creatinineold is in mg/dL
        creatinineold = float(creatinineold)
        k = float(k) # L/hours clearance
        hoursdiff = float(hoursdiff)
        age = float(age) # years
        lbw = float(lbw) # kg
        height = float(height) # inches
        creatinineold = creatinineold * 10 # mg/dL to mg/L
        if sex == 'M':
            if age >= 18:
                ratein = (28-(0.2*age))*lbw/24 # mg/hr
            elif age < 2:
                ratein= height*2.54*0.45*600/1000 # mg/hr
            elif age >= 2 and age < 13:
                ratein=height*2.54*0.55*600/1000 # mg/hr
            elif age >= 13 and age < 18:
                ratein=height*2.54*0.7*600/1000 # mg/hr
        elif sex=='F':
            if age >= 18:
                ratein = (28-(0.2*age))*lbw*0.85/24 # mg/hr
            elif age < 2:   
                ratein= height*2.54*0.45*600/1000 # mg/hr
            elif age >= 2 and age < 13:         
                ratein=height*2.54*0.55*600/1000 # mg/hr
            elif age >= 13 and age < 18:
                ratein=height*2.54*0.55*600/1000 # mg/hr
        # Creatinine Calculate
        creatininenewest = (creatinineold*math.exp((-k*hoursdiff)/(0.6*lbw))) + (ratein/k)*(1-math.exp((-k*hoursdiff)/(0.6*lbw))) #mg/L
        return creatininenewest
    except (TypeError, ValueError, ZeroDivisionError) as e:
        # Log the error or handle it as needed
        print(f"Error calculating Creatinine: {e}")
        print(traceback.format_exc())
        return None

def creatinineclearancecalc2(creatinineold, creatininenew, hoursdifference, age, sex, lbw, crcl, bsa, height):
    try:
        # Convert creatininenew, hoursdifference, age, lbw, creatinineclearance, bsa, height to float
        creatinineold = float(creatinineold)
        creatininenew = float(creatininenew)
        crcl= float(crcl) #used calculating most recent scr
        hoursdifference = float(hoursdifference)
        age = float(age)
        lbw = float(lbw)
        bsa = float(bsa)
        height = float(height)
        k1=crcl*0.1*60/1000 # ml/min convert to L/hr 1/10 of the original value
        k2= k1*1.05 # so clearance is increasing
        k3= None
        cp1= None
        while(abs((k2-k1)/k1)>0.000500001):
           cp1=creatininecalc(creatinineold, k1, hoursdifference, age, sex, lbw, height) #returns mg/L
           cpchange1= (cp1-(creatininenew*10)) #mg/L
           cp2 =creatininecalc(creatinineold, k2, hoursdifference, age, sex, lbw, height) # returns mg/L
           cpchange2= (cp2-(creatininenew*10)) # mg/L
           #              slope                       x+        b(intercept)
           # y=mx+b
           k3 = (-(k2-k1) / (cpchange2-cpchange1))*cpchange2 + k2
           k1=k2
           k2=k3
                   
        
        if age < 18:
            crcl=k2*(1000/60)*bsa/1.73 # convert L/Hr to ml/min/1.73m2
        elif age >= 18:
            clcr =k2*1000/60 # convert L/Hr to ml/min
        clcr = Decimal(clcr).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return clcr
    except (TypeError, ValueError, ZeroDivisionError) as e:
        # Log the error or handle it as needed
        print(f"Error calculating Creatinine Clearance: {e}")
        print(traceback.format_exc())
        return None
    
def hoursdifferencecalc(time1, time2):
    try:
        # Ensure time1 and time2 are datetime objects
        if not isinstance(time1, datetime):
            time1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
        if not isinstance(time2, datetime):
            time2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
        
        # Calculate the difference between the two times
        time_difference = time2 - time1
        
        # Convert the difference to hours
        hours_difference = time_difference.total_seconds() / 3600.0
        
        return hours_difference
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error calculating hours difference: {e}")
        return None
    
def eliminationratecalc(clcr, drug, bsa):
    try:
        # Convert clcr to float
        clcr = float(clcr)
        bsa = float(bsa)
        if drug == 'vancomycin':                      #needs work for peds
            k=0.00107*clcr*1.73/bsa + 0.005216005
            #return k
        elif drug in ['gentamicin', 'tobramycin', 'amikacin']:
            k = 0.0026*clcr+ 0.014
            #k=clcr/1000*0.693/2 # 2 hours half life
            #return k
        elif drug == 'piperacillin':
            k=clcr/1000*0.693/1.5 # 1.5 hours half life
            #return k
        elif drug == 'cefepime':
            k=clcr/1000*0.693/2 # 2 hours half life
            #return k
        elif drug == 'meropenem':
            k=clcr/1000*0.693/1 # 1 hour half life
            #return k
        elif drug == 'imipenem':
            k=clcr/1000*0.693/1 # 1 hour half life
            #return k
        elif drug == 'ertapenem':
            k=clcr/1000*0.693/4.5 # 4.5 hours half life
            #return k
        elif drug == 'ceftriaxone':
            k=clcr/1000*0.693/8 # 8 hours half life
            #return k
        elif drug == 'aztreonam':
            k=clcr/1000*0.693/2 # 2 hours half life
            #return k
        elif drug == 'ciprofloxacin':
            k=clcr/1000*0.693/4 # 4 hours half life
            #return k 
        elif drug == 'levofloxacin':
            k=clcr/1000*0.693/8 # 8 hours half life 
            #return k 
        else:
             return None  # Return None for unsupported drugs
        k= Decimal(k).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        return k
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating elimination rate: {e}")
        print(traceback.format_exc())
        return None

def Vdcalc(dosingweight, drug):
    try:
        # Convert dosingweight to float
        dosingweight = float(dosingweight)
        if drug == 'vancomycin':
            Vd=0.65*dosingweight
            #return Vd
        elif drug in ['gentamicin', 'tobramycin', 'amikacin']:
            Vd=0.25*dosingweight
            #return Vd
        elif drug == 'piperacillin':
            Vd=0.3*dosingweight
            #return Vd
        elif drug == 'cefepime':
            Vd=0.2*dosingweight
            #return Vd
        elif drug == 'meropenem':
            Vd=0.2*dosingweight
            #return Vd
        elif drug == 'imipenem':
            Vd=0.2*dosingweight
            #return Vd
        elif drug == 'ertapenem':
            Vd=0.2*dosingweight
            #return Vd
        elif drug == 'ceftriaxone':
            Vd=0.1*dosingweight
            #return Vd
        elif drug == 'aztreonam':
            Vd=0.1*dosingweight
            #return Vd
        elif drug == 'ciprofloxacin':
            Vd=0.3*dosingweight
            #return Vd 
        elif drug == 'levofloxacin':
            Vd=0.3*dosingweight 
            #return Vd 
        else:
             return None  # Return None for unsupported drugs
        Vd = Decimal(Vd).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Vd
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating Volume of Distribution: {e}")
        print(traceback.format_exc())
        return None

def Vdperkgcalc(vd, dosingweight):
    try:
        # Convert vd and dosingweight to float
        vd = float(vd)
        dosingweight = float(dosingweight)
        Vdperkg=vd/dosingweight
        Vdperkg = Decimal(Vdperkg).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Vdperkg
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating Volume of Distribution per kg: {e}")
        print(traceback.format_exc())
        return None

def drughalf_lifecalc(eliminationrate):
    try:
        # Convert eliminationrate to float
        eliminationrate = float(eliminationrate)
        drughalf_life=0.693/eliminationrate
        drughalf_life = Decimal(drughalf_life).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        return drughalf_life
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating Drug Half Life: {e}")
        print(traceback.format_exc())
        return None

def loadingdosecalc(infusionperiod, eliminationrate, drug, vd):
    try:
        # Convert infusionperiod and eliminationrate to float
        infusionperiod = float(infusionperiod)
        eliminationrate = float(eliminationrate)
        vd = float(vd)
        if drug == 'vancomycin':
            loadingdose=30*vd*eliminationrate*infusionperiod/(1-math.exp(-eliminationrate*infusionperiod))
            #return loadingdose
        elif drug in ['gentamicin', 'tobramycin']:
            loadingdose=10*vd*eliminationrate*infusionperiod/(1-math.exp(-eliminationrate*infusionperiod))
        elif drug == 'amikacin':
            loadingdose=30*vd*eliminationrate*infusionperiod/(1-math.exp(-eliminationrate*infusionperiod))
            #return loadingdose
        elif drug == 'piperacillin':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'cefepime':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'meropenem':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'imipenem':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'ertapenem':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'ceftriaxone':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'aztreonam':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose
        elif drug == 'ciprofloxacin':
            loadingdose=0.5*eliminationrate*vd*infusionperiod
            #return loadingdose 
        elif drug == 'levofloxacin':
            loadingdose=0.5*eliminationrate*vd*infusionperiod 
            #return loadingdose 
        else:
             return None  # Return None for unsupported drugs
        loadingdose = Decimal(loadingdose).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return loadingdose
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed 
        print(f"Error calculating Loading Dose: {e}")
        print(traceback.format_exc())   
        return None

def maintenancedosecalc(drug, dosingweight):
    dosingweight = float(dosingweight)
    if drug == 'vancomycin':
        maintenancedose=15*dosingweight
        #return maintenancedose
    elif drug in ['gentamicin', 'tobramycin']:
        maintenancedose=1.5*dosingweight
        #return maintenancedose 
    elif drug == 'amikacin':
        maintenancedose=7.5*dosingweight 
        #return maintenancedose
    elif drug == 'piperacillin':
        maintenancedose=0.5*dosingweight
        #return maintenancedose
    elif drug == 'cefepime':
        maintenancedose=0.5*dosingweight
        #return maintenancedose
    elif drug == 'meropenem':
        maintenancedose=0.5*dosingweight
        #return maintenancedose
    elif drug == 'imipenem':
        maintenancedose=0.5*dosingweight
        #return maintenancedose
    elif drug == 'ertapenem':
        maintenancedose=0.5*dosingweight
        #return maintenancedose
    elif drug == 'ceftriaxone':
        maintenancedose=0.5*dosingweight
        #return maintenancedose     
    elif drug == 'aztreonam':
        maintenancedose=0.5*dosingweight    
        #return maintenancedose
    elif drug == 'ciprofloxacin':
        maintenancedose=0.5*dosingweight
        #return maintenancedose     
    elif drug == 'levofloxacin':
        maintenancedose=0.5*dosingweight    
        #return maintenancedose
    else:
         return None
    maintenancedose = Decimal(maintenancedose).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return maintenancedose


def taucalc(drug, EliminationRate, InfusionPeriod, Vd, MaintenanceDose):
    try:
        # Convert EliminationRate, InfusionPeriod, MaintenanceDose to float
        EliminationRate = float(EliminationRate)
        InfusionPeriod = float(InfusionPeriod)
        MaintenanceDose = float(MaintenanceDose)
        Vd=float(Vd)
        if drug == 'vancomycin':
            tau=(MaintenanceDose*24)/(EliminationRate*Vd*500)
            #return tau
        elif drug in ['gentamicin', 'tobramycin']:
            tau=math.log(8/1)/EliminationRate + InfusionPeriod
            #return tau
        elif drug == 'amikacin':
            tau=math.log(30/5)/EliminationRate + InfusionPeriod
            #return tau 
        else:
             return None  # Return None for unsupported drugs   
        tau = Decimal(tau).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return tau
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating tau: {e}")
        print(traceback.format_exc())
        return None

