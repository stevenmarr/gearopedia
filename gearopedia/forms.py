from wtforms import StringField, validators, SelectField, FileField, BooleanField

from flask.ext.wtf import Form

FILE_TYPE = {
    '0': '-',
    '1': 'Owners Manual',
    '2': 'Service Manual',
    '3': 'Firmware',
    '4': 'Software',
    '5': 'Other',
}


class LoginForm(Form):
    openid = StringField('openid', validators=[validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class AddCategoryForm(Form):
    """Form for adding new categories"""

    name = StringField(u'Name', [validators.DataRequired(),
                       validators.Length(1, 80)])


class ModelForm(Form):
    """Form for addig new gear models"""

    manufacturer = StringField(u'Manufacturer', [validators.DataRequired(),
                               validators.Length(1, 80)])
    name = StringField('Model', [validators.DataRequired(),
                       validators.Length(2, 80)])
    description = StringField(u'Description', [validators.Length(0,
                              800)])
    product_url = StringField(u'Website', [validators.Optional(),
                              validators.Length(14, 2084),
                              validators.URL(require_tld=False,
                              message='Invalid URL')])
    image = FileField(u'Image File', [validators.Optional()])

    file = FileField(u'File', [validators.Optional()])

    file_type = SelectField(u'File type', [validators.Optional()], choices=[(key,
                            FILE_TYPE[key]) for key in FILE_TYPE.keys()], default='0')
