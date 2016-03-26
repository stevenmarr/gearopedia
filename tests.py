#!venv/bin/python
import os
import unittest
from cStringIO import StringIO
from mock import patch
from coverage import coverage


#os.environ['APP_CONFIG'] = '/var/www/gearopedia/config/production.py'
os.environ['APP_CONFIG'] = 'config.TestingConfig'

from gearopedia import app, db, views
from gearopedia.models import GearModels

from flask import session as login_session
from flask import url_for
from flask.ext.testing import TestCase

session = db.session
BASE_DIR = app.config['BASE_DIR']


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
   
    def test_addgearcategory(self):
        response = self.add_category()
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

    def add_category(self):
        with patch.dict(login_session, {'name': 'tester'}):
            return(self.client.post('add_category/', 
                                    data={'name': 'Category - Test'}, 
                                    follow_redirects=True))

    def add_models(self):
        self.add_category()
        return(self.client.post(url_for('addmodel', category_id = 1),
                                        data=dict(manufacturer='test_name%s' % '_test',
                                        name='test_name%s' % '_test',
                                        description='test_name%s' % '_test',
                                        product_url='http://www.example.com',
                                        file_type='0',
                                        file=(StringIO("test_text_file"), 'test.txt'),
                                        image=(StringIO("png_string"), 'test.png')),
                                        follow_redirects=True))

    def test_add_models(self):
        response = self.add_models()
        assert 'New model created' in response.data
    
    def test_JSON_response(self):
        self.add_models()
        response = self.client.get(url_for('json_call'))

        assert 'test_name_test' in response.data

    def test_edit_models(self):
        pass
       

if __name__ == "__main__":
    cov = coverage(branch=True, omit=['venv/*', 'tests.py'])
    cov.start()
    suite = unittest.TestLoader().loadTestsFromTestCase(BaseTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    cov.stop()
    cov.save()
    print("HTML version: " + os.path.join(BASE_DIR, "tmp/coverage/index.html"))
    cov.html_report(directory=os.path.join(BASE_DIR, "tmp/coverage/index.html"))
    cov.erase()
