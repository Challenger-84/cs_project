import random

def generate_otp():
    otp = ''

    for i in range(4):
        otp = otp + str(random.randint(0, 9))
    
    return otp