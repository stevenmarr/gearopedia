#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtforms import Form, BooleanField, StringField, validators, \
    TextField, PasswordField, DateField, SelectField, FileField
from wtforms.widgets.core import Select
from wtforms import widgets
import re

from setting import FILE_TYPE


class AddCategoryForm(Form):

    name = StringField(u'Name', [validators.Required(),
                       validators.Length(1, 20)])
    description = StringField(u'Description', [validators.Optional(),
                              validators.Length(0, 800)])


class ModelForm(Form):

    manufacturer = StringField(u'Manufacturer', [validators.Required(),
                               validators.Length(1, 80)])
    name = StringField('Model', [validators.Required(),
                       validators.Length(3, 80)])
    description = StringField(u'Description', [validators.Length(0,
                              800)])
    product_url = StringField(u'Website', [validators.Optional(),
                              validators.URL(require_tld=False,
                              message='Invalid URL')])
    image = FileField(u'Image File', [validators.Optional()])

    file = FileField(u'File', [validators.Optional()])

    file_type = SelectField(u'File type', choices=[(key,
                            FILE_TYPE[key]) for key in
                            FILE_TYPE.keys()])
