import re
from sqlalchemy import exc
from sqlalchemy import or_
from sqlalchemy import func
import logging
from scipy import stats
from datetime import datetime
from time import sleep
from time import strptime
from time import strftime
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker,undefer
from sqlalchemy import create_engine
from sqlalchemy import Date, cast

from datetime import date
from classes.Documento import Documento,Base
from multiprocessing import Pool,cpu_count,Lock
from modules import parser
from math import ceil
import itertools
import os
import random

logger = logging.getLogger('db_worker')
CHUNK_SIZE=7000

db_url = os.environ['panadata_db']
logger.info('loading %s', db_url)

def query_chunks(q, n):
  """ Yield successive n-sized chunks from query object."""
  for i in range(0, q.count(), n):
    yield list(itertools.islice(q, 0, n))

def chunks(l, n):
    """ return n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_all_controls(session):
    try:
        controls = list(zip(*session.query(Documento.control).all()))[0]
        session.close()
        return {item.lower() for item in controls}
    except:
        session.close()
        return set()

def create_documento(documento,session):
    c = documento.control
    try:
        session.add(documento)
        #logger.info('got new documento %s', documento.numero)
        session.commit()
        session.expunge(documento)
    except exc.IntegrityError as e:
        session.rollback()
    except Exception as e:
        print(e)
    return c

def create_documentos(documentos,session):
    for doc in documentos:
        try:
            session.add(documento)
            #logger.info('got new documento %s', documento.numero)
            session.commit()
            session.expunge(documento)
        except Exception as e:
            #logger.error(e)
            session.rollback()
        finally:
            session.close()
    return documentos
