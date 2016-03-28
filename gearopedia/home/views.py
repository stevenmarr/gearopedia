from flask import render_template, request, flash, Blueprint
from flask import session as login_session
from oauth2client import client, crypt

from ..models import GearCategories
from gearopedia import app, db

# import db.db_session as session

session = db.session
CLIENT_ID = app.config['CLIENT_ID']

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


@home_blueprint.route('/')
def default():
    """Render home page."""
    categories = session.query(GearCategories).all()
    return render_template('default.html',
                           title="Categories",
                           categories=categories,
                           login_session=login_session,
                           page_title='Categories',
                           CLIENT_ID=CLIENT_ID)


# Login/Logout Handlers
@home_blueprint.route('/tokensignin', methods=['POST'])
def tokensignin():
    """Login user if valid id_token exists in request."""
    token = request.form['idtoken']
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Login Failed")
    login_session['user_id'] = idinfo['sub']
    login_session['name'] = idinfo['name']
    login_session['provider'] = "Google"
    if 'picture' in idinfo:
        login_session['picture'] = idinfo['picture']
    else:
        login_session['picture'] = "https://upload.wikimedia.org/wikipedia/commons/7/70/User_icon_BLACK-01.png"
    response = "Login Success"
    return response


@home_blueprint.route('/tokensignout', methods=['POST'])
def tokensignout():
    """Logout user if valid id_token exists in request."""
    token = request.form['idtoken']
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Logout Failed")
    del login_session['user_id']
    del login_session['name']
    del login_session['picture']
    del login_session['provider']
    response = "Logout Success"
    session.close()
    return response

# Error Handlers


@home_blueprint.errorhandler(400)
def not_found_error(error):
    flash('PAGE NOT FOUND')
    return render_template('404.html', login_session=login_session), 404


@home_blueprint.errorhandler(404)
def not_found_error(error):
    flash('PAGE NOT FOUND')
    return render_template('404.html', login_session=login_session), 404


@app.errorhandler(500)
def internal_error(error):
    session.rollback()
    flash('SOMETHING BROKE!')
    return render_template('500.html', login_session=login_session), 500
