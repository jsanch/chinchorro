from multiprocessing import Pool
from classes.Documento import Documento,Base
from sqlalchemy.orm import sessionmaker,undefer
from sqlalchemy import create_engine
from modules import parser,url_generator,db_worker
from bs4 import BeautifulSoup,SoupStrainer
import math
from random import shuffle
import re
import logging
from queue import Queue
import sys,os
import gc
sys.setrecursionlimit(10000)
import urllib3
import threading
from time import sleep
import asyncio
import aiohttp

logger = logging.getLogger('crawler')
url = 'http://190.34.178.19/Sicowebconsultas/buscar.aspx'
#office_ids = ['0035','624','001','145','055','003','016','017']
office_ids = ["202", "043", "624", "108", "001", "029", "114", "238", "234", "105", "047", "145", "022", "103", "203", "107", "109", "016015", "106", "055", "057", "204", "315", "330", "345", "600", "115", "208", "11018", "274", "360", "110", "212", "375", "521", "522", "311", "11004", "11014", "625", "623", "628", "058", "045", "611", "614", "612", "613", "615", "616", "617", "618", "610", "619", "031", "002", "053", "224", "621", "01702", "033", "111", "11005", "11006", "049", "041", "397", "063", "050", "060", "01703", "299", "704", "900", "198", "278", "699", "054", "701", "038", "039", "123", "052", "11015", "01232", "118", "124", "152", "266", "120", "137", "051", "125", "391", "0362", "270", "390", "130", "392", "023", "122", "151", "142", "140", "640", "643", "644", "639", "645", "641", "646", "642", "622", "638", "649", "635", "653", "652", "650", "647", "632", "636", "651", "633", "637", "648", "634", "620", "282", "0163", "016501", "010091", "008", "010", "021", "016", "007", "007041", "007061", "017", "003", "009", "012", "012021", "018", "013", "014", "020", "005", "629", "507", "525", "508", "569", "585", "570", "526", "541", "501", "527", "528", "529", "586", "587", "571", "597", "517", "572", "502", "543", "573", "574", "503", "547", "516", "580", "530", "531", "518", "532", "558", "524", "539", "545", "575", "588", "509", "548", "589", "559", "549", "560", "561", "584", "538", "590", "542", "510", "540", "546", "550", "511", "576", "551", "562", "512", "552", "544", "563", "519", "533", "534", "591", "596", "577", "535", "592", "536", "578", "593", "520", "553", "594", "595", "579", "537", "564", "146", "700", "028", "030", "135", "117", "037", "800", "999", "11003", "0181", "11011", "11008", "11009", "11010", "11012", "11007", "153", "11002", "133", "036", "01619", "0035", "01633", "148", "011", "703", "044", "134", "705", "226", "276", "056", "112", "0183", "119", "0182", "0184", "027", "01701", "655", "310", "121", "275", "026", "626", "702", "040", "193", "187", "190", "046", "195", "100", "296"]
#doc_types = ["ACO","CO","OC","TRA","CH","CHEC"]
years = [2014,2013,2012,2010,2009,2008,2007]
recent_years = [2014,2013,2012,2010]
doc_types = ['AC', 'ACO', 'ACUE', 'ACUEM', 'AJOC', 'CASER', 'CAT', 'CCR', 'CCUE', 'CD', 'CDNO', 'CEFA', 'CEFOIN', 'CF', 'CH', 'CHEC', 'CHESB', 'CHI', 'CO', 'COMPP', 'CONV', 'CPA', 'CUE', 'CUEP', 'CUET', 'DEM', 'DEN', 'DJB', 'ENM', 'GC', 'GCOSB', 'LETT', 'LEVE', 'LEVP', 'LEVS', 'LEYTRANSP', 'LIQ', 'MOV', 'OC', 'OF', 'OP', 'PAC', 'PAL', 'PLANAD', 'PLANCOM', 'POD', 'POL', 'QUE', 'RC', 'REC', 'REDPART', 'REEM', 'REEMPRE', 'REISO', 'RES', 'RF', 'RPA', 'SAD', 'SOL', 'SV', 'TRA', 'TRA.CERP', 'TRAS']

db_url = os.environ['panadata_db']
doc_lock = asyncio.Lock()
sem = asyncio.Semaphore(7)
engine = create_engine(db_url, convert_unicode=True, echo=True)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
loop = asyncio.get_event_loop()
states = set ()
visited = set()

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read())

@asyncio.coroutine
def get_html(url):
    with (yield from sem):
         return (yield from get(url))

def crawl_all():
    shuffle(office_ids)
    for office in office_ids:
        crawl_oficina(office)

def crawl_oficina(oficina_id):
    logger.info('Crawling %s',oficina_id)
    data = url_generator.parse_har()
    for d in doc_types:
        data = url_generator.set_doc_type(url_generator.set_oficina_id(data,oficina_id),d).copy()
        for year in recent_years:
            states.clear()
            visited.clear()
            docs = set()
            states.add('_')
            data = url_generator.set_year(data,year)
            new_tasks = spawn_queries(data,states)
            while new_tasks:
                try:
                    loop.run_until_complete(new_tasks)
                    new_tasks = spawn_queries(data,states.difference(visited))
                    visited.update(states)
                except ValueError:
                   break

def spawn_queries(data,states):
    queries = states_to_queries(data,states)
    new_tasks = []
    for q in queries:
        new_tasks.append(asyncio.async(crawl_pages(q)))
    return asyncio.wait(new_tasks)

def process_query(docs,data):
    session = session_maker()
    states.update([s for s in docs_to_states(docs) if s not in visited])
    docs = [ db_worker.create_documento(item,session) for item in docs if item.control not in visited ]
    session.close()

def states_to_queries(data,states):
   queries = list()
   for s in states:
       d = data.copy()
       queries.append(url_generator.set_document_id(d,s))
   return queries

def state_to_query(data,state):
   d = data.copy()
   return url_generator.set_document_id(d,state)

def docs_to_states(docs):
    states = set()
    for d in docs:
        tokens = ''.join(c for c in d.numero if c.isalnum() or c.isspace() or c.isdigit() or c == '-').split('-')
        for token in tokens:
            if token.isdigit():
                if token not in [str(y) for y in years]:
                    states.update(int_to_states(token))
            else:
                states.update(token.split())
    return states

def int_to_states(i):
    i = math.floor(int(i)/100)
    return [ str(n) + '__' for n in range(i-2,i+2) ]

@asyncio.coroutine
def post(*args, **kwargs):
    response = yield from aiohttp.request('POST', *args, **kwargs)
    if response.status == 200 and 'error' not in response.url:
        return (yield from response.read())
    response.close()

@asyncio.coroutine
def crawl_pages(data):
    logger.info('crawling %s',url_generator.get_document_id(data))
    docs = set()
    while url_generator.get_page(data) < 5:
        with (yield from sem):
                html = yield from post(url, data=data)
        soup = BeautifulSoup(html,'lxml')
        docs.update(parser.get_documentos(soup))
        if not parser.has_pages(soup): break
        data = url_generator.increment_page(data)
        data = url_generator.set_event_validation(data,parser.get_event_validation(soup))
        data = url_generator.set_view_state(data,parser.get_view_state(soup))
    with (yield from doc_lock):
        process_query(docs,data)
    logger.debug('found %i docs',len(docs))
