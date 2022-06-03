
def is_string_int(value:str):
    
    try:
        if type(value) is bool:
            return False

        else :
            int(value)

    except ValueError:
        return False

    else:
        return True

