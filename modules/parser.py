import random
import unittest
from bs4 import BeautifulSoup,SoupStrainer
from classes.Documento import Documento
from itertools import chain
from decimal import Decimal
from datetime import datetime
import urllib3
import re
from time import sleep

def get_office_ids(soup):
    options = soup.find(id='ctl00_contenidoArriba_ddlOficinas').find_all('option')
    return [int(o['value'].strip()) for o in options if o['value'].strip() != '%']

def get_documento_types(soup):
    options = soup.find(id='ctl00_contenidoArriba_ddlDocumento').find_all('option')
    return [o['value'].strip() for o in options if o['value'].strip() != '%']

def get_view_state(soup):
    vs = soup.find(id='__VIEWSTATE')['value'].strip()
    return vs

def get_event_validation(soup):
    ev = soup.find(id='__EVENTVALIDATION')['value'].strip()
    return ev

def has_pages(soup):
    if soup.find(class_='pager-row'):
        return True
    else:
        return False

def replace_spanish_month(string):
    string = re.sub(r'ENE', '01',string)
    string = re.sub(r'FEB', '02',string)
    string = re.sub(r'MAR', '03',string)
    string = re.sub(r'ABR', '04',string)
    string = re.sub(r'MAY', '05',string)
    string = re.sub(r'JUN', '06',string)
    string = re.sub(r'JUL', '07',string)
    string = re.sub(r'AGO', '08',string)
    string = re.sub(r'SEP', '09',string)
    string = re.sub(r'OCT', '10',string)
    string = re.sub(r'NOV', '11',string)
    string = re.sub(r'DIC', '12',string)
    return string

def parse_fecha(fecha):
  try:
    fecha = fecha.replace('.','').upper()
    fecha = replace_spanish_month(fecha)
    fecha = datetime.strptime(fecha,"%d-%m-%y %I:%M %p")
  except Exception as e:
#    logger.error("%s", e)
#    logger.error('error parsing fecha %s', fecha)
    fecha = None
  return fecha

def parse_monto(monto):
  monto = re.sub(r'[^\d.]', '',monto) #remove non digits
  monto = re.sub(r'^.', '',monto) #remove leading period
  if not monto == "":
    monto = Decimal(monto)
  else:
    monto = Decimal(0)
  return monto

def sanitize(string):
  return str(re.sub(' +',' ', string)).lower() #no repeated spaces


def get_documentos(soup):
   docs = chain(soup.select('.row'),soup.select('.alternaterow'))
   docs = [filter(lambda x: x != None and x != '',[s.next_element.string.strip() if s.next_element.string != None else s.next_element.next_element.next_element.string for s in d]) for d in docs]
   return parse_documentos(docs)

def parse_documento_dict(doc_dict):
    for k,v in doc_dict.items():
        if k == 'monto':
            doc_dict[k] = parse_monto(v)
        elif k == 'fecha':
            doc_dict[k] = parse_fecha(v)
    return Documento(doc_dict)


def parse_documentos(documento_list):
  keys = ['control','institucion','documento','numero','favor','monto','estado','fecha']
  return [parse_documento_dict({ k:v for k,v in zip(keys,doc) }) for doc in documento_list]
