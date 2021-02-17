from django.core.exceptions import ValidationError

def only_int(value):
    try:
        value.isdigit()==True
    except:
        raise ValidationError('This field only accepts numerical values.')

def exp_date(value):
    try:
        x = value.split("/")
        if x[0].isdigit()==True and x[1].isdigit()==True:
            pass
        else:
            raise ValidationError('Please input in this format: MM/YY.')            
    except:
        raise ValidationError('Please input in this format: MM/YY.')