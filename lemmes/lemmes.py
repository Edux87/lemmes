# -*- coding: UTF-8 -*-
import sys
import io
import config as cf
import numpy as np
import logging
from backports import csv
from itertools import groupby
from os.path import isfile, join, isdir
from os import path, popen, makedirs
import shutil
import unicodedata
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from pickle import dump, load
from nltk.tokenize import word_tokenize
import difflib
import string
import re


STR_PUNC = string.punctuation
STR_PUNC = str(string.punctuation).replace('@', '')
TRANS_PUNC = dict((ord(char), u' ') for char in STR_PUNC)

MAP_SPECIALS = dict((
    (ord(u'Á'), u'a'), (ord(u'É'), u'e'), (ord(u'Í'), u'i'),
    (ord(u'Ó'), u'o'), (ord(u'Ú'), u'u'), (ord(u'Ñ'), u'ñ'),
    (ord(u'À'), u'a'), (ord(u'È'), u'e'), (ord(u'Ì'), u'i'),
    (ord(u'Ò'), u'o'), (ord(u'Ù'), u'u'), (ord(u'@'), u'a'),
    (ord(u'á'), u'a'), (ord(u'é'), u'e'), (ord(u'í'), u'i'),
    (ord(u'ó'), u'o'), (ord(u'ú'), u'u'), (ord(u'ñ'), u'ñ'),
    (ord(u'à'), u'a'), (ord(u'è'), u'e'), (ord(u'ì'), u'i'),
    (ord(u'ò'), u'o'), (ord(u'ù'), u'u'), (ord(u'ü'), u'u')
))

class Lemmatizer:
  @classmethod
  def __init__(self):
    self.STEMMER = SnowballStemmer('spanish')
    self.STOPW = stopwords.words('spanish')
    self.LANG = cf.LANG
    self.LOG = logging.getLogger(__name__)
    if not isfile(cf.FILE_LEMMAS_BIN):
      self.create_lemmas()
    self.LOG.info('uncompress dict: ' + repr(cf.FILE_LEMMAS_BIN))
    self.DICTIONARY = self.uncompress(cf.FILE_LEMMAS_BIN)

  @classmethod
  def lemmatize_sent(self, sentence, stemm_unk=False, merge=False):
    sent = self.remove_nonchars(sentence.lower())
    tokens = [t for t in word_tokenize(sent) if t not in self.STOPW]
    words = []
    if len(tokens):
      for token in tokens:
        lemma = self.lemmatize(token)
        if lemma:
          if merge:
            if isinstance(lemma, list):
              for w in lemma:
                words.append(w)
            else:
              words.append(lemma)
          else:
            words.append(lemma)
      return words
    return False

  @classmethod
  def lemmatize(self, token, stemm_unk=False):
    if len(token):
      lemma = None
      self.LOG.info(token)
      stemmed = self.STEMMER.stem(token)
      lemmas = self.DICTIONARY.get(stemmed)
      self.LOG.info(token + ' lemmas: ' + repr(lemmas))
      self.LOG.info(token + ' stemm: ' + repr(stemmed))
      #
      # if not lemmas:
      #   stemmed = self.STEMMER.stem(stemmed)
      #   lemmas = self.DICTIONARY.get(stemmed)

      if lemmas:
        self.LOG.info(token + ' count lemmas ' + str(len(lemmas)))
        if len(lemmas) == 1:
          lemma = lemmas[0]
        else:
          if token in lemmas:
            self.LOG.info(token + ' token in lemma!')
            lemma = token
          else:
            temp_lemmas = {}
            temp_lemma = []

            for w in lemmas:
              temp_lemmas.update({self.convert_special_char(w): w})
            temp_lemmas_values = temp_lemmas.keys()
            for x in range(len(stemmed), len(token)):
              c = token[:x]
              temp_lemma.append(c)
              temp_lemma.append(c + 'o')
              temp_lemma.append(c + 'e')
              temp_lemma.append(c + 'es')
              temp_lemma.append(c + 'r')
              temp_lemma.append(c + 'er')
              temp_lemma.append(c + 'ar')

            # if stemmed in temp_lemma:
            #   del temp_lemma[temp_lemma.index(stemmed)]
            self.LOG.info(token + ' combinaciones: ' + repr(temp_lemma))

            lemma = []

            for x in temp_lemmas_values:
              if x in temp_lemma:
                lemma.append(temp_lemmas.get(x))
                self.LOG.info(token + ' no_tilde: ' + repr(x))

            if len(lemma) >= 2:
              aprox = difflib.get_close_matches(token, lemma, 2, .5)
              self.LOG.info(token + ' aprox: ' + repr(aprox))
              if aprox:
                lemma_score = []
                for a in aprox:
                  score = difflib.SequenceMatcher(None, token, a).ratio()
                  self.LOG.info(token + ' score aprox: ' + repr(a) + ' ' + repr(score))
                  if score >= .8:
                    lemma_score.append(a)
                if len(lemma_score):
                  lemma = lemma_score
            if len(lemma) == 0:
              lemma = token
      else:
        lemma = stemmed if stemm_unk else token
        self.LOG.info(token + ' not_exist!')
      self.LOG.info(token + ' lemma: ' + repr(lemma))
      if isinstance(lemma, list):
        if len(lemma) == 1:
          return lemma[0]
      return lemma
    return False

  @classmethod
  def create_lemmas(self):
    lemmas = []
    dictionary = {}
    # if not isfile(cf.SET_PATH_BIN_LEMMES)
    self.move_file()
    with io.open(cf.FILE_LEMMAS_CSV, 'r', encoding='utf-8') as flemma:
      reader = csv.reader(flemma)
      for row in reader:
          lemmas.append((row[0], row[1]))
    lemmas.sort()
    for stemm, stemms in groupby(lemmas, lambda x: x[0]):
      stemm_list = []
      for words in stemms:
        self.LOG.debug('Stemm: ' + stemm + ' | Word: ' + words[1])
        stemm_list.append(words[1])
      dictionary.update({stemm: stemm_list})

    self.compress(dictionary, cf.FILE_LEMMAS_BIN)
    self.LOG.info('Done!: ' + cf.FILE_LEMMAS_BIN)

  @staticmethod
  def uncompress(filename):
    output = open(filename, 'rb')
    return load(output)

  @staticmethod
  def compress(obj, filename):
    output = open(filename, 'wb')
    dump(obj, output)
    output.close()
    return filename

  @classmethod
  def remove_nonchars(self, text):
    if not len(text):
      return None
    text = self.is_unicode(text).translate(TRANS_PUNC)
    return text

  @staticmethod
  def convert_special_char(text):
    if not len(text):
      return None
    return text.translate(MAP_SPECIALS)

  @staticmethod
  def is_unicode(text):
    return text if isinstance(text, unicode) else unicode(text, 'utf8')

  @classmethod
  def move_file(self):
    lemmas = []
    dictionary = {}
    shutil.copy('data/' + cf.SOURCE_LEMMAS_CSV, cf.FILE_LEMMAS_CSV)

  @classmethod
  def generate(self):
    lemmas = []
    dictionary = {}
    shutil.copy('data/' + cf.SOURCE_LEMMAS_CSV, cf.FILE_LEMMAS_CSV)
    with io.open(cf.FILE_LEMMAS_CSV, 'r', encoding='utf-8') as flemma:
      for word in flemma:
        if word:
          word = self.is_unicode(word.rstrip('\r\n'))
          stemm = self.is_unicode(STEMMER.stem(word))
          lemmas.append([stemm, word])
      flemma.close()
    with io.open('data/' + cf.SOURCE_LEMMAS_CSV + '.x', 'w', encoding='utf-8') as f:
      w = csv.writer(f)
      for row in lemmas:
        w.writerow(row)
