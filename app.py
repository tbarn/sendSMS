import os

from flask import Flask
from flask import render_template
from flask import request

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient 

from keen.client import KeenClient

from forms import PhoneNumberForm

app = Flask(__name__)
app.config.from_pyfile('local_settings.py')

client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

keen = KeenClient(app.config['KEEN_PROJECT_ID'], app.config['KEEN_WRITE_KEY'], app.config['KEEN_READ_KEY'])

@app.route('/', methods=['GET', 'POST'])
def index():
	form = PhoneNumberForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			#TODO: Create different cases for types of messages, will also need to change index.html
			client.messages.create(body="Hello " + form.getName().data + "!",
				from_=app.config['TWILIO_CALLER_ID'], to="+1" + form.getNumber().data)
		except TwilioRestException as e:
			print e 
			form.phone_number.errors = [unicode(e.msg)]
			return render_template('index.html', form=form)
		params = {'phone_number': request.form['phone_number']}
		keen.add_event("text_message", { "message_sent": True })
		return render_template('success.html', params=params)
	else: 
		form = PhoneNumberForm()
	return render_template('index.html', form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    if port == 5000:
    	app.debug = True
    app.run(host='0.0.0.0', port=port)
