import traceback
import math, decimal
from decimal import Decimal, ROUND_HALF_UP

def bsa(weight, height):
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
        elif age < 18 and height <22:
            lbw = weight
        elif age < 18 and height < 48: #lener, Peck, Brown, Perlin Formula 
            lbw = (-59.6035 + (5.2878*height) -(0.123939*(height**2))+ (0.00128936*(height**3)) )/2.2
        if sex=='F':
            if age >=18:
                lbw = 45.5 + 2.3*(height-60)
        elif age < 18 and height < 22:
            lbw = weight
        elif age < 18 and height < 48:
            lbw =(-77.55796 + (6.93728*height) -(0.171703*(height**2)) +(0.001726*(height**3)))/2.2
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
                crcl = 0.85*(140 - age) * lbw / (72 * scr)
            elif age < 2:
                crcl = 0.45*height*2.54*bsa/(scr*1.73)
            elif age >=2 and age <13:
                crcl = 0.55*height*2.54*bsa/(scr*1.73)
            elif age >=13 and age <18:
                crcl = 0.55*height*2.54*bsa/(scr*1.73)
        # Round the Creatinine Clearance (CrCl) to 2 decimal places
        crcl = Decimal(crcl).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return crcl  # Return the calculated Creatinine Clearance (CrCl)
    except (TypeError, ValueError, ZeroDivisionError) as e:
         # Log the error or handle it as needed
        print(f"Error calculating Creatinine Clearance: {e}")
        print(traceback.format_exc())
        return None
        