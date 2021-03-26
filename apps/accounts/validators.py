from django.core.exceptions import ValidationError

def only_int(value):
    try:
        value.isdigit()==True
    except:
        raise ValidationError(_('This field only accepts numerical values.'), code='invalid_format')

def exp_date(value):
    try:
        x = value.split("/")
        if x[0].isdigit()==True and x[1].isdigit()==True:
            pass
        else:
            raise ValidationError(_('Please input in this format: MM/YY.'), code='invalid_format')
    except:
        raise ValidationError(_('Please input in this format: MM/YY.'), code='invalid_format')

