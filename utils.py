import re 
def validate_email(email, domain  = None):
    if domain:
        regex = r'\b[A-Za-z0-9._%+-]+@'+re.escape(domain)
        return True if re.fullmatch(regex,email) else False
    
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if re.fullmatch(regex,email) else False