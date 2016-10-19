# -*- coding: UTF-8 -*-
from lemmes import Lemmatizer
import logging


# logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
  L = Lemmatizer()
  print(repr(L.lemmatize_sent(u'Hola Bienvenidos a Lemmes!, diviértete', merge=True)))
  print(repr(L.lemmatize_sent(u'hallan desechos hospitalarios en botadero', merge=True)))
  print(repr(L.lemmatize_sent(u'ahora tu estas conmigo asi que vivamos el presentee', merge=True)))
  print(repr(L.lemmatize_sent(u'los borraste o los descargaste a un .zip y backup? se pueden bajar carpetas independientes del gmail automáticamente.', merge=True)))
  print(repr(L.lemmatize(u'extraordinarios')))
  print(repr(L.lemmatize(u'extraterritoriales')))
  print(repr(L.lemmatize(u'extrañezas')))
  print(repr(L.lemmatize(u'extorsiones')))
  print(repr(L.lemmatize(u'extorsionadores')))
  print(repr(L.lemmatize(u'extenuantemente')))
  print(repr(L.lemmatize(u'ayen')))
  print(repr(L.lemmatize(u'hallar')))
  print(repr(L.lemmatize(u'hall')))
  print(repr(L.lemmatize(u'causita')))
  print(repr(L.lemmatize(u'borrachines')))
