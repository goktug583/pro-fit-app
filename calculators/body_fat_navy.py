import math

def calc_navy_body_fat(waist, neck, height, gender):
   
    height_cm = height * 100
    
    if gender.lower() == 'male':
        
        if waist - neck <= 0:
            return 0 
            
        log_waist_neck = math.log10(waist - neck)
        log_height = math.log10(height_cm)
        
        body_fat = 495 / (1.0324 - 0.19077 * log_waist_neck + 0.15456 * log_height) - 450
    else:
        return 0 

    return max(0, body_fat)