#!/usr/bin/env python

import os
import cPickle
from bisect import bisect_left, bisect_right


class KeyColumnValueStore(object):

    def __init__(self, path=None):

        """
        initiate the data store.
        if path provided then persist to disk
        else use memory only.

        """

        self.store = {}
        self.persist = False

        if path:
            self.path = path
            self.persist = True
            self.load_file()

    def load_file(self):

        """ load the data store from disk """

        if (os.path.isfile(self.path)):
            file = open(self.path, 'r+')
            data = cPickle.loads(file.read())
            file.close()

            if data.keys():
                self.store = data

    def write_file(self):

        """ write the data store to disk """

        file = open(self.path, 'w+')
        file.write(cPickle.dumps(self.store))
        file.close()

    def _persists(fn):

        """ decorator for persitant storage """

        def wrapper(self, *args, **kwargs):

            fn(self, *args, **kwargs)

            if self.persist:
                self.write_file()

        return wrapper

    @_persists
    def set(self, key, col, val):

        """ sets the value at the given key/column """

        columns = self.get_key(key)

        if columns:

            columns.sort(key=lambda r: r[0])
            column_keys = [r[0] for r in columns]
            index = bisect_left(column_keys, col)

            if index != len(columns):

                if column_keys[index] == col:
                    columns[index] = (col, val)

                else:
                    columns.insert(index, (col, val))

            else:
                columns.append((col, val))

        else:
            columns.insert(0, (col, val))

        self.store[key] = columns

    def get(self, key, col):

        """ return the value at the specified key/column """

        columns = self.get_key(key)

        if columns:

            for i, v in enumerate(columns):

                if v[0] == col:
                    return columns[i][1]

        return None

    def get_key(self, key):

        """ returns a sorted list of column/value tuples """

        if key in self.get_keys():
            return self.store[key]

        else:
            return []

    def get_keys(self):

        """ returns a set containing all of the keys in the store """

        return self.store.keys()

    def get_slice(self, key, start, stop):

        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction

        """

        columns = self.get_key(key)
        column_keys = [r[0] for r in columns]

        if start:
            start = bisect_left(column_keys, start)

        if stop:
            stop = bisect_right(column_keys, stop)

        return columns[start:stop]

    @_persists
    def delete(self, key, col):

        """ removes a column/value from the given key """

        columns = self.get_key(key)

        if columns:
            column_keys = [r[0] for r in columns]
            del columns[bisect_left(column_keys, col)]

    @_persists
    def delete_key(self, key):

        """ removes all data associated with the given key """

        if key in self.get_keys():
            del self.store[key]
