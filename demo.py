# -*- coding: UTF-8 -*-
from lemmes import Lemmatizer
import logging


logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
  L = Lemmatizer()
  # L.create_lemmas()
  print(repr(L.lemmatize_sent(u'en los almacenes del callao a continuacion se detallan articulo', merge=True)))
