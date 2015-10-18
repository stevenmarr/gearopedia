#!flask/bin/python
import os
import unittest
from cStringIO import StringIO

from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()


from gearopedia import app, db, views
from gearopedia.models import GearModels

from flask import session as login_session
from flask import url_for
from flask.ext.testing import TestCase

session = db.session
BASE_DIR = app.config['BASE_DIR']

os.environ['APP_CONFIG'] = '/var/www/gearopedia/config/production.py'


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(BASE_DIR, 'test.db')
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_addgearcategory(self):
        response = self.client.post('add_category/', 
                                    data={'name': 'Category - Test'}, 
                                    follow_redirects=True)
        assert 'New category added' in response.data

    def test_default_response(self):
        self.test_addgearcategory()
        response = self.client.get('/')
        assert 'Category - Test' in response.data

    def test_deletegearcategory(self):
        self.test_addgearcategory()
        response = self.client.post(url_for('deletegearcategory', category_id=1),
                                    follow_redirects=True)
        assert 'deleted' in response.data

    def test_add_models(self):
        self.test_addgearcategory()
        for x in range(1):
            response = self.client.post(url_for('addmodel', category_id = 1),
                                        data=dict(manufacturer='test_name%s' % x,
                                        name='test_name%s' % x,
                                        description='test_name%s' % x,
                                        product_url='http://www.example.com',
                                        file_type='0',
                                        file=(StringIO("hi everyone"), 'test.txt'),
                                        image=(StringIO("hi everyone"), 'test.png')),
                                        follow_redirects=True)
            # print response.data
            assert 'New model created' in response.data
    

    '''def test_view_model(self):
        rv = self.app.get('/view_model/1', follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data'''
        
if __name__ == '__main__':
    unittest.main()
    cov.stop()
    cov.save()
    print('\n\nCoverage Report:\n')
    cov.report()
    print("HTML version: " + os.path.join(BASE_DIR, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
