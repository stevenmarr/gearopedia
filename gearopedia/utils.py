import os

from flask import url_for, flash, redirect, session
from flask import session as login_session
from functools import wraps

from gearopedia import app

def login_required(f):
    """Decorator for checking login state, or testing enviroment"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in login_session:
            return f(*args, **kwargs)
        elif app.config['TESTING']:
            session['name'] = "tester"
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('home.default'))
    return wrap