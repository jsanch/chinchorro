#!/usr/bin/python3
import sys
import argparse
import os
import logging.config
import yaml
from modules import parser
from modules import crawler

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# create logger
logging.config.dictConfig(yaml.load(open('logging.yaml','r').read()))
logger = logging.getLogger('contraloriadump')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dataminer de Contraloria Panama')
    parser.add_argument('--oficina', dest='oficina', type=str)
    args = parser.parse_args()
    #crawler.setThreads(args.threads) #set threads
    logger.info('dump started')
    if args.oficina:
        crawler.crawl_oficina(args.oficina)
    else:
        crawler.crawl_all()



