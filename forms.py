from wtforms import Form, TextField 
#TODO: from wtforms import validators, ValidationError

class PhoneNumberForm(Form):
    phone_number = TextField('Enter a 10 digit phone number')
    
    def getNumber(self):
    	return self.phone_number

#TODO: check to make sure it is a valid phone number and if not change it into