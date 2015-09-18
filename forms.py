#!/usr/bin/python

from wtforms import Form, StringField, validators, SelectField, FileField


from setting import FILE_TYPE


class AddCategoryForm(Form):

    name = StringField(u'Name', [validators.DataRequired(),
                       validators.Length(1, 20)])


class ModelForm(Form):

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
