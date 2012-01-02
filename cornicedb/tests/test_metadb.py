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
        self.app.post('/users/1', params=json.dumps({'name': 'tarek'}))

        # the user already exists
        self.app.post('/users/1', params=json.dumps({'name': 'tarek'}),
                      status=400)

        # let's see what we have now
        user = json.loads(self.app.get('/users/1').body)
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['name'], 'tarek')

        # let's kill the user
        self.app.delete('/users/1')
        self.app.get('/users/1', status=404)

        self.app.delete('/users/1', status=404)

        # we can also put for updates the root
        self.app.put('/users/1', params=json.dumps({'name': 'tarek'}))
        user = json.loads(self.app.get('/users/1').body)
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['name'], 'tarek')

        self.app.put('/users/1', params=json.dumps({'name': 'tarek2'}))
        user = json.loads(self.app.get('/users/1').body)
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['name'], 'tarek2')
