
def is_string_float(value:str):
    
    try:
        if type(value) is bool:
            return False
        
        else :
            float(value)
            

    except ValueError:
        return False

    else:
        return True