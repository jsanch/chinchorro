from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Sequence, Boolean, Numeric, DateTime
from sqlalchemy.orm import deferred
from sqlalchemy.types import Unicode, UnicodeText
from datetime import datetime

Base = declarative_base()
class Documento(Base):
  __tablename__ = 'documentos'


  id = Column(Integer, primary_key=True)
  control = Column(Unicode, unique=True)
  institucion = Column(Unicode)
  documento = Column(Unicode)
  numero = Column(Unicode)
  favor = Column(Unicode)
  estado = Column(Unicode)
  monto = Column(Numeric(15,2))
  html = deferred(Column(UnicodeText))
  fecha = Column(DateTime)
  created_at = Column(Date, default=datetime.now)
  updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)

  def __init__(self, kwargs):
    self.html = None
    for k in  kwargs.keys():
        self.__setattr__(k, kwargs[k])

  def __hash__(self):
    return hash(self.control)

  def __eq__(self, other):
    return self.control == other.control

  def __getitem__(self,key):
    return getattr(self, key)

  def __str__(self):
    return "<Documento %s>" % (self.control)

  def __repr__(self):
    return "<Documento %s>" % (self.control)
