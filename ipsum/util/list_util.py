
def list_equals(left_list, rigth_list, validate_order=True):

    if left_list == rigth_list:
        return True

    if not validate_order:
        for l in left_list: 
            if not l in rigth_list:
                return False

        for r in rigth_list:
            if r not in left_list:
                return False
        
        return True

    return False