import os

from flask import Flask
from flask import render_template, request

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient 

from forms import PhoneNumberForm

app = Flask(__name__)

#TODO: Make config file

# Uncomment and fill out with your information
# sending_number = ""
# account_sid = ""
# auth_token  = ""

app.client = TwilioRestClient(account_sid, auth_token)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = PhoneNumberForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			#TODO: Create different cases for types of messages, will also need to change index.html
			app.client.sms.messages.create(body="Hello " + form.getName().data + "!",
				from_=sending_number, to="+1" + form.getNumber().data)
		except TwilioRestException as e:
			#TODO: Add more error handling
			 form.phone_number.errors = [unicode(e.msg)]
			 return render_template('index.html', form=form)
		params = {'phone_number': request.form['phone_number']}
		return render_template('success.html', params=params)
	else: 
		form = PhoneNumberForm()
	return render_template('index.html', form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
    	app.debug = True
    app.run(host='0.0.0.0', port=port)
