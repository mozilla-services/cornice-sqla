import unittest
from cornicedb.tests.wsgiapp import main
from webtest import TestApp
import json
import os


class TestMetaDB(unittest.TestCase):

    def setUp(self):
        app = main({})
        self.app = TestApp(app)

    def tearDown(self):
        # XXX do better ;later
        os.remove('/tmp/cornice.db')

    def test_def(self):
        # let's create a user
        self.app.put('/users/1', params=json.dumps({'name': 'tarek'}))

        # let's see what we have now
        user = json.loads(self.app.get('/users/1').body)
        self.assertEqual(user['item']['id'], 1)
        self.assertEqual(user['item']['name'], 'tarek')
