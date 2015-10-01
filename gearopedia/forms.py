#!/usr/bin/python


from datetime import timedelta

from wtforms import Form, StringField, validators, SelectField, FileField
from wtforms.ext.csrf.session import SessionSecureForm
from gearopedia import app

FILE_TYPE = {
    '0': '-',
    '1': 'Owners Manual',
    '2': 'Service Manual',
    '3': 'Firmware',
    '4': 'Software',
    '5': 'Other',
}


class BaseForm(SessionSecureForm):
    """Base form, implements CSRF"""

    SECRET_KEY = app.config['SECRET_KEY']
    TIME_LIMIT = timedelta(minutes=20)  


class AddCategoryForm(BaseForm):
    """Form for adding new categories"""

    name = StringField(u'Name', [validators.DataRequired(),
                       validators.Length(1, 20)])


class ModelForm(BaseForm):
    """Form for addig new gear models"""

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
                            FILE_TYPE[key]) for key in FILE_TYPE.keys()])
