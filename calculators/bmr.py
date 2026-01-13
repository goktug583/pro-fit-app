def calc_bmr(weight, height, age, gender):
    
    
    height_cm = height * 100
    
    
    if gender.lower() == 'male': 
        
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
        
    else: 
        
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    
    return bmr
