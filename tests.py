#!/usr/bin/env python

import os
import json
import unittest
from keycolumnvalue import KeyColumnValueStore
import rest_app


class TestKeyColumnValue(unittest.TestCase):

    def setUp(self):

        self.store = KeyColumnValueStore()

        self.store.set('a', 'aa', 'x')

        self.store.set('a', 'ab', 'x')

        self.store.set('c', 'cc', 'x')

        self.store.set('c', 'cd', 'x')

        self.store.set('d', 'de', 'x')

        self.store.set('d', 'df', 'x')


    def test_get(self):

        self.assertEqual(self.store.get('a', 'aa'), 'x')


    def test_get_key(self):

        self.assertEqual(self.store.get_key('a'), [('aa', 'x'), ('ab', 'x')])


    def test_get_none(self):

        self.assertEqual(self.store.get('z', 'yy'), None)
    
    
    def test_get_key_none(self):

        self.assertEqual(self.store.get_key('z'), [])


    def test_overwrite(self):

        # if we set different values on the 'a' key:

        self.store.set('a', 'aa', 'y')

        self.store.set('a', 'ab', 'z')

        # the statements below will evaluate to True

        self.assertEqual(self.store.get('a', 'aa'), 'y')

        self.assertEqual(self.store.get_key('a'), [('aa', 'y'), ('ab', 'z')])


    def test_delete_column(self):

        self.store.delete('d', 'df')

        self.assertEqual(self.store.get_key('d'),  [('de', 'x')])

    
    def test_delete_key(self):

        self.store.delete_key('c')

        self.assertEqual(self.store.get_key('c'), [])


    def test_slice(self):

        # set additional data for slice test 

        self.store.set('a', 'ac', 'x')

        self.store.set('a', 'ad', 'x')

        self.store.set('a', 'ae', 'x')

        self.store.set('a', 'af', 'x')

        self.store.set('a', 'ag', 'x')

        self.assertEqual(
            self.store.get_slice('a', 'ac', 'ae'), 
            [('ac', 'x'), ('ad', 'x'), ('ae', 'x')]
        )
        
        self.assertEqual(
            self.store.get_slice('a', 'ae', None),
            [('ae', 'x'), ('af', 'x'), ('ag', 'x')]
        )
        
        self.assertEqual(
            self.store.get_slice('a', None, 'ac'),
            [('aa', 'x'), ('ab', 'x'), ('ac', 'x')]
        )


class TestKeyColumnValuePersist(unittest.TestCase):

    def setUp(self):

        self.persistent_datastore = 'foo.db'

    def tearDown(self):

        # remove file 

        if (os.path.isfile(self.persistent_datastore)):

            os.remove(self.persistent_datastore)

    def test_write_file(self):
        
        self.assertEqual(os.path.isfile(self.persistent_datastore), False)

        self.store = KeyColumnValueStore(path=self.persistent_datastore)

        self.store.set('a', 'aa', 'x')

        # check file has been created

        self.assertEqual(os.path.isfile(self.persistent_datastore), True)


    def test_read_file(self):

        # load a sample data file

        self.store = KeyColumnValueStore(path='fixture.db')

        self.assertEqual(self.store.get('a', 'aa'), 'x')

        self.assertEqual(self.store.get_key('a'), [('aa', 'x'), ('ab', 'x')])


class TestRESTApp(unittest.TestCase):

    def setUp(self):

        rest_app.app.config['TESTING'] = True

        self.app = rest_app.app.test_client()

    def test_api_get_keys(self):

        res = self.app.get('/api/v1/keys')

        self.assertEqual(json.loads(res.data), json.loads('{"keys": ["a", "c"]}'))

    def test_api_get_key(self):

        res = self.app.get('/api/v1/keys/a')

        self.assertEqual(json.loads(res.data), json.loads('{"columns": [["aa", "Hello"], ["ab", "x"]]}'))

    def test_api_get(self):

        res = self.app.get('/api/v1/keys/a/aa')

        self.assertEqual(json.loads(res.data), json.loads('{"val": "Hello"}'))


test_classes = [TestKeyColumnValue, TestKeyColumnValuePersist, TestRESTApp]

loader = unittest.TestLoader()

suite_list = []

for test_class in test_classes:

    suite = loader.loadTestsFromTestCase(test_class)

    suite_list.append(suite)

all_tests = unittest.TestSuite(suite_list)

unittest.TextTestRunner(verbosity=2).run(all_tests)
