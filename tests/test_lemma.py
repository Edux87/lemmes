# -*- coding: UTF-8 -*-
from nose.tools import assert_equals, assert_true
from unittest import TestCase
from lemmes import Lemmatizer


class LemmaTest(TestCase):
    @classmethod
    def test_lemmatize(self):
        L = Lemmatizer()
        w = u'circunstancialmente'
        assert_true(isinstance(L.lemmatize(w), unicode))
