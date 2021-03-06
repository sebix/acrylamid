# -*- coding: utf-8 -*-

import sys; reload(sys)
sys.setdefaultencoding('utf-8')

import shutil

try:
    import unittest2 as unittest
except ImportError:
    import unittest # NOQA

from acrylamid import log
from acrylamid.core import cache
from acrylamid import helpers
from acrylamid import AcrylamidException

class TestUtils(unittest.TestCase):

    def setUp(self):
        log.init('acrylamid', level=40)
        cache.init()

    def tearDown(self):
        shutil.rmtree(cache.cache_dir)

    def test_safeslug(self):

        examples = (('This is a Test', 'this-is-a-test'),
                    ('this is a test', 'this-is-a-test'),
                    ('This is another-- test', 'this-is-another-test'),
                    ('A real example: Hello World in C++ -- "a new approach*"!',
                     'a-real-example-hello-world-in-c++-a-new-approach'))

        for value, expected in examples:
            self.assertEqual(helpers.safeslug(value), expected)

        if not helpers.translitcodec:
            raise ImportError('this test requires `translitcodec`')

        examples = ((u'Hänsel und Gretel', 'haensel-und-gretel'),
                    (u'fácil € ☺', 'facil-eur'))

        for value, expected in examples:
            self.assertEqual(helpers.safeslug(value), expected)

        from unicodedata import normalize
        setattr(helpers, 'normalize', normalize)
        helpers.translitcodec = None
        self.assertEqual(helpers.safeslug(u'Hänsel und Gretel'), 'hansel-und-gretel')

    def test_joinurl(self):

        examples = ((['hello', 'world'], 'hello/world'),
                    (['/hello', 'world'], '/hello/world'),
                    (['hello', '/world'], 'hello/world'),
                    (['/hello', '/world'], '/hello/world'),
                    (['/hello/', '/world/'], '/hello/world/'))

        for value, expected in examples:
            self.assertEqual(helpers.joinurl(*value), expected)

    def test_expand(self):

        self.assertEqual(helpers.expand('/:foo/:bar/', {'foo': 1, 'bar': 2}), '/1/2/')
        self.assertEqual(helpers.expand('/:foo/:spam/', {'foo': 1, 'bar': 2}), '/1/:spam/')
        self.assertEqual(helpers.expand('/:foo/', {'bar': 2}), '/:foo/')

    def test_paginate(self):

        class X(str):
            # dummy class
            has_changed = True
            md5 = property(lambda x: str(hash(x)))

        res = ['1', 'asd', 'asd123', 'egg', 'spam', 'ham', '3.14', '42']
        res = [X(val) for val in res]

        # default stuff
        self.assertEqual(list(helpers.paginate(res, 4)),
            [((None, 1, 2), res[:4], True), ((1, 2, None), res[4:], True)])
        self.assertEqual(list(helpers.paginate(res, 4, lambda x: x.isdigit())),
            [((None, 1, None), [X('1'), X('42')], True), ])
        self.assertEqual(list(helpers.paginate(res, 7)),
            [((None, 1, 2), res[:7], True), ((1, 2, None), res[7:], True)])

        # with orphans
        self.assertEqual(list(helpers.paginate(res, 7, orphans=1)),
            [((None, 1, None), res, True)])
        self.assertEqual(list(helpers.paginate(res, 6, orphans=1)),
            [((None, 1, 2), res[:6], True), ((1, 2, None), res[6:], True)])

        # a real world example which has previously failed
        res = [X(_) for _ in range(20)]
        self.assertEqual(list(helpers.paginate(res, 10)),
            [((None, 1, 2), res[:10], True), ((1, 2, None), res[10:], True)])

        res = [X(_) for _ in range(21)]
        self.assertEqual(list(helpers.paginate(res, 10)),
            [((None, 1, 2), res[:10], True), ((1, 2, 3), res[10:20], True),
             ((2, 3, None), res[20:], True)])

        # edge cases
        self.assertEqual(list(helpers.paginate([], 2)), [])
        self.assertEqual(list(helpers.paginate([], 2, orphans=7)), [])
        self.assertEqual(list(helpers.paginate([X('1'), X('2'), X('3')], 3, orphans=1)),
            [((None, 1, None), [X('1'), X('2'), X('3')], True)])

    def test_escape(self):

        self.assertEqual(helpers.escape('Hello World'), 'Hello World')
        self.assertEqual(helpers.escape('Hello: World'), '"Hello: World"')
        self.assertEqual(helpers.escape('Hello\'s World'), '"Hello\'s World"')
        self.assertEqual(helpers.escape('Hello "World"'), "'Hello \"World\"'")

    @unittest.skipIf(sys.version_info < (2, 7), '')
    def test_system(self):

        examples = ((['echo', 'ham'], None, 'ham'),
                    ('bc', '1 + 1\n', '2'),
            )
        for cmd, stdin, expected in examples:
            self.assertEqual(helpers.system(cmd, stdin), expected)

        with self.assertRaises(AcrylamidException):
            helpers.system('bc', '1+1')
        with self.assertRaises(OSError):
            helpers.system('foo', None)
