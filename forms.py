from wtforms import Form, BooleanField, TextField, validators, ValidationError

class PhoneNumberForm(Form):
	phone_number = TextField('Enter a 10 digit phone number', [validators.Length(min=10, max=10)])
	name = TextField('Enter your first name')
    
	def getNumber(self):
		return self.phone_number

	def getName(self):
		return self.name