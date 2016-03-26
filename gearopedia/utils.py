import os

from flask import url_for, flash, redirect
from flask import session as login_session
from functools import wraps


def login_required(f):
    """Decorator for checking login state, or testing enviroment"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in login_session:
            return f(*args, **kwargs)
        elif os.environ['APP_CONFIG'] == 'config.TestingConfig':
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('default'))
    return wrap