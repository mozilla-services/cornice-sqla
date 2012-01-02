import unittest
from cornicesqla.tests.wsgiapp import main
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

        self.app.put('/users/2', params=json.dumps({'name': 'bill'}))

        res = self.app.get('/users')
        users = json.loads(res.body)
        self.assertEqual(len(users['items']), 2)

        # let's try some collection calls
        bob = {'name': 'bob'}
        sarah = {'name': 'sarah'}

        res = self.app.put('/users', params=json.dumps([bob, sarah]))
        res = json.loads(res.body)
        self.assertEqual(res['ids'], [1, 2])

        res = json.loads(self.app.delete('/users').body)
        self.assertEqual(res['deleted'], 2)

        res = self.app.put('/users', params=json.dumps([bob, sarah]))
        res = json.loads(res.body)
        self.assertEqual(res['ids'], [1, 2])

        bill = {'name': 'bill'}
        sarah = {'name': 'sarah2'}
        res = self.app.post('/users', params=json.dumps([bill, sarah]))
        res = json.loads(res.body)
        self.assertEqual(res['ids'], [3, 4])

        res = json.loads(self.app.get('/users/4').body)
        self.assertEquals(res['name'], 'sarah2')

        self.app.post('/users', params=json.dumps([bill]))

        res = json.loads(self.app.get('/users').body)
        self.assertEquals(len(res['items']), 5)
