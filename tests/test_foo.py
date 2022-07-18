from unittest import TestCase
from foo import Foo

class TestFoo(TestCase):

    def test_say(self):
        self.assertEqual(Foo().say(), 'foo')