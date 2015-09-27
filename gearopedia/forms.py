#!/usr/bin/python
from datetime import timedelta

from wtforms import Form, StringField, validators, SelectField, FileField
from wtforms.ext.csrf.session import SessionSecureForm
from gearopedia import app

class BaseForm(SessionSecureForm):
    SECRET_KEY = app.config['SECRET_KEY']
    TIME_LIMIT = timedelta(minutes=20)  

class AddCategoryForm(BaseForm):

    name = StringField(u'Name', [validators.DataRequired(),
                       validators.Length(1, 20)])


class ModelForm(BaseForm):

    manufacturer = StringField(u'Manufacturer', [validators.DataRequired(),
                               validators.Length(1, 80)])
    name = StringField('Model', [validators.DataRequired(),
                       validators.Length(3, 80)])
    description = StringField(u'Description', [validators.Length(0,
                              800)])
    product_url = StringField(u'Website', [validators.Optional(),
                              validators.URL(require_tld=False,
                              message='Invalid URL')])
    image = FileField(u'Image File', [validators.Optional()])

    file = FileField(u'File', [validators.Optional()])

    file_type = SelectField(u'File type', choices=[(key,
                            app.config['FILE_TYPE'][key]) for key in app.config['FILE_TYPE'].keys()])
