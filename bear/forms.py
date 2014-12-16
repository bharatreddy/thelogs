from import Form, TextField, TextAreaField, SubmitField
 
class RegistrationForm(Form):
  name = TextField("Name")
  email = TextField("Email")
  subject = TextField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")