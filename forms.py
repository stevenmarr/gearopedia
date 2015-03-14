from wtforms import Form, BooleanField, StringField, validators, TextField, PasswordField, DateField, SelectField
from wtforms.widgets.core import Select
from wtforms import widgets

class AddCategoryForm(Form):
    name = StringField('Category Name',
                          [validators.Required(), validators.Length(1,20)])
    
class AddModelForm(Form):
	manufacturer = StringField('Manufacturer',
                         	[validators.Required(), validators.Length(4,80)])
	name = StringField('Model',
							[validators.Required(), validators.Length(3,80)])
	description = StringField('Description',
							[validators.Length(0,800)])
	product_url = StringField('Model Website',
							[validators.URL(require_tld=False, message='Invalid URL')])
	manual_url = StringField('Link to owners manual',
							[validators.Optional(),
							 validators.URL(require_tld=False, message='Invalid URL')])
	