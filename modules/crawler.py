from multiprocessing import Pool
from modules import parser,url_generator,db_worker
from bs4 import BeautifulSoup,SoupStrainer
import math
from random import shuffle
import re
import logging
import sys
sys.setrecursionlimit(10000)
import urllib3

#conn = urllib3.HTTPConnectionPool('190.34.178.19', maxsize=15)
logger = logging.getLogger('crawler')
url = '/Sicowebconsultas/buscar.aspx'
office_ids = [202, 43, 624, 108, 1, 29, 114, 238, 234, 105, 47, 145, 22, 103, 203, 107, 109, 16015, 106, 55, 57, 204, 315, 330, 345, 600, 115, 208, 11018, 274, 360, 110, 212, 375, 521, 522, 311, 11004, 11014, 625, 623, 628, 58, 45, 611, 614, 612, 613, 615, 616, 617, 618, 610, 619, 31, 2, 53, 224, 621, 1702, 33, 111, 11005, 11006, 49, 41, 397, 63, 50, 60, 1703, 299, 704, 900, 198, 278, 699, 54, 701, 38, 39, 123, 52, 11015, 1232, 118, 124, 152, 266, 120, 137, 51, 125, 391, 362, 270, 390, 130, 392, 23, 122, 151, 142, 140, 640, 643, 644, 639, 645, 641, 646, 642, 622, 638, 649, 635, 653, 652, 650, 647, 632, 636, 651, 633, 637, 648, 634, 620, 282, 163, 16501, 10091, 8, 10, 21, 16, 7, 7041, 7061, 17, 3, 9, 12, 12021, 18, 13, 14, 20, 5, 629, 507, 525, 508, 569, 585, 570, 526, 541, 501, 527, 528, 529, 586, 587, 571, 597, 517, 572, 502, 543, 573, 574, 503, 547, 516, 580, 530, 531, 518, 532, 558, 524, 539, 545, 575, 588, 509, 548, 589, 559, 549, 560, 561, 584, 538, 590, 542, 510, 540, 546, 550, 511, 576, 551, 562, 512, 552, 544, 563, 519, 533, 534, 591, 596, 577, 535, 592, 536, 578, 593, 520, 553, 594, 595, 579, 537, 564, 146, 700, 28, 30, 135, 117, 37, 800, 999, 11003, 181, 11011, 11008, 11009, 11010, 11012, 11007, 153, 11002, 133, 36, 1619, 35, 1633, 148, 11, 703, 44, 134, 705, 226, 276, 56, 112, 183, 119, 182, 184, 27, 1701, 655, 310, 121, 275, 26, 626, 702, 40, 193, 187, 190, 46, 195, 100, 296]
doc_types = ["OC","CO","TRA","CH"]

def crawl_all():
    shuffle(office_ids)
    for office in office_ids:
        crawl_oficina(office)

def crawl_oficina(oficina_id):
    logger.info('Crawling %s',oficina_id)
    data = url_generator.parse_har()
    for d in doc_types:
        data = url_generator.set_oficina_id(data,oficina_id)
        data = url_generator.set_doc_type(data,d)
        crawl(data,docs_to_states)

def crawl(data,doc_parser):
    pool = Pool(processes=4)
    for year in [2009,2010,2011,2012,2013,2014]:
        logger.info('crawling year %i',year)
        data = url_generator.set_year(data,year)
        states = ['_']
        visited = set()
        docs = set()
        depth = 0
        while states:
            visited.update(states)
            queries = states_to_queries(data,states)
            docs = { item for sublist in pool.map(crawl_pages,queries) for item in sublist }
            states = [s for s in doc_parser(docs) if s not in visited]
            for doc in docs: db_worker.create_documento(doc)
            depth += 1
            logger.info('found %i docs',len(docs))
            logger.info('found %i new states',len(states))
        logger.info('total depth for %i: %i',year,depth)
    pool.close()

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
    regex = re.compile("\d+")
    for d in docs:
        if regex.match(d.numero):
            states.update([item for sublist in [int_to_states(n) for n in regex.findall(d.numero)] for item in sublist])
        else:
            s = str(d.numero).split(' ')[0][:2] + '__'
            states.add(s)
    return states

def int_to_states(i):
    i = math.floor(int(i)/100)
    return [ str(n) + '__' for n in range(i-2,i+2) ]

def crawl_pages(data):
    logger.debug('crawling %s',url_generator.get_document_id(data))
    conn = urllib3.HTTPConnectionPool('190.34.178.19', maxsize=15)
    docs = set()
    while url_generator.get_page(data) < 5:
        html = conn.request("POST", url, data).data.decode('ISO-8859-1','ignore')
        soup = BeautifulSoup(html,'lxml')
        docs.update(parser.get_documentos(soup))
        if not parser.has_pages(soup): break
        data = url_generator.increment_page(data)
        data = url_generator.set_event_validation(data,parser.get_event_validation(soup))
        data = url_generator.set_view_state(data,parser.get_view_state(soup))
    logger.debug('found %i docs',len(docs))
    conn = urllib3.HTTPConnectionPool('190.34.178.19', maxsize=15)
    conn.close()
    return docs
