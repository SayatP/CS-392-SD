
def validate_string_as_number(s):
    try:
        int(s)
    except Exception:
        return False
    return True
