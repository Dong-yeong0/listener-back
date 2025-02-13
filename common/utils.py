import re


def is_valid_email_format(email):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return False
    return True

def is_valid_password_strength(password):
    if not re.search('[a-z]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[@#$%^&+=]', password):
        return False
    return True

def is_valid_password_length(password):
    if len(password) < 8 or len(password) > 16:
        return False
    return True

def is_password_str_num_included(password):
    if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
        return False
    return True